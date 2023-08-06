from config.logger import *

class product_information:

    def __init__(self) -> None:
        pass

    def __extract_product_info(self, content):
        #log.info("Fetching details")
        import re
        count = 0
        for a in content.findAll('div', attrs={'class':'_1YokD2 _3Mn1Gg col-8-12'}):
            name=a.find('span', attrs={'class':'B_NuCI'}).text
            name = name.split("(")[0].strip()
            price=a.find('div', attrs={'class':'_30jeq3 _16Jk6d'}).text
            rating=a.find('div', attrs={'class':'_3LWZlK'}).text
            no_of_reviews = a.find('span', attrs = {'class' : '_2_R_DZ'}).text
            
            #Removing special characters in the price
            price = str(int(price.replace("₹","").replace(",", "")))
            
            #Extarcting Number Of ratings
            ratings_count = no_of_reviews.replace(",", "")
            ratings_count = re.search(r"(\d+) Ratings", ratings_count)
            ratings_count = str(int(ratings_count.groups()[0]))

            #Extarcting Number Of Reviews
            reviews_count = no_of_reviews.replace(",", "")
            reviews_count = re.search(r"(\d+) Reviews", reviews_count)
            reviews_count = str(int(reviews_count.groups()[0]))

        return name, price, rating, ratings_count, reviews_count

    def get_product_info(self, content):
        name, price, rating, ratings_count, reviews_count  = self.__extract_product_info(content)

        return {"product"        : name,
                "price"          : price,
                "overall_rating" : rating,
                "ratings_count"  : ratings_count,
                "reviews_count"  : reviews_count}


product_info = product_information().get_product_info