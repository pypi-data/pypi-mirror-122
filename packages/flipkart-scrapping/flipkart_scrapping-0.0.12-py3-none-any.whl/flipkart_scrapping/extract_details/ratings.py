class extract_ratings:

    def __init__(self) -> None:
        pass

    def __extract_ratings(self, content):
        #print("extract_phone_details started")
        #print(content)
        rating_details = None
        camera_rating, battery_rating, display_rating, value_for_money  = range(0, 4)
        for a in content.findAll('div', attrs={'class': '_2LE14f'}):
            rating_details = a.findAll('text', attrs={'class' : '_2Ix0io'})
            #print("rating details")
            #print(rating_details)
            break
        if rating_details is None:
            return []
        if len(rating_details) != 4:
            return []
        
        return [rating_details[camera_rating].text, rating_details[battery_rating].text,
               rating_details[display_rating].text, rating_details[value_for_money].text]

    def get_ratings(self, content):
        ratings = self.__extract_ratings(content)
        if ratings == []:
            return {}
        camera_rating, battery_rating, display_rating, value_for_money  = range(0, 4)
        return {"camera_rating"    : ratings[camera_rating],
                "battery_rating"   : ratings[battery_rating],
                "display_rating"   : ratings[display_rating],
                "value_for_money"  : ratings[value_for_money]}


get_ratings = extract_ratings().get_ratings