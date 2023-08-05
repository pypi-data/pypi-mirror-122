__package__ = None
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as exception
from sqlalchemy import create_engine

import pandas as pd
import json
import csv
import time

#Customized options for Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
desired_capabilities = options.to_capabilities()

cars_data1 = []

class Carscraper:
    '''
    This class is used to represent a car scraper.

    Attributes:
        manufacturer: The manufacturer of the car.
        model: The model of the car.
        sale_price: The sale_price of the car.
        year: The year of the car.
        transmission: The transmission of the car.
        fuel: The fuel of the car.
        mileage: The mileage of the car.
        condition: The condition of the car.
        location: The location of the car.
        contact_number: The contact_number of the car.
    '''

    def __init__(self):
        self.manufacturer = []
        self.model = []
        self.sale_price = []
        self.year = []
        self.transmission = []
        self.fuel = []
        self.mileage = []
        self.condition = []
        self.location = []
        self.contact_number = []
        self.new_list = []
        self.car_data = {}
        #self.page = range(1,31)
        self.driver = webdriver.Chrome(r"C:\Users\Simeon\Downloads\chromedriver_win32\chromedriver", desired_capabilities=desired_capabilities)

    def get_links(self):
        '''
        This function is used to get webpages (1-30), number of cars and hrefs for the cars listed
        on each of the ebay webpages.

        '''
        #self.page_urls = []
        for page in range(1, 2):
            ROOT = f"https://www.ebay.co.uk/b/Cars/9801/bn_1839037?page=%7Bpage%7D&_pgn=" + str(page)
            self.driver.get(ROOT)
            time.sleep(3)
            print(ROOT)
            #print(self.page_urls)
            listings = self.driver.find_elements_by_xpath("//ul[@class='b-list__items_nofooter srp-results srp-grid']/li")
            # print(listings)
            print(len(listings))
            cars = self.driver.find_elements_by_xpath("//div[@class='s-item__info clearfix']/a")
            for i in cars:
                time.sleep(1)
                self.new_list.append(i.get_attribute("href"))
                time.sleep(3)
            print(self.new_list)

    def get_car_details(self):
        '''
        This function is used to get specific properties (i.e sale_price, model etc)
        of the cars listed or advertised cars on each of the webpage of used cars 
        on ebay and append them to a dictionary; self.car_data.
        '''
        for car in self.new_list:
            self.driver.get(car)
            time.sleep(2)
            self.car_data = {"manufacturer": self.manufacturer, "model": self.model, "sale_price": self.sale_price, "year": self.year, "transmission": self.transmission, "fuel": self.fuel,
                        "mileage": self.mileage, "condition": self.condition, "location": self.location,
                        "contact_number": self.contact_number}

            try:
                manufacturer = self.driver.find_element_by_xpath(
                    "//td[contains(text(),'Manufacturer:')]/following-sibling::td/span").text
                self.car_data['manufacturer'].append(manufacturer)
            except NoSuchElementException:
                self.car_data['manufacturer'].append(None)
            try:
                model = self.driver.find_element_by_xpath("//td[contains(text(),'Model:')]/following-sibling::td/span").text
                self.car_data['model'].append(model)

            except NoSuchElementException:
                self.car_data['model'].append(None)

            try:
                sale_price = self.driver.find_element_by_xpath('//*[@id="prcIsum"]').text
                self.car_data['sale_price'].append(sale_price)

            except NoSuchElementException:
                self.car_data['sale_price'].append(None)

            try:
                year = self.driver.find_element_by_xpath("//td[contains(text(),'Year:')]/following-sibling::td/span").text
                self.car_data['year'].append(year)

            except NoSuchElementException:
                self.car_data['year'].append(None)

            try:
                transmission = self.driver.find_element_by_xpath(
                    "//td[contains(text(),'Transmission:')]/following-sibling::td/span").text
                self.car_data['transmission'].append(transmission)

            except NoSuchElementException:
                self.car_data['transmission'].append(None)

            try:
                fuel = self.driver.find_element_by_xpath("//td[contains(text(),'Fuel:')]/following-sibling::td/span").text
                self.car_data['fuel'].append(fuel)

            except NoSuchElementException:
                self.car_data['fuel'].append(None)

            try:
                mileage = self.driver.find_element_by_xpath("//td[contains(text(),'Mileage:')]/following-sibling::td/span").text
                self.car_data['mileage'].append(mileage)

            except NoSuchElementException:
                self.car_data['mileage'].append(None)

            try:
                condition = self.driver.find_element_by_xpath('//div[@class="u-flL condText  "]').text
                self.car_data['condition'].append(condition)

            except NoSuchElementException:
                self.car_data['condition'].append(None)

            try:
                location = self.driver.find_element_by_xpath('//span[@itemprop="availableAtOrFrom"]').text
                self.car_data['location'].append(location)

            except NoSuchElementException:
                self.car_data['location'].append(None)

            try:
                contact_number = self.driver.find_element_by_xpath('//div[@id="slrCntctNum"]').text
                self.car_data['contact_number'].append(contact_number)

            except NoSuchElementException:
                self.car_data['contact_number'].append(None)

        time.sleep(2)
        self.driver.back()
        time.sleep(2)
        print(self.car_data)
        #cars_data1.append(car_data)


    def print_to_json_and_csv(self):
        '''
        This function is used to print the self.car_data dictionary to a
        json file and subsequently to a dataframe & csv file.
        '''
        with open("car_data.json", "w") as g:
            json.dump(self.car_data, g)
        with open(r"C:\Users\Simeon\PycharmProjects\ebay_car_scraper_pypi\car_scraper\car_data.json", 'r') as f:
            self.car_data = json.load(f)
            self.car_data_df = pd.DataFrame(self.car_data, columns = ['manufacturer', 'model', 'sale_price', 'year', 'transmission', 'fuel', 'mileage', 'condition', 'location', 'contact_number'])
            #print(self.car_data_df)
            self.car_data_df.to_csv("car_data_df.csv")
        return self.car_data_df

    def run(self):
        '''
        This function is used to run or execute all the methods.
        '''
        self.get_links()
        #self.get_cars()
        self.get_car_details()
        self.print_to_json_and_csv()

scraper = Carscraper()
scraper.run()