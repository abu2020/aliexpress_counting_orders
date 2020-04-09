# Aliexpress.com counting orders
This Python3 script will count all of your orders from aliexpress.com, separating received and cancelled orders.


## All things you have to do:
#1. download Python bindings for Selenium from the PyPI page for selenium package. However, a better approach would be to use pip to install the selenium package. Python 3.6 has pip available in the standard library. Using pip, you can install selenium like this:   
`my system: Linux (ubuntu 18.04)`

    sudo apt install python3-pip
    pip3 install selenium

#2. Selenium requires a driver to interface with the chosen browser:

	for google chrome:
	https://sites.google.com/a/chromium.org/chromedriver/downloads

	for firefox:
	https://github.com/mozilla/geckodriver/releases

	for safari:
	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

note: my preference is google chrome.

#3. move the downloaded file (chromedriver) or (geckodriver) in >> /usr/local/bin/

	mv ....driver /usr/local/bin/

##### Detailed instructions for Windows users:
https://selenium-python.readthedocs.io/installation.html



#### DONE.

Now run the script:

	python3 aliexpress_counting_orders.py

now just enter your username and password when prompted.

##### OR >> for much easier:

	python3 aliexpress_counting_orders.py("yourEmailAddress", "yourPassword")
	

#### I will appreciate any contribution to improve this script
