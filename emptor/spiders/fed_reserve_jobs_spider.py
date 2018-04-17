import urllib
import scrapy


class FedReserveJobsSpider(scrapy.Spider):
    name = "fed_reserve_jobs"

    def start_requests(self):
        base_url = "https://www.federalreserve.gov/start-job-search.htm"
        yield scrapy.Request(url=base_url, callback=self.parse)

    def parse(self, response):
        iframe_src_url = response.xpath('//iframe[@class = "embed-responsive-item"]/@src').extract_first()
        yield scrapy.Request(url=iframe_src_url, callback=self.parse_iframe)

    def parse_iframe(self, response):
        data = {}
        jobFieldMapping = self.get_job_field_id(response.xpath('//*[@id="advancedSearchInterface.jobfield1L1"]/option'))
        if hasattr(self, 'keywords'):
            data['keyword'] = self.keywords
        if hasattr(self, 'category'):
            if self.category in jobFieldMapping.keys():
                data['jobfield1'] = jobFieldMapping[self.category]
            else:
                print("Invalid Category")

        yield scrapy.FormRequest(url=response.url, formdata=data, callback=self.parse_data,dont_filter=True)

    def parse_data(self, response):
        response_data = response.xpath('//*[@id="initialHistory"]/@value').extract_first()
        formatted_response = urllib.parse.unquote(response_data).split("!$!")[2].split("!|!")
        display_result(formatted_response)

    def get_job_field_id(self, category):
        item = {}
        for ar in category:
            item[str(ar.xpath('text()').extract()[0].strip())] = str(ar.xpath('@value').extract()[0].strip())
        return item


def display_result(formatted_response):
    print("****************** DATA CRAWLED ******************")
    for i in range(0, int(len(formatted_response) / 38)):
        print("\nJob Title : " + formatted_response[7 + (i * 38)])
        print("Location : " + formatted_response[10 + (i * 38)])
        print("Posting Date : " + formatted_response[16 + (i * 38)])
    print("\n****************** END OF DATA ******************")
