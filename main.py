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

# Returns list of rows
def get_reports_meta():
    with open("trips_meta.csv", "r") as f:
        csv_reader = csv.reader(f)
        return list(csv_reader)

def get_dose_chart(page_content):
    output = []
    page = html.fromstring(page_content)
    dose_table = page.xpath("//table[@class='dosechart']/tbody/tr")
    for dose_timestamp in dose_table:
        dose_object = {}
        dose_entry = dose_timestamp.xpath(".//td")
        dose_object["time"] = dose_entry[0].text.encode("ascii", "ignore").decode("utf-8")
        dose_object["amount"] = dose_entry[1].text
        dose_object["ingestion_method"] = dose_entry[2].text
        dose_object["substance"] = dose_entry[3].text
        try:
            dose_object["ingestion_form"] = dose_entry[4].text
        except:
            dose_object["ingestion_form"] = "N/A"
        output += [dose_object]

    return output

def get_bodyweight(page_content):
    page = html.fromstring(page_content)
    body_weight = "N/A"
    try:
        body_weight = page.xpath("//td[@class='bodyweight-amount']/text()")[0]
    except:
        pass
    return body_weight

def get_exp_year(page_content):
    page = html.fromstring(page_content)
    exp_year = "N/A"
    try:
        exp_year_tr = page.xpath("//table[@class='footdata']/tbody/tr/td/text()")[0]
        exp_year = exp_year_tr[10:]
    except:
        pass
    return exp_year

def get_trip_report(page_content):
    page = html.fromstring(page_content)
    report_text = "N/A"
    try:
        report_text = page.xpath("//div[@class='report-text-surround']/text()")
        report_text = ''.join(report_text).strip()
    except:
        pass
    return report_text

def get_author_gender(page_content):
    page = html.fromstring(page_content)
    author_gender = "N/A"
    try:
        author_gender_tr = page.xpath("//table[@class='footdata']/tbody/tr/td/text()")[2]
        author_gender = author_gender_tr[8:]
    except:
        pass
    return author_gender

def get_age_at_exp(page_content):
    page = html.fromstring(page_content)
    age_at_exp = "N/A"
    try:
        age_at_exp_tr = page.xpath("//table[@class='footdata']/tbody/tr/td/text()")[4]
        age_at_exp = age_at_exp_tr[27:]
    except:
        pass
    return age_at_exp

def get_report_info(row):
    title = row[0]
    url = row[1]
    author = row[2]
    substance = row[3]
    pub_date = row[4]
    browser.get(url)
    page_content = browser.page_source
    dose_chart = get_dose_chart(page_content)
    body_weight = get_bodyweight(page_content)
    exp_year = get_exp_year(page_content)
    report = get_trip_report(page_content)
    gender = get_author_gender(page_content)
    age_at_exp = get_age_at_exp(page_content)

    return [
        title,
        url,
        author,
        gender,
        body_weight,
        age_at_exp,
        exp_year,
        pub_date,
        substance,
        dose_chart,
        report
    ]

def get_reports():
    report_objects = []
    meta = get_reports_meta()
    first_row = True
    counter = 0
    total = len(meta)
    for report_meta in meta:
        if first_row:
            first_row = False
            continue
        sleep(1)
        report_info = get_report_info(report_meta)
        report_objects += [report_info]
        counter += 1
        print("Did " + str(counter) + " / " + str(total))
    
    with open("trips.csv", "w") as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["title", "url", "author", "gender", "body weight", "age during experience", "experience year", "publication date", "substance", "dose chart", "report"])
        for thing in report_objects:
            csv_writer.writerow(thing)

get_reports()
browser.close()