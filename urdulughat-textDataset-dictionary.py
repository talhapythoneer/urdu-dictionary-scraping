import scrapy
from scrapy.crawler import CrawlerProcess
import xlsxwriter

wb = xlsxwriter.Workbook("Urdu Dataset.xlsx")
ws = wb.add_worksheet()


class ScrapUrduWords(scrapy.Spider):
    name = "Urdu Dictionary Spider"
    c = 1

    def start_requests(self):
        for i in range(1, 110000):
            yield scrapy.Request(url="http://urdulughat.info/words/" + str(i), callback=self.parse)

    def parse(self, response):
        processedMeanings = []
        processedTranslations = []

        word = response.css("h2::text").extract_first()
        word = word.strip()
        pronunciation = response.css("div.name_with_inflictions > span::text").extract_first()
        language = response.css("div.language > div > span::text").extract_first()
        meanings = response.css("div.meaning-title::text").extract()
        translations = response.css("div#english-translations > ul > li::text").extract()

        for translation in translations: #Cleaning
            processedTranslations.append(translation.replace(" \xa0", " "))

        for meaning in meanings:  # Removing extra spaces from chapters
            processedMeanings.append(" ".join(meaning.split()))

        meanings = str(processedMeanings)  # Making a single string out of the
        translations = str(processedTranslations)

        print(self.c, "\t", word, "\t", pronunciation, "\t", language, "\t", meanings, "\t", translations)
        ws.write(self.c, 0, str(self.c))
        ws.write(self.c, 1, word)
        ws.write(self.c, 2, pronunciation)
        ws.write(self.c, 3, language)
        ws.write(self.c, 4, meanings)
        ws.write(self.c, 5, translations)
        self.c += 1


process = CrawlerProcess()
process.crawl(ScrapUrduWords)
process.start()
wb.close()
