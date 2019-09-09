import argparse
from selenium import webdriver
import time
import pause, datetime

ITEM_URL = "Test"
MAX_BID = "5.00"
TIME_TO_BID_SECS = 45

def usage():
    parser = argparse.ArgumentParser(
        description='Ebay Sniper script to bid on item at the last minute')
    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        help="This will turn on detailed logging from the program.")
    parser.add_argument("-t", "--timeToBid",
                        dest="timeToBid",
                        help="Number of seconds before auction end to wake up and bid. At minimum set to 30s")
    parser.add_argument("-i", "--itemUrl",
                        dest="itemUrl",
                        required=True,
                        help="The complete url to the item you want to bid on.")
    parser.add_argument("-b", "--maxBid",
                        dest="maxBid",
                        required=True,
                        help="The maximum bid you want to place on the item")
    parser.add_argument("-u", "--username",
                        dest="userName",
                        required=True,
                        help="Your Ebay Username")
    parser.add_argument("-p", "--pwd",
                        dest="passWord",
                        required=True,
                        help="Your Ebay Password")
    parser.set_defaults(verbose=False, timeToBid=45)
    args = parser.parse_args()

    return args

def main():
    params = usage()

    USER_NAME = params.userName
    PWD = params.passWord
    TIME_TO_BID_SECS = params.timeToBid
    ITEM_URL = params.itemUrl
    MAX_BID = params.maxBid

    driver = None

    try:
        driver = webdriver.Firefox()

        #Find item url to get end time in ms
        driver.get(ITEM_URL)
        time.sleep(3)
        endTimeAttr = driver.find_element_by_class_name("timeMs")
        endTimeMs = endTimeAttr.get_attribute("timems")

        if params.verbose:
            print ("End time in ms: " + str(endTimeMs))

        bidTime = int(endTimeMs) - TIME_TO_BID_SECS*1000

        if params.verbose:
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

if __name__ == '__main__': main()
