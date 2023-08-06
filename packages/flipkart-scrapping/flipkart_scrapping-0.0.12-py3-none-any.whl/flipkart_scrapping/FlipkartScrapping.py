import os
import sys
root_dir = os.path.abspath(os.path.dirname( __file__ ))
sys.path.insert(0, root_dir)

from settings.settings import *
from config.logger import *

from modules.content import page_content

from extract_details.page import search_url, product_urls, comments_page, reviews_next_page, next_page
from extract_details.product import product_info
from extract_details.ratings import get_ratings
from extract_details.reviews import get_reviews

from file_oper.write_to_file import writeToFile

from mongo_operations.mongoOper import mongoOperations as mongo

class __flipkartScrap:

    def __init__(self):
        pass

    def initMongo(self):
        mongoobj = mongo()
        mongoobj.connect()
        return mongoobj

    def __insert_to_mongo(self, product_json):
        self.mongoobj = self.initMongo()
        self.mongoobj.insert(product_json)

    def __update_to_mongo(self, content):
        self.mongoobj.update(content)

    def __product_exists(self, product_url, product_list) -> bool:
        for p_name in product_list:
            if p_name in product_url:
                return True
        return False

    def processProductDetails(self, request_url : str):
        #Product URL
        log.info(f"Processing Page content from url {request_url}")
        product_content = page_content(request_url)

        #Extracting Main Details from the content
        log.info("Extracting Product Info")
        prod_info = product_info(product_content)
        log.info(f'Parsing Product Name {prod_info["product"]}')
        name = prod_info["product"].split("(")[0].strip()
        prod_info["product"] = name

        #Extracting Product Ratings 
        log.info("Extracting Ratings")
        ratings_content = get_ratings(product_content)
        prod_info["ratings"] = ratings_content
        prod_info["reviews"] = []

        return product_content, prod_info
    
    def processProductReviews(self, content, max_comments=2):
        # Extract comments page URL
        log.info("Processing Prouct Reviews")
        comments_page_url = comments_page(content)
        
        #Extract page Content
        log.info("Extracting Page Content")
        content = page_content(comments_page_url)       
        log.info("Extracting Reviews")
        reviews = get_reviews(content, max_comments)
        return content, reviews


    def process(self, product, to_file, to_mongo, details):

        log.info("Processing Started")
        p_search_url = search_url(product)
        log.info(f"End Product URL - {p_search_url}")
        
        no_of_products = 2
        next_page_number = 1
        products = []
        while no_of_products >= 0:
            
            content = page_content(p_search_url)
            prod_urls = product_urls(content)
            
            #Iterating over products in Flipkart   
            for url in prod_urls:
                if self.__product_exists(url, products):
                    continue
                log.info(f"Current Page Number - {next_page_number} & No of products left - {no_of_products}")
                no_of_products -=1 
                if no_of_products < 0:
                    break
                product_content, product_json = self.processProductDetails(url)
                p_name = product_json["product"]
                p_name = p_name.lower().replace(" ", "-")
                products.append(p_name)

                #Inserting product detials to mongdb
                if to_mongo:
                    self.__insert_to_mongo(product_json)

                max_comments = 3
                reviews_list = []
                while max_comments > 0:
                    content, reviews = self.processProductReviews(product_content, max_comments)
                    no_of_comments = len(reviews)
                    max_comments -= no_of_comments
                    
                    #Updating reviews to mongodb
                    if to_mongo:
                        self.__update_to_mongo(reviews)
                    if to_file:
                        reviews_list.extend(reviews)
                    if max_comments <= 0:
                        break
                    
                    log.info("Extracting Comments next page url")
                    #log.info(str(content)[:100])
                    comments_url = reviews_next_page(content)
                    if comments_url is None:
                        break
                if to_file:
                    product_json['reviews']  = reviews_list
                writeToFile(details['file'], product_json)
            if no_of_products < 0:
                    break
            next_page_number += 1
            p_search_url = next_page(p_search_url, next_page_number)

    def to_file(self, product, file):
        details = {"file" : file}
        self.process(product, to_file=True, to_mongo=False, details=details)
    
    def to_mongo(self, product):
        details = {
            "username" : "username",
            "password" : "password",
            "db_name" : "db_name",
            "collection" : "collection"
        }
        self.process(product, to_file=False, to_mongo=True, details=details)

fp_scrap = __flipkartScrap