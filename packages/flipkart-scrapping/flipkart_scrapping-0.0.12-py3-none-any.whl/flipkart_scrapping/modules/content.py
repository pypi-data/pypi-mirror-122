import requests as rq
from html_page_parser import html_parser

class pageContent:

    def __init__(self) -> None:
        pass

    def get_contents(self, url : str) -> str:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        content = rq.get(url, headers=headers)
        return content.content

    def content(self, request_url : str): 
        #log.info(f"url {request_url}")
        
        content = self.get_contents(request_url)
        html_page_content = html_parser(content)
        return html_page_content

page_content = pageContent().content