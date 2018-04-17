
For the following site: https://www.federalreserve.gov/start-job-search.htm created a spider that can be executed from command line, takes an input, returns all items and can accept the following arguments:
- No argument<br />
- Keywords<br />
- Job category

# Example

scrapy crawl fed_reserve_jobs -a keywords=student -a category=Interns
Requirements
- Python
- Scrapy
