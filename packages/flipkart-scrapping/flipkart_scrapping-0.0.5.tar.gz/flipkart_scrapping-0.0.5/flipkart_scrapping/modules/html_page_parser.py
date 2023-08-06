from bs4 import BeautifulSoup as bsp

def __html_text_parser(html_text : str):
    html_page = bsp(html_text, "html.parser")
    return html_page

html_parser = __html_text_parser
