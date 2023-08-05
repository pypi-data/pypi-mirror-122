# ebay_car_scraper_pypi
This package has been created solely for extrcating second hand car data from ebay to enable one to make comparisons among cars based on Manufacturers, Mileage, fuel-type, location etc.

It has a package with one module;car_scraping_1, test folder and rds uploader.

car_scraping_1 has 3 methods that allows it to get links to webpages, link for each car on the individual webpages and finally put all the data in a dictionary which is converted into a pandas DataFrame and stored as a csv file

The test folder includes a package with one module; test_car_scraping_1. This module helps to check the link is working as well as checks the number of cars returned per page.

The rds uploader folder includes a package with one module; rds_scraped_ebay_cars. This module helps load the pandas DataFrame, connect to AWS RDS, creates the table and uploads the data into the database.
