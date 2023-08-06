class page:

    def __init__(self) -> None:
        pass
    
    def form_prd_url(self, product):
        #log.info(f"Forming Product Main URL for product - {product}")
        return f"https://www.flipkart.com/search?q={product}"

    def get_next_page_url(self, page_url, next_page_number):
        return f"{page_url}&page={next_page_number}"

    def get_product_urls(self, main_content): 
        urls = []
        a = main_content.find("div", href=False, attrs={"class" : "_36fx1h _6t1WkM _3HqJxg"})
        for a in a.findAll("a", attrs={"class"  :"_1fQZEK"}):
            #log.info(a.get("href"))
            href = a.get("href")
            url = f"https://www.flipkart.com{href}"
            urls.append(url)
        return urls

    def get_reviews_next_page(self, content):
        try:

            next_page = content.findAll('a', href=True, attrs={'class' : '_1LKTO3'})[-1] 
            next_page = f"https://www.flipkart.com{next_page.get('href')}"
            if not next_page.endswith('=2'):
                return None
            return next_page
        except Exception as e:
            #print(str(content) + " " + "exception")
            return None

    def extract_comments_page_url(self, product_content):
        comments_url = None
        for a in product_content.findAll('div', href=False, attrs={'class' : "col JOpGWq"}):
            a  = a.find('a')
            href = a.get("href")
            #log.info("href links")
            #log.info(href)
            href = href.split("&lid")[0]
            comments_url = f"https://www.flipkart.com{href}"
        return comments_url

    

reviews_next_page = page().get_reviews_next_page
comments_page = page().extract_comments_page_url
search_url = page().form_prd_url
product_urls = page().get_product_urls
next_page = page().get_next_page_url