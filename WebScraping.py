#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing modules
import requests  #To get the webpage content
from bs4 import BeautifulSoup  #To parse the HTML code
import pandas 
import argparse 
import connect


# In[2]:


parser = argparse.ArgumentParser()
parser.add_argument("--page_num_max", help = "Enter the number of pages to parse", type = int)
parser.add_argument("--dbname", help = "Enter the number of pages to parse", type = int)
args, unknown = parser.parse_known_args()

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_num_MAX = args.page_num_max
scraped_info_list = []
connect.connect(args.dbname)

for page_num in range(1, page_num_MAX):
  url = oyo_url + str(page_num)
  
  req = requests.get(url)
  content = req.content
    
  soup = BeautifulSoup(content, "html.parser")

  all_hotels = soup.find_all("div", {"class": "hotelCardListing"})

  for hotel in all_hotels:
      hotel_dict = {}
      hotel_dict["name"] = hotel.find("h3", {"class": "ListingHotelDescription_hotelName"}).text
      hotel_dict["address"] = house.find("span", {"intemprop": "streetAddress"}).text
      hotel_dict["price"] = hotel.find("span", {"class": "listingPrice__finalPrice"}).text

      #try ..... except
      try:
          hotel_dict["rating"] = hotel.find("span", {"class": "hotelRating__ratingSummary"}).text                                                                                      
      except AttributeError:
        pass
        #hotel_dict["rating"] = None Use this if an error related to values is faced

      parent_amenities_element = hotel.find("div", {"class": "amenityWrapper"})

      amenities_list = []
      for amenity in parent_amenities_element.find_all("div", {"class": "amenityWrapper_amenity"}):
        amenities_list.append(amenity.find("span", {"class": "d-body-sm"}).text.strip())

      hotel_dict["amenities"] = ', '.join(amenities_list[:-1]) #Joining and slicing the dictionary elements
    
      scraped_info_list.append(hotel_dict)
      connect.insert_into_table(args.dbname, tuple(hote_dict.values()))
      
      #print(hotel_name, hotel_address, hotel_price, hotel_rating, amenities_list)

dataFrame = pandas.DataFrame(scraped_info_list)
dataFrame.to_csv("Oyo.csv")
connect.get_hotel_info(args.dbname)

