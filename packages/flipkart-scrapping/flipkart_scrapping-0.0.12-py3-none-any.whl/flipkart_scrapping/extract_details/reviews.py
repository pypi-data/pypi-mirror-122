from config.logger import *

class extract_reviews:
    
    def __init__(self) -> None:
        pass

    def __extract_review_rating(self, content) -> str:
        rating = content.find('div', attrs={'class': '_3LWZlK _1BLPMq'})
        if rating is None:
            rating = content.find('div', attrs={'class': '_3LWZlK _1rdVr6 _1BLPMq'})
        return rating.text

    def __extract_mini_review(self, content) -> str:
        comment_header = content.find('p', attrs={'class': '_2-N8zT'})
        return comment_header.text

    def __extract_reviewed_date(self, content) -> str:
        commented_on = content.findAll('p', attrs={'class': '_2sc7ZR'})[1]
        return commented_on.text

    def __extract_full_review(self, content) -> str:
        comment = content.find('div', attrs={'class': 't-ZTKy'})
        comment = comment.find("div", attrs={"class" : ""}).text
        if(comment.startswith('...')):
            comment = comment[3:]
        if(comment.strip().endswith('READ MORE')):
            comment = comment[:-9]
        return comment

    def __get_review(self, content) -> dict:
        review_rating = self.__extract_review_rating(content)
        mini_review   = self.__extract_mini_review(content)
        full_review   = self.__extract_full_review(content)
        review_date   = self.__extract_reviewed_date(content)

        return {"review_rating" : review_rating,
                "mini_review"   : mini_review,
                "full_review"   : full_review,
                "review_date"   : review_date}

    def reviews(self, main_content, max_reviews=-1) -> list:
        reviews_list = []
        for content in main_content.findAll('div', href=False, attrs={'class': '_27M-vq'}):
            review = self.__get_review(content)
            reviews_list.append(review)
            max_reviews -= 1
            if max_reviews == 0:
                break
        return reviews_list

get_reviews = extract_reviews().reviews