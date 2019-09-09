from selenium import webdriver
import time
import pause, datetime


ITEM_URL = "https://www.ebay.com/itm/NYMPH-ASSORTMENT-136-flies-in-a-new-waterproof-fly-box/123886469909?hash=item1cd8358315:g:OlgAAOSw~6ddYtfw"
MAX_BID = "65.00"
TIME_TO_BID_SECS = 45
USER_NAME= "yourusername"
PWD="yourpwd"

driver = None

try:
    driver = webdriver.Firefox()

    #Find item url to get end time in ms
    driver.get(ITEM_URL)
    time.sleep(3)
    endTimeAttr = driver.find_element_by_class_name("timeMs")
    endTimeMs = endTimeAttr.get_attribute("timems")
    print ("End time in ms: " + str(endTimeMs))
    bidTime = int(endTimeMs) - TIME_TO_BID_SECS*1000
    #endTime = time(bidTime)
    print("Bid time: " + str(bidTime))

    #Convert to datetime understandable time from bidTime
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
    elements[2].send_keys(USER_NAME)
    elements[3].send_keys(PWD)

    time.sleep(3)
    button = driver.find_element_by_id("sgnBt")
    button.click()

    time.sleep(2)
    driver.get(ITEM_URL)

    time.sleep(3)
    elements = driver.find_element_by_id("MaxBidId")
    elements.send_keys(MAX_BID)
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