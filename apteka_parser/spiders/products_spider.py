import scrapy
import json

from pydantic import ValidationError
from typing import List, Generator

from ..items import ProductItem, Product
from ..telegram import send_telegram_message


class ProductsSpider(scrapy.Spider):
    name = "products"

    def __init__(self, city_ids: List[int], type_ids: List[int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city_ids = city_ids
        self.types_ids = type_ids

    def start_requests(self) -> Generator:
        for city_id in self.city_ids:
            for type_id in self.types_ids:
                send_telegram_message(
                    self.settings["BOT_TOKEN"],
                    self.settings["CHAT_ID"],
                    f"Start parsing products with cityID={
                        city_id} and typeIDs={type_id}",
                )
                url = f"https://web-api.apteka-april.ru/catalog/ID,price,name,properties,@products?typeIDs={
                    type_id}&cityID={city_id}"
                yield scrapy.Request(
                    url, callback=self.parse, meta={"city_id": city_id}
                )
                send_telegram_message(
                    self.settings["BOT_TOKEN"],
                    self.settings["CHAT_ID"],
                    f"Parsing is done",
                )
                break
            break

    def parse(self, response) -> Generator:
        """
        Parse response and getting goal points.

        :param response:
        :return Generator:
        """
        pre_text = response.css("pre::text").get().strip()
        pre_text = pre_text.rstrip(" ,")

        try:
            products = json.loads(pre_text)
        except json.JSONDecodeError:
            self.logger.error("Json decode error")
            return
        for product in products:
            if product.get("price") is None:
                continue
            item = ProductItem()
            item["product_id"] = product["ID"]
            item["name"] = product["name"]
            item["price"] = product["price"].get("withCard", 0)
            if item["price"] == 0:
                continue
            item["special_price"] = product["price"].get("withPeriod", 0)
            for item_property in product["properties"]:
                if isinstance(item_property.get("typeID"), int):
                    if item_property["typeID"] == 13:
                        item["manufacturer"] = item_property["name"]
                    if item_property["typeID"] == 15:
                        item["country"] = item_property["name"]
            try:
                validated_product = Product(**item)
                yield validated_product.model_dump()
            except ValidationError as e:
                self.logger.error(f"Validation data error: {e}")
            yield item
