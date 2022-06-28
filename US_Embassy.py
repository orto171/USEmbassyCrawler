from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from os import path
import time
from datetime import datetime, timedelta


def try_reschedule(browser, city):

    select = select_appointment_location(browser)
    select_city_value(city, select)
    get_available_dates(browser)

    next_two_months = ["ui-datepicker-group ui-datepicker-group-first", "ui-datepicker-group ui-datepicker-group-last"]
    for month in next_two_months:
        month_element = get_month_element(browser, month)

        try:
            find_available_spots(browser, month_element)
            select_earlieat_available_spot(browser)
            return 'SUCCESS'

        except Exception as e:
            raise e


def select_earlieat_available_spot(browser):
    Select(browser.find_element_by_id("appointments[consulate_appointment][time]")).select_by_index(1)
    browser.find_element_by_id("appointments_submit").click()
    browser.find_element_by_css_selector("a.button.alert").click()


def find_available_spots(browser, month_element):
    month_element.find_element_by_class_name(" undefined").click()
    browser.find_element_by_id("appointments_consulate_appointment_time_input").click()


def get_month_element(browser, month):
    element_wrapper = browser.find_element_by_xpath("//*[@class='" + month + "']")
    return element_wrapper.find_element_by_class_name("ui-datepicker-calendar")


def get_available_dates(browser):
    try:
        browser.find_element_by_id("appointments_consulate_appointment_date_input").click()
    except:
        return 'FAILURE - There are no available dates at all for this city'


def select_city_value(city, select):
    if city == 'Jerusalem':
        select.select_by_value('97')
    else:
        select.select_by_value('96')


def select_appointment_location(browser):
    select = Select(browser.find_element_by_id("appointments_consulate_appointment_facility_id"))
    return select


def crawl(username, password):

    browser = get_chrome_browser()
    log_in(browser=browser, username=username, password=password)
    enter_reschedule_page(browser)

    now = datetime.now()
    while now < datetime.now() + timedelta(hours=5):
        if try_reschedule(browser, city='Jerusalem') == 'SUCCESS':
            print("New interview meeting was successfully set in Jerusalem embassy")
            break
        if try_reschedule(browser, city='Tel Aviv') == 'SUCCESS':
            print("New interview meeting was successfully set in Tel Aviv embassy")
            break
        sleep(seconds=60)
        browser.refresh()


def enter_reschedule_page(browser):
    browser.find_element_by_xpath('//a[@href="' + "/he-il/niv/schedule/35170054/continue_actions" + '"]').click()
    browser.find_element_by_xpath("(//li[@class='accordion-item'])[3]").click()
    sleep(seconds=2)
    browser.find_element_by_xpath('//a[@href="' + "/he-il/niv/schedule/35170054/appointment" + '"]').click()


def log_in(browser, username, password):
    browser.get('https://ais.usvisa-info.com/he-il/niv/users/sign_in')
    enter_user_details(browser, password, username)
    confirm_policy(browser)
    browser.find_element_by_name("commit").click()
    sleep(seconds=2)


def confirm_policy(browser):
    actions = ActionChains(browser)
    actions.move_to_element(browser.find_element_by_id("policy_confirmed")).click().perform()


def enter_user_details(browser, username, password):
    browser.find_element_by_id("user_email").send_keys(username)
    browser.find_element_by_id("user_password").send_keys(password)


def get_chrome_browser():
    return webdriver.Chrome(path.join(path.dirname(path.realpath(__file__)), "chromedriver.exe"))


def sleep(seconds):
    time.sleep(seconds)


def main():

    embassy_website_username = "XXXXXXX"
    embassy_website_password = "XXXXXXX"

    try:
        crawl(username=embassy_website_username, password=embassy_website_password)
    except Exception as e:
        print("Exception was thrown during the process: " + str(e))


if __name__ == '__main__':
    main()
