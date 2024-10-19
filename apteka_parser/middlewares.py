# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        chrome_options.binary_location = "resourse/chrome-win64/chrome.exe"
        servise = Service(
            executable_path="resourse/chromedriver-win64/chromedriver.exe"
        )
        self.driver = webdriver.Chrome(service=servise, options=chrome_options)

    def process_request(self, request, spider) -> HtmlResponse:
        self.driver.get(request.url)
        body = self.driver.page_source
        return HtmlResponse(
            self.driver.current_url, body=body, encoding="utf-8", request=request
        )

    def __del__(self):
        self.driver.quit()
