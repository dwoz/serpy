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
random.seed()


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
    i = 0 # random.randint(1, 3)
    return i + (random.random() * random.random() * 2)


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

class EngineDriver(object):

    def __init__(self, driver):
        self.driver = driver

class GoogleEngine(EngineDriver):

    initial_page_url = 'https://www.google.com'
    def load_search_page(self):
        logger.debug("Initial request to %s", self.initial_page_url)
        self.driver.get(self.initial_page_url)
        wait_for_results(self.driver)

    def enter_search_query(self, query):
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            search_input = self.driver.find_element_by_xpath('//input[@aria-label=\'Search\']')
        except selenium.common.exceptions.NoSuchElementException as exc:
            self.driver.save_screenshot('err.png')
            raise
        search_input.send_keys(query)

    def submit_search(self):
        search_button = self.driver.find_element_by_xpath('//input[@aria-label=\'Google Search\']')
        search_button.click()
        wait_for_results(self.driver)

    def gather_link_info(self):
        links = []
        for result_div in self.driver.find_elements_by_xpath('//h3[@class=\'r\']'):
            try:
                link = result_div.find_element_by_tag_name('a')
            except:
                logger.exception("Exception retreiving search result links")
                continue
            href_text = link.get_attribute('href')
            logger.debug("Found link: %s", href_text)
            yield link.text, href_text

    def _get_next_page_link(self):
        try:
            return self.driver.find_element_by_xpath('//a[@id=\'pnnext\']')
        except selenium.common.exceptions.NoSuchElementException as exc:
            return None

    def has_next_page(self):
        return self._get_next_page_link() is not None

    def load_next_page(self):
        self._get_next_page_link().click()


class SearchRunner(object):

    def __init__(self, phrase, engine, driver_name='phantomjs', driver_kwargs=None):
        self.phrase = phrase
        self.engine = engine
        self.driver_name = driver_name
        self.driver_kwargs = driver_kwargs or {}

    def gather_link_info(self, driver):
        links = []
        for result_div in driver.find_elements_by_xpath('//h3[@class=\'r\']'):
            try:
                link = result_div.find_element_by_tag_name('a')
            except:
                logger.exception("Exception retreiving search result links")
                continue
            href_text = link.get_attribute('href')
            logger.debug("Found link: %s", href_text)
            yield link.text, href_text

    def search(self, limit=0):
        with driver_ctx(self.driver_name, **self.driver_kwargs) as driver:
            engine = self.engine(driver)
            engine.load_search_page()
            engine.enter_search_query(self.phrase)
            engine.submit_search()

            count = 0
            def should_stop():
                return limit > 0 and count > limit

            while True:
                logger.debug("Parse results page")
                for href, txt in engine.gather_link_info():
                    count += 1
                    yield txt, href
                    if should_stop():
                        break
                if should_stop():
                    break
                if not engine.has_next_page():
                    break
                time.sleep(random_wait())
                engine.load_next_page()
                time.sleep(random_wait())
                logger.debug('Load next page by clicking next')
            logger.debug('Save screenshot of last page')
            driver.save_screenshot('sucess.png')


def main():
    logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', default=0, type=int, help='Stop after this number of results')
    parser.add_argument('--driver', default='phantomjs', help='Web driver to use')
    ns = parser.parse_args()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    if ns.driver == 'phantomjs':
        # Use Chrome User Agent
        dcap["phantomjs.page.settings.userAgent"] = USER_AGENT
        kwargs = {
            'desired_capabilities': dcap,
            'service_args': ['--debug=yes'],
        }
    else:
        kwargs = {}
    searcher = SearchRunner(ns.query, GoogleEngine, driver_name=ns.driver, driver_kwargs=kwargs)
    for test, href in searcher.search(ns.limit):
        print(test, href)


if __name__ == '__main__':
    main()
