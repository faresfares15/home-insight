from bs4 import BeautifulSoup
import pandas as pd
import re

from Utilities import save_csv, get_data_frame, save_to_db


def scraper(content, file_path):
    prices = []
    rooms = []
    bedrooms = []
    sizes = []
    addresses = []
    print(type(content), content)
    soup = BeautifulSoup(content, features='html.parser')
    print(type(soup), '\n------ SOUP ------\n')
    print(soup)
    for element in soup.findAll('div', attrs={'class': 'col-1-3'}):
        price = element.find('span', attrs={'class': 'item-price'})
        address = element.find('span', attrs={'class': 'h1'})
        # extracting rooms bedrooms and the size
        item_tags_ul = element.find('ul', attrs={'class': 'item-tags'})

        if item_tags_ul:
            li_elements = item_tags_ul.find_all('li')

            # check if they are present
            if len(li_elements) >= 3:
                # Extract numeric part from the first element using regular expressions
                room_number = re.search(r'\d+', li_elements[0].text)
                room = room_number.group() if room_number else None

                # Extract numeric part from the second element using regular expressions
                bedroom_number = re.search(r'\d+', li_elements[1].text)
                bedroom = bedroom_number.group() if bedroom_number else None

                # Extract numeric part from the third element using regular expressions
                size_number = re.search(r'\d+', li_elements[2].text)
                size = size_number.group() if size_number else None
            else:
                room = bedroom = size = None
        else:
            room = bedroom = size = None
        if room and bedroom and size:
            rooms.append(room)
            bedrooms.append(bedroom)
            sizes.append(size)
            if price and price.text:
                price_text = price.text.replace('€', '').replace(' ', '').replace('.', '')
                price = float(price_text)
                prices.append(price)
            if address and address.text:
                addresses.append(' '.join(address.text.split()))
    print(addresses, prices, rooms, bedrooms, sizes)

    new_data_frame = pd.DataFrame({
        'Address': addresses,
        'Price': prices,
        'Rooms': rooms,
        'Bedrooms': bedrooms,
        'Size': sizes
    })
    if addresses == [] or prices == [] or rooms == [] or bedrooms == [] or sizes == []:
        print("couldn't scrape properly")
        return new_data_frame
    else:
        try:
            old_data_frame = get_data_frame()
            result_data_frame = pd.concat([old_data_frame, new_data_frame], ignore_index=True)
            result_data_frame = result_data_frame.drop_duplicates()
            save_csv(result_data_frame, file_path)
            save_to_db(result_data_frame)
        except Exception as e:
            print("Got a problem with the data frame, " + e.__str__() + " creating a new one")
            result_data_frame = new_data_frame

        return result_data_frame
