#Made by cloud :3

import requests
from bs4 import BeautifulSoup
import time
import json
import csv
import os
from shopify_scraper import scraper

global present
global scrap
#Set to true to send messege for deal of day, Set to false to ignore previous
present = False

scrap = ['https://thefloatlife.com', 'https://pickleworks.ca', 'https://craftandride.com', 'https://fungineers.us', 'https://nickleworks.com', 'https://1wheelparts.com', 'https://floatershack.com']

# Function to send Discord webhook message
def send_webhook_message(Namer, product_name, product_image, link, ):
    webhook_url = '###################'

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

def extract_pricing_name_color_and_extra(filename):
    pricing_name_color_and_extra = []
    with open(filename, newline='', encoding='utf-8') as csvfile:  # specify the encoding
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extracting the pricing data (price)
            price = float(row['price'])
            
            # Extracting the name
            quicktitle = row['title']

            title = row["parent_title"]

            # Extracting the color
            option1 = row['option1']

            # Extracting the extra information
            option2 = row['option2']

            # Extracting the company
            option3 = row['option3']

            company = row['vendor']

            beforeprice = row['compare_at_price']
            
            # Extracting the ID
            product_id = row['id']

            # Extracting the product ID

            real_product_id = row['product_id']
            
            pricing_name_color_and_extra.append((price, quicktitle, title, option1, option2, option3, company, beforeprice, product_id, real_product_id))
    return pricing_name_color_and_extra


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
        
        #Scraper
        try:
            if scrap:
                    
                for scrapeurl in scrap:

                    try:

                        print(f"Scraping {scrapeurl}")
                        name = scrapeurl.split('/')[-1]
                        print(f"Scraping {name}")
                        parents = scraper.get_products(scrapeurl)
                        print('Parents: ', len(parents))


                        children = scraper.get_variants(parents)

                        children.to_csv(f'childrentemp.csv', index=False)

                        try: 
                            old_list = extract_pricing_name_color_and_extra(f'{name}children.csv')
                            new_list = extract_pricing_name_color_and_extra(f'childrentemp.csv')

                            # Comparing prices and printing differences
                            # Comparing prices and printing differences based on product IDs
                            # Comparing prices and printing differences based on product IDs
                            item_sent = []
                            hold_pid = ""
                            for old_item in old_list:
                                old_price, old_quicktitle, old_title, old_option1, old_option2, old_option3, old_company, old_beforeprice, old_product_id, old_real_product_id = old_item
                                for new_item in new_list:
                                    new_price, new_quicktitle, new_title, new_option1, new_option2, new_option3, new_company, new_beforeprice, new_product_id, new_real_product_id = new_item
                                    if old_product_id == new_product_id and old_price != new_price:

                                        if (old_price > new_price):
                                            print(f"Difference found for product with ID {old_product_id}: Old Price - {old_price}, New Price - {new_price}")
                                            difer = round(abs((new_price - old_price) / old_price) * 100, 2)
                                            difer_str = str(difer)
                                            print("running check")
                                            if (difer <= 1):
                                                print("Sale less then 1%")
                                            else:
                                                print("sending webhook")
                                                print("New title: ", new_title, "Old title: ", old_title, "New price: ", new_price, "Old price: ", old_price, "Diference: ", difer_str) 
                                                messegee = f"{new_title} is now {new_price}$ {difer_str}% off"
                                                fixedtitle = new_title.replace(" ", "-")
                                                sendurl = f"{scrapeurl}/products/{fixedtitle}"
                                                try:
                                                    # Fetch the webpage content
                                                    response = requests.get(sendurl)
                                                    response.raise_for_status()

                                                    # Parse the webpage content using BeautifulSoup
                                                    soup = BeautifulSoup(response.text, 'html.parser')

                                                    # Find the first image tag (you may need to adjust this based on the structure of the webpage)
                                                    img_tag = soup.find('img')

                                                    # Extract the source (src) attribute of the image tag
                                                    if img_tag:
                                                        embed_photo_url = img_tag.get('src')
                                                        embed_photo_url = f"https:{embed_photo_url}"
                                                        print("Embedded photo URL:", embed_photo_url)
                                                    else:
                                                        print("No embedded photo found.")
                                                        embed_photo_url = ''

                                                except Exception as e:
                                                    print("Error:", e)
                                                    embed_photo_url = ''
                                                    sendurl = scrapeurl
                                                #Make sure items sent before aren't send
                                                if new_real_product_id not in item_sent:
                                                    hold_pid = new_quicktitle
                                                    send_webhook_message(f"New Deal From {new_company}!", messegee, embed_photo_url, sendurl)
                                                    item_sent.append(new_real_product_id)
                                                else:
                                                    if hold_pid != "":
                                                        send_webhook_message(f"", f"{hold_pid}", '', sendurl)
                                                        hold_pid = ""
                                                    send_webhook_message(f"", f"{new_quicktitle}", '', sendurl)


                                            break
                                        elif (old_price < new_price):
                                            print(f"Difference found for product with ID {old_product_id}: Old Price - {old_price}, New Price - {new_price}")
                                        break
                                else:
                                    print(f"No difference found for product with ID {old_product_id}")
                        except:
                            print("Failed to find differences but like so bad it crashed :3")
                    except:
                        print(f"{scrapeurl} Failed To Scrape")



                    children.to_csv(f'{name}children.csv', index=False)
                    print('Children: ', len(children))
        except:
            print("Crashed the scraper")
            print("Starting timeout to prevent timeout again")
            time.sleep(300)
            print("starting again")


                
                    

	#More could be added
        print("waiting")
        time.sleep(80)  # Check every 80 seconds
        print("Running again")

# Start monitoring the deal of the day
monitor_deals()
