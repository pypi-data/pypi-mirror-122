# __package__ = None
from selenium import webdriver
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), r'C:\Users\Simeon\PycharmProjects\ebay_car_scraper_pypi'))

import unittest
from car_scraper.car_scraping_1 import Carscraper
import random

#Customized options for Chrome
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
desired_capabilities = options.to_capabilities()

class CarscraperTestCase(unittest.TestCase):

    def setUp(self):
        self.carscraper = Carscraper()
        self.carscraper.driver = webdriver.Chrome(r"C:\Users\Simeon\Downloads\chromedriver_win32\chromedriver",
                                       desired_capabilities=desired_capabilities)

    # def test_wrong_link(self):
    #     page = 50
    #     with self.assertRaises(ValueError) as err:
    #         self.car_scraping_1.get_links(page)

    def test_no_of_cars_per_page(self):
        # code to test scraper returns the expected number of cars on the webpage
        i = 13
        url = f"https://www.ebay.co.uk/b/Cars/9801/bn_1839037?page=%7Bpage%7D&_pgn=" + str(i)
        self.carscraper.driver.get(url)
        no_of_cars = 48
        xpath = "//ul[@class='b-list__items_nofooter srp-results srp-grid']/li"
        self.carscraper.driver.find_elements_by_xpath(xpath)
        actual_value = len(self.carscraper.driver.find_elements_by_xpath(xpath))
        expected_value = no_of_cars
        self.assertEqual(actual_value, expected_value)


    # def test_correct_url(self):
    #     #code to test scraper return the correct url
    #     url = f"https://www.ebay.co.uk/b/Cars/9801/bn_1839037?page=%7Bpage%7D&_pgn=50"
    #     self.carscraper.driver.get(url)
    #     actual_value = self.carscraper.driver.current_url
    #     expected_value = url
    #     self.assertEqual(actual_value, expected_value)


    #
    #
    # def check_exists(self)
    #
    # def test_wrong_date(self):
    #     date = 'February_30'
    #     with self.assertRaises(ValueError) as err:
    #         self.scraper.get_celebrities(date)
unittest.main(argv=[''], verbosity=0, exit=False)
