from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pause, datetime


itemidurl = "fullItemUrl"
maxbidebay = "6.00"
timeToBidSecs = 30

try:
    driver = webdriver.Firefox()

    #Find item url to get end time in ms
    driver.get(itemidurl)
    time.sleep(3)
    endTimeAttr = driver.find_element_by_class_name("timeMs")
    endTimeMs = endTimeAttr.get_attribute("timems")
    print ("End time in ms: " + str(endTimeMs))
    bidTime = int(endTimeMs) - 30*1000
    #endTime = time(bidTime)
    print("Bid time: " + str(bidTime))

    bidTime = bidTime/1000
    ts = datetime.datetime.fromtimestamp(bidTime).strftime('%Y-%m-%d %H:%M:%S')
    print ("Sleeping until bid time: " + str(ts))
    driver.quit()
    dt = datetime.datetime.fromtimestamp(bidTime)
    pause.until(dt)

    #Wake up and start the bid
    driver = webdriver.Firefox()
    driver.get('https://signin.ebay.com/ws/eBayISAPI.dll')

    time.sleep(3)
    elements = driver.find_elements_by_class_name("fld")
    elements[2].send_keys("username")
    elements[3].send_keys("pwd")

    time.sleep(3)
    button = driver.find_element_by_id("sgnBt")
    button.click()

    time.sleep(2)
    driver.get(itemidurl)

    time.sleep(3)
    elements = driver.find_element_by_id("MaxBidId")
    elements.send_keys(maxbidebay)
    elements = driver.find_element_by_id("bidBtn_btn")
    elements.click()

    time.sleep(3)
    io = driver.find_element_by_id("confirm_button")
    io.click()

    time.sleep(20)
except Exception as e:
    print ("Error caught: " + str(e))
finally:
    driver.quit()