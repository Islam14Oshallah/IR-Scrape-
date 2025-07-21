import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

# Importing time libraries to add wait times
from datetime import datetime
from time import sleep
# Importing BeautifulSoup to read the page HTML source code
from bs4 import BeautifulSoup
# To create csv file where we'll scrape the content
import pandas as pd

# Initialize lists to store post data
name_list = []
pst_list = []
reply_list = []
image_list = []
date_list = []

# Adding options functionality to disable notifications
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

# Set up Chrome driver with the correct path and options
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=chrome_options)

driver.get("https://www.facebook.com")
driver.maximize_window()
sleep(2)

# Logging in
email = driver.find_element(By.ID, "email")
email.send_keys("d7ome195@icloud.com")
password = driver.find_element(By.ID, "pass")
password.send_keys("Seifa123")
login = driver.find_element(By.NAME, "login")
login.click()
sleep(1)
sleep(2)
driver.get("https://www.facebook.com/groups/3059922490730993")  # change group here
sleep(1)
y = 500
while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    all_posts = soup.find_all("div", {"class": "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"})
    for post in all_posts:
        #try:
            #name = post.find("strong", {"class": "html-strong xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs x1s688f"}).get_text()
        #except:
            #name = "Anonymous"


        try:
            pst = post.find("span", {"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"}).get_text()
        except:
            pst = "No Post"

        try:
            if pst == "No Post":
                pst = post.find("div", {"class": "x6s0dn4 x78zum5 xdt5ytf x5yr21d xl56j7k x10l6tqk x17qophe x13vifvy xh8yej3"}).get_text()
        except:
            pst = "No Post"


        try:
            reply = post.find("span", {"class": "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u"}).get_text()
        except:
            reply = "No Reply"


        try:
            image = post.find("div", {"class": "xqtp20y x6ikm8r x10wlt62 x1n2onr6"}).find("img")['src']
        except:
            image = "No Image"



        # Append new data to the lists
        #name_list.append(name)
        pst_list.append(pst)
        reply_list.append(reply)
        image_list.append(image)

    # Save data to DataFrame once per iteration, and avoid overwriting
    df = pd.DataFrame({"Post": pst_list, "Reply": reply_list, "Image": image_list})
    df.drop_duplicates(subset="Reply", keep="first", inplace=True)
    
    # Save to CSV after the loop finishes scraping new data
    df.to_csv("Medical_DataSet2.2.csv", index=False)
    
    # Stop scraping after collecting enough posts (e.g., more than 2 rows)
    if df.shape[0] > 10000:
        break

    # Scroll to load more posts
    
    for timer in range(0, 10):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 500
        sleep(0.35)

driver.quit()