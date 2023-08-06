#__package__ = None
from car_scraper.car_scraping_1 import Carscraper
from rds_uploader.rds_scraped_ebay_cars import DataHandling



simulate = DataHandling()
scrap_upload = simulate.run_data()
# simulate = Carscraper()
#

# car_property = simulate.get_car_details()
