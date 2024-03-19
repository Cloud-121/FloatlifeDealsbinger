import requests
from bs4 import BeautifulSoup
import time
import json

global present
#Set to true to send messege for deal of day, Set to false to ignore previous
present = True

# Function to send Discord webhook message
def send_webhook_message(Namer, product_name, product_image, link):
    webhook_url = 'WEBHOOK'

    data = {
    "username" : "Vesc Deals"
    }

    data["embeds"] = [
        {
        "description" : f"[{product_name}]({link})",  # Added comma here
        "title" : f"{Namer}",
        "image": {"url": f"{product_image}"}
        }
    ]

    result = requests.post(webhook_url, json = data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

# Function to get deal of the day products
def get_deal_of_the_day_products():
    print("Finding Day")
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
    print("Finding Jeff")
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

# Function to continuously check for changes in product names and send webhook
def monitor_deals():
    previous_names = set()

    while True:

	#The Float Life Section
        #Deal of day
        deal_of_the_day_products = get_deal_of_the_day_products()
        if deal_of_the_day_products:
            for product in deal_of_the_day_products:
                if product['name'] not in previous_names:
                    if (present): 
                        print(f"Preset set to True")
                        send_webhook_message("New Deal Of The Day From The Float Life!!", product['name'], product['image'], "https://thefloatlife.com/collections/deal-of-the-day")
                        previous_names.add(product['name'])
                    else:
                        print(f"Present was set to False")
                        preset = True
                        print(f"Preset set to {preset}")
                        print("adding previous")
                        previous_names.add(product['name'])
                        print("Added prev")
                else:
                    print("Same as before")

        #Thrift Shop
        thriftshop = jeffthriftshop()
        if thriftshop:
            for product in thriftshop:
                if product['name'] not in previous_names:
                    if (present): 
                        print(f"Preset set to True")
                        send_webhook_message("New Thrift From The Float Life!!", product['name'], product['image'], "https://thefloatlife.com/collections/jeffs-thrift-shop")
                        previous_names.add(product['name'])
                    else:
                        print(f"Present was set to False")
                        preset = True
                        print(f"Preset set to {preset}")
                        print("adding previous")
                        previous_names.add(product['name'])
                        print("Added prev")
                else:
                    print("Same as before")
                    

	#More could be added
        print("waiting")
        time.sleep(60)  # Check every 60 seconds
        print("Running again")

# Start monitoring the deal of the day
monitor_deals()
