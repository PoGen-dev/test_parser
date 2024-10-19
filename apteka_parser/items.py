# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from pydantic import BaseModel


class ProductItem(Item):
    product_id = Field()
    name = Field()
    price = Field()
    special_price = Field()
    manufacturer = Field()
    country = Field()


class Product(BaseModel):
    product_id: int
    name: str
    price: float
    special_price: float
    manufacturer: str
    country: str
