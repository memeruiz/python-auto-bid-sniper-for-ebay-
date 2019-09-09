# Python script to auto bid on ebay 

# Installation

## Selenium
pip3 install selenium

## Pause
pip3 install pause

## Install gecko driver
Go to: https://github.com/mozilla/geckodriver/releases
Find correct driver for your OS

Install the executable and put it in your PATH
i.e.  export PATH="path_to_geckodriver_dir:$PATH"


###### Example
python3 ebaysniper.py -b 5.00 -u myusername -p mypwd -i https://www.ebay.com/itm/full-item-url

