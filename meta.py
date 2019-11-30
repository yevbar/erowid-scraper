import csv
from lxml import html
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
# Uncomment the following line to run in headless mode
# options.headless = True
browser = webdriver.Firefox(options=options)
reports = []

search_url = "https://erowid.org/experiences/exp.cgi?Cellar=1&ShowViews=0&Cellar=1&Start=1&Max=35925"
xpath_query = '//*[@id="results-form"]/table/tbody/tr[not(@height)]'
next_button_query = '//a/img'

def get_reports_objects(page_content):
    global reports
    page = html.fromstring(page_content)
    current_reports = page.xpath(xpath_query)
    for report in current_reports:
        columns = report.xpath(".//td")
        report_title = columns[1].xpath(".//a/text()")[0]
        report_href = columns[1].xpath(".//a/@href")[0]
        report_object = {
            "title": report_title,
            "url": report_href,
            "author": columns[2].text,
            "substance": columns[3].text,
            "pub_date": columns[4].text
        }
        reports += [report_object]

def get_reports():
    print("Sleeping")
    sleep(2)
    print("Now we're rocking")
    get_reports_objects(browser.page_source)

    try:
        next_button = browser.find_elements_by_xpath(next_button_query)[0]
        next_button.click()
        get_reports()
    except:
        pass

browser.get(search_url)
get_reports()
with open("trips_meta.csv", "w") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["title", "url", "author", "substance", "pub_date"])
    for report in reports:
        csv_writer.writerow([report["title"], "https://erowid.org/experiences/" + report["url"], report["author"], report["substance"], report["pub_date"]])
browser.close()
