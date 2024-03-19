import requests
from bs4 import BeautifulSoup
import time
import json

global present
# Set to True to send message for deal of the day, Set to False to ignore previous.
present = True

def send_webhook_message(Namer, product_name, product_image, link):
    webhook_url = 'https://discord.com/api/webhooks/1219439917038305290/IhJreQphZKuYmQw_InEQkkgmx84ZBdhncNfwwc41ge0ifUQtpfiFqsU8H0-sd4YgsZUn'

    data = {
        "username": "Vesc Deals"
    }

    data["embeds"] = [
        {
            "description": f"[{product_name}]({link})",
            "title": f"{Namer}",
            "image": {"url": f"{product_image}"}
        }
    ]

    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def get_deal_of_the_day_products():
    url = 'https://thefloatlife.com/collections/deal-of-the-day'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_infos = soup.find_all('div', class_='product-card__info')
        products = []
        for info in product_infos:
            product_info = {}
            img_tag = info.find_previous('img', class_='lazyload')
            if img_tag:
                product_info['name'] = img_tag.get('alt', 'No name available')
                image_url = img_tag.get('data-src', 'No image available')
                image_url = image_url.replace('{width}', '300')
                image_url = 'https:' + image_url
                product_info['image'] = image_url
                products.append(product_info)
        return products
    return None

def jeffthriftshop():
    url = 'https://thefloatlife.com/collections/jeffs-thrift-shop'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_infos = soup.find_all('div', class_='product-card__info')
        products = []
        for info in product_infos:
            product_infothrift = {}
            img_tag = info.find_previous('img', class_='lazyload')
            if img_tag:
                product_infothrift['name'] = img_tag.get('alt', 'No name available')
                image_url = img_tag.get('data-src', 'No image available')
                image_url = image_url.replace('{width}', '300')
                image_url = 'https:' + image_url
                product_infothrift['image'] = image_url
                products.append(product_infothrift)
        return products
    return None

def monitor_deals():
    previous_names = set()

    while True:
        deal_of_the_day_products = get_deal_of_the_day_products()
        if deal_of_the_day_products:
            for product in deal_of_the_day_products:
                if product['name'] not in previous_names:
                    if present:
                        print(f"Preset set to True")
                        send_webhook_message("New Deal Of The Day From The Float Life!!", product['name'], product['image'], "https://thefloatlife.com/collections/deal-of-the-day")
                        previous_names.add(product['name'])
                    else:
                        print(f"Present was set to False")
                        present = True
                        print(f"Preset set to {present}")
                        print("adding previous")
                        previous_names.add(product['name'])
                        print("Added prev")
                else:
                    print("Same as before")

        thriftshop = jeffthriftshop()
        if thriftshop:
            for product in thriftshop:
                if product['name'] not in previous_names:
                    if present:
                        print(f"Preset set to True")
                        send_webhook_message("New Thrift From The Float Life!!", product['name'], product['image'], "https://thefloatlife.com/collections/jeffs-thrift-shop")
                        previous_names.add(product['name'])
                    else:
                        print(f"Present was set to False")
                        present = True
                        print(f"Preset set to {present}")
                        print("adding previous")
                        previous_names.add(product['name'])
                        print("Added prev")
                else:
                    print("Same as before")
                    
        print("waiting")
        time.sleep(60)
        print("Running again")

monitor_deals()
