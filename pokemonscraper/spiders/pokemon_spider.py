import scrapy
from pokemonscraper.items import PokemonscraperItem

class PokemonSpiderSpider(scrapy.Spider):
    name = "pokemon_spider"
    allowed_domains = ["scrapeme.live"]
    start_urls = ["https://scrapeme.live/shop/"]

    def parse(self, response):
        pokemons = response.css('li.product-type-simple')
        for pokemon in pokemons:

            pokemon_page_url = pokemon.css('a::attr(href)').get()
            if pokemon_page_url is not None:
                yield response.follow(pokemon_page_url, callback= self.pokemon_parse)
        li_tags = response.css('a.page-numbers::attr(href)')
        next_page = li_tags[-1].get()

        if next_page is not None:
            yield response.follow(next_page, callback= self.parse)

    def pokemon_parse(self, response):
        item = PokemonscraperItem()
        item["name"] = response.css('h1.entry-title ::text').get()
        item["price"] = response.xpath('//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/text()').get()
        item["in_stock"] = response.css('p.in-stock::text').get()
        item["Weight"] = response.css('td.product_weight::text').get()
        item["Dimensions"] = response.css('td.product_dimensions::text').get()
        yield item

        
