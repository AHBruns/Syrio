from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import sqlite3
import time
import sys


def main():
    conf = json.load(open("config.json", "r"))
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = None
    while driver is None:
        try:
            driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
        except Exception as ex:
            print(ex)
    print(">> getting website")
    driver.get("https://coinmarketcap.com/all/views/all/")
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    while True:
        print(">> got website")
        query_time = time.time()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "total-marketcap")))
        table_el = driver.find_element_by_tag_name("tbody")
        line_els = table_el.find_elements_by_tag_name("tr")
        for line_el in line_els:
            tds = line_el.find_elements_by_tag_name("td")
            market_caps = line_el.find_element_by_class_name("market-cap")
            index = tds[0].text
            name = line_el.find_element_by_class_name("currency-name").get_attribute("data-sort")
            ticker = line_el.find_element_by_class_name("col-symbol").text
            usd_market_cap = market_caps.get_attribute("data-usd")
            btc_market_cap = market_caps.get_attribute("data-btc")
            circulating_supply = tds[5].get_attribute("data-sort")
            volume_24h = tds[6].get_attribute("data-sort")
            change_1h = tds[7].get_attribute("data-sort")
            change_24h = tds[8].get_attribute("data-sort")
            change_7d = tds[9].get_attribute("data-sort")
            print_str = "{} | {} | {} | ${} | Ƀ{} | {} | {} | {} | {} | {}".format(
                index,
                name,
                ticker,
                usd_market_cap,
                btc_market_cap,
                circulating_supply,
                volume_24h,
                change_1h,
                change_24h,
                change_7d)
            print(print_str)
            if usd_market_cap == "?":
                usd_market_cap = -1.0
            if btc_market_cap == "?":
                btc_market_cap = -1.0
            if volume_24h == "?":
                volume_24h = -1.0
            if change_1h == "?":
                change_1h = -1.0
            if change_24h == "?":
                change_24h = -1.0
            if change_7d == "?":
                change_7d = -1.0
            s = """INSERT INTO """ + """_{}""".format(int(index))\
                + """ VALUES ({}, \"{}\", \"{}\", {}, {}, {}, {}, {}, {}, {})""".format(
                int(query_time),
                name,
                ticker,
                float(usd_market_cap),
                float(btc_market_cap),
                float(circulating_supply),
                float(volume_24h),
                float(change_1h),
                float(change_24h),
                float(change_7d))
            print("s: {}".format(s))
            try:
                c.execute(s)
            except sqlite3.OperationalError as ex:
                print(ex)
            c.fetchall()
            c.execute("""SELECT * FROM _{}""".format(int(index)))
            print(c.fetchall())
            conn.commit()
        print(">> getting website")
        driver.refresh()


if __name__ == "__main__":
    main()
