import argparse
import logging
import random
import sys
import signal
import time

from contextlib import contextmanager

import selenium.common.exceptions

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver


logger = logging.getLogger('libserpy')


USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"


class SearchException(Exception): pass


def driver_class(name="chrome"):
    mod = getattr(webdriver, name, None)
    if not mod:
        raise SearchException('Selenium driver not found')
    return mod.webdriver.WebDriver


def wait_for_results(driver):
    WebDriverWait(driver, 100).until(
        lambda driver:
        driver.execute_script("return document.readyState === 'complete';")
    )


def random_wait():
    time.sleep(random.random() * random.random() * 2)


@contextmanager
def driver_ctx(name="chrome", **kwargs):
    cls = driver_class(name)
    driver = cls(**kwargs)
    driver.set_window_size(1400, 1000)
    try:
        yield driver
    finally:
        driver.close()
        driver.service.process.send_signal(signal.SIGKILL)
        driver.quit()


def gather_link_info(driver):
    links = []
    for result_div in driver.find_elements_by_xpath('//h3[@class=\'r\']'):
        try:
            link = result_div.find_element_by_tag_name('a')
        except:
            logger.exception("Exception retreiving search result links")
            continue
        href_text = link.get_attribute('href')
        logger.debug("Found link: %s", href_text)
        links.append((link.text, href_text,))
    return links


def search4(search_phrase):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # Use Chrome User Agent
    dcap["phantomjs.page.settings.userAgent"] = USER_AGENT
    #with driver_ctx() as driver:
    with driver_ctx('phantomjs', desired_capabilities=dcap, service_args=['--debug=yes']) as driver:
        driver.get('https://www.google.com')
        wait_for_results(driver)
        source = driver.page_source
        links = []
        #source = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        soup = BeautifulSoup(source, 'html.parser')
        try:
            search_input = driver.find_element_by_xpath('//input[@aria-label=\'Search\']')
        except selenium.common.exceptions.NoSuchElementException as exc:
            driver.save_screenshot('err.png')
            raise
        search_input.send_keys(search_phrase)
        search_buton = driver.find_element_by_xpath('//input[@aria-label=\'Google Search\']')
        search_buton.click()
        wait_for_results(driver)
        while True:
            links.extend(gather_link_info(driver))
            try:
                next_link = driver.find_element_by_xpath('//a[@id=\'pnnext\']')
            except selenium.common.exceptions.NoSuchElementException as exc:
                next_link = None
            if not next_link:
                break
            next_link.click()
            logger.debug('Sleep some...')
            random_wait()
        driver.save_screenshot('sucess.png')
        return links


def match_filter(filter, href):
    return href.find(filter) != -1


def main():
    logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='Search query')
    parser.add_argument('--filter', help='filter')
    ns = parser.parse_args()
    links = search4(ns.query)
    for n, (test, href,) in enumerate(links):
        if ns.filter and not match_filter(ns.filter, href):
            continue
        print(n, test, href)


if __name__ == '__main__':
    main()
