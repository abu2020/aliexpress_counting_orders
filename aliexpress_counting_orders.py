#!/usr/bin/python3
# coding: utf-8

from selenium import webdriver
from time import sleep, time

paids_total = 0
cancelled_total = 0
page_number = 1
all_lists = []
all_cancelled = []

def main(username=None, password=None):
    if username == None and password == None:
        username = input("please type your email: ")
        password = input("please type your password: ")

    #--------------------------------------------------------starting to browse
    t1 = time()
    long_loading_time = 4
    short_loading_time = 1.5
    try:
        print()
        print("please wait .............")
        driver = webdriver.Chrome()
        driver.delete_all_cookies()
        #driver.maximize_window()
        driver.get("https://login.aliexpress.com/")
        print("now entering into website ............")
        sleep(short_loading_time)

        #---------------------------------------------------------Sign In page
        try:
            signin = driver.find_element_by_xpath("//input[@name='fm-login-id']").send_keys(username)
            password_box = driver.find_element_by_xpath("//input[@name='fm-login-password']").send_keys(password)
            sleep(short_loading_time)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            print("now signing in ............")
            sleep(long_loading_time)
            print("successfully signed in ............")
        except:
            print("your username or password is incorrect")

        #---------------------------------------------------------going to my order page
        my_order = driver.find_element_by_xpath("//div[@id='user-benefits']/div[2]/div[3]/ul/li[2]/a/span[1]")
        my_order.click()
        print("now going to order list ...........")
        sleep(long_loading_time)

        checking_English = driver.find_element_by_xpath("//div[@id='appeal-alert']/h3").text
        if checking_English != "Orders":
            print("now, changing language to English")
            language = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[5]/a[@data-role='goto-globalsite']").click()
            sleep(long_loading_time)
            print("now, order list in English")
            my_order = driver.find_element_by_xpath("//div[@id='user-benefits']/div[2]/div[3]/ul/li[2]/a/span[1]").click()
            sleep(long_loading_time)

        #-------------------------------------------------------finding total page numbers
        all_pages_get = driver.find_element_by_xpath("//div[@id='simple-pager']/div/label")
        all_pages_str = all_pages_get.text
        all_pages_len = len(all_pages_str)
        if all_pages_len == 3:
            all_pages = all_pages_str[-1]
        else:
            all_pages = all_pages_str[-2:]
        print()
        print("Your total order pages >>", all_pages)
        print("normally each page has 10 items")
        print(40 * "_", "\n")

        #-------------------------------------------------------PAGES

        #-----------calling (list_of_prices)(total_of_page)(list_of_cancelled)(total_of_cancelled) variables
        #-----------calling variables from inside of another function
        def x():
            pass
        #-----------------------------------------------------
        def ending():
            print("list ----- ", x.list_of_prices)
            all_lists.append(x.list_of_prices)
            all_cancelled.append(x.total_of_cancelled)
            print("page", str(page_number).zfill(2)," > ", ("%.2f" %x.total_of_page), "USD")
            global paids_total
            paids_total += x.total_of_page
            global cancelled_total
            cancelled_total += x.total_of_cancelled
            print("Subtotal = ", "%.2f" %paids_total, "\n")

        #---------calling (price) variable depending on loop of parent
        def y():
            pass

        #------------------------------------------------------
        def calculation():
            if (y.status == "Awaiting delivery" or y.status == "Finished") and (y.received[:7] == "Confirm"):
                L_strip = y.price.lstrip("$ ")
                digital = float(L_strip)
                x.list_of_prices.append(digital)
                x.total_of_page += digital
            else:
                L_strip = y.price.lstrip("$ ")
                digital = float(L_strip)
                x.list_of_cancelled.append(digital)
                x.total_of_cancelled += digital

        #----------------------------------------------------
        def final_quote():
            print("Your confirm paid amount:  ", ("%.2f" %paids_total), "USD", "\n")
            print("and Cancelled paid amount: ", ("%.2f" %cancelled_total), "USD", "\n")
            TOTAL = float(paids_total) + float(cancelled_total)
            print("and your TOTAL transaction:", ("%.2f" %TOTAL), "USD")
            print((39 * "_"), "\n")

        #----------------------------------------------------
        def first_page():
            x.total_of_page = 0
            x.list_of_prices = []
            x.list_of_cancelled = []
            x.total_of_cancelled = 0
            for i in range(1,11):
                s_received = ("//table[@id='buyer-ordertable']/tbody[%i]/tr[2]/td[2]" %i)
                y.received = driver.find_element_by_xpath(s_received).text
                s_status = ("//table[@id='buyer-ordertable']/tbody[%i]/tr[2]/td[3]/span" %i)
                y.status = driver.find_element_by_xpath(s_status).text
                s_price = ("//table[@id='buyer-ordertable']/tbody[%i]/tr[1]/td[4]/div/p[2]" %i)
                y.price = driver.find_element_by_xpath(s_price).text
                calculation()
                last_item = driver.find_element_by_xpath("//table[@id='buyer-ordertable']/tbody[%i]" %i)
                last_item_attribute = last_item.get_attribute("class")
                if last_item_attribute == "order-item-wraper last-tbody":
                    break
            ending()
            if all_pages_str == "1/1":
                final_quote()
            else:
                sleep(short_loading_time)
                page_2 = ("//div[@id='simple-pager']/div/a")
                page_2 = driver.find_element_by_xpath(page_2).click()
                sleep(long_loading_time)
                driver.execute_script("window.scrollTo(0, 1000)")

        #----------------------------------------------------
        def middle_pages():
            global page_number
            for i in range(int(all_pages)-2):
                page_number += 1
                x.total_of_page = 0
                x.list_of_prices = []
                x.list_of_cancelled = []
                x.total_of_cancelled = 0
                for i in range(1,11):
                    s_received = ("//table[@id='buyer-ordertable']/tbody[%i]/tr[2]/td[2]" %i)
                    y.received = driver.find_element_by_xpath(s_received).text
                    s_status = ("//table[@id='buyer-ordertable']/tbody[%i]/tr[2]/td[3]/span" %i)
                    y.status = driver.find_element_by_xpath(s_status).text
                    s_price = ("//table[@id='buyer-ordertable']/tbody[%i]/tr[1]/td[4]/div[1]/p[2]" %i)
                    y.price = driver.find_element_by_xpath(s_price).text
                    calculation()
                ending()
                sleep(short_loading_time)
                page_n = ("//div[@id='simple-pager']/div/a[2]")
                page_n = driver.find_element_by_xpath(page_n).click()
                sleep(long_loading_time)
                driver.execute_script("window.scrollTo(0, 1000)")

        #-----------------------------------------------------
        def last_page():
            global page_number
            page_number += 1
            x.total_of_page = 0
            x.list_of_prices = []
            x.list_of_cancelled = []
            x.total_of_cancelled = 0
            for i in range(1,11):
                s_received = ("//table[@id='buyer-ordertable']/tbody[%i]/tr[2]/td[2]" %i)
                y.received = driver.find_element_by_xpath(s_received).text
                s_status = ("//table[@id='buyer-ordertable']/tbody[%i]/tr[2]/td[3]/span" %i)
                y.status = driver.find_element_by_xpath(s_status).text
                s_price = ("//table[@id='buyer-ordertable']/tbody[%i]/tr[1]/td[4]/div[1]/p[2]" %i)
                y.price = driver.find_element_by_xpath(s_price).text
                calculation()
                last_item = driver.find_element_by_xpath("//table[@id='buyer-ordertable']/tbody[%i]" %i)
                last_item_attribute = last_item.get_attribute("class")
                if last_item_attribute == "order-item-wraper last-tbody":
                    break
            ending()
            final_quote()

        #-----------------------------------------conditions based on pages quantity
        if all_pages_str == "1/1":
            first_page()
        elif all_pages_str == "1/2":
            first_page()
            last_page()
        else:
            first_page()
            middle_pages()
            last_page()

    except:
        print("please try again")
        driver.quit()

    t2 = time() - t1
    print("Processed time is  >> ", "%.2f" %t2, "seconds", "\n")
    driver.quit()

main()
