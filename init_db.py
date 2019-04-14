import sqlite3
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()
c.execute("""CREATE TABLE currency2id (id INTEGER, currency TEXT)""")
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = None
while driver is None:
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as ex:
        print(ex)
driver.get("https://coinmarketcap.com/all/views/all/")
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "total-marketcap")))
table_el = driver.find_element_by_tag_name("tbody")
line_els = table_el.find_elements_by_tag_name("tr")
for line_el in line_els:
    tds = line_el.find_elements_by_tag_name("td")
    market_caps = line_el.find_element_by_class_name("market-cap")
    index = tds[0].text
    name = line_el.find_element_by_class_name("currency-name").get_attribute("data-sort")
    ticker = line_el.find_element_by_class_name("col-symbol").text
    c.execute("""INSERT INTO currency2id VALUES (?, ?)""", (int(index), name,))
    s = """CREATE TABLE """ + "_{}".format(int(index)) + """ (
      ts INTEGER,
      currency TEXT,
      ticker TEXT,
      usd_market_cap REAL,
      btc_market_cap REAL,
      circulating_supply REAL,
      volume_24h REAL,
      change_1h REAL,
      change_24h REAL,
      change_7d REAL)"""
    c.execute(s)
    conn.commit()
    c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    print(c.fetchall())
c.fetchall()
c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
print(c.fetchall())
conn.close()

