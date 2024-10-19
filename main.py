import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

default_types_ids = [
    400228,
    396070,
    396194,
    398631,
    398611,
    400221,
    396198,
    400010,
    400217,
    400226,
    398511,
    398830,
    400232,
    400224,
    400227,
    400229,
]

def run_spider(city_ids):
    process = CrawlerProcess(get_project_settings())
    process.crawl('products', city_ids=city_ids, type_ids=default_types_ids)
    process.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apteka April Parser')
    parser.add_argument('-c', '--city_ids', nargs='+', help='List of city IDs', required=True)
    args = parser.parse_args()
    run_spider(args.city_ids)