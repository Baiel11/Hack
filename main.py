import csv
import requests
from bs4 import BeautifulSoup



def get_html(url):
    response = requests.get(url)
    return response.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_ul = soup.find('div', class_='pager-wrap').find('ul')
    last_page = pages_ul.find_all('li')[-1]
    total_pages = last_page.find('a').get('href').split('=')[-1]
    return int(total_pages)

def write_to_csv_(data):
    with open('kivano.kg.smartphones', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((
            data['title'],
            data['price'],
            data['photo']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_="list-view")
    products = product_list.find_all('div', class_="item product_listbox oh")
    base_url = 'https://www.kivano.kg'


    for product in products:
        try:
            photo = product.find('div', class_="listbox_img pull-left").find('a').find('img').get('src')
            complete_photo_url = base_url + photo
        except:
            photo = ''

        try:
            title = product.find('div', class_="listbox_title oh").find('a').text
        except:
            title = ''

        try:
            price = product.find('div', class_="listbox_price text-center").find('strong').text
        except:
            price = ''

        
        data = {'title':title, 'price':price, 'photo':base_url + photo}
        write_to_csv_(data)

        

def main():
    smartphones_url = 'https://www.kivano.kg/mobilnye-telefony'
    pages = '?page='

    total_page = get_total_pages(get_html(smartphones_url))
    for page in range(1, total_page+1):
        url_with_page = smartphones_url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)


main()









