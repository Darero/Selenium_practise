import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def browser():
    print('\nStarting browser...')
    browser = webdriver.Chrome()
    browser.set_window_size(1600, 900)
    browser.implicitly_wait(5)
    yield browser
    print('\nQuitting browser')
    browser.quit()


class TestSearchBar:
    url = 'https://www.dns-shop.ru/'
    searchbar_selector = '#header-search [placeholder=\'Поиск по сайту\']'
    good_name = 'Bosch GSR 18V-50 Professional 06019H5020'
    good_article = 8173241
    expected_link = 'https://www.dns-shop.ru/product/f3edd3959b033330/drel-surupovert-bosch-gsr-18v-50-professional-06019h5020-li-ion-18v/'
    category = 'Компьютеры'
    category_link = 'https://www.dns-shop.ru/catalog/17a8932c16404e77/personalnye-kompyutery/'

    def initiate_searching(self, test_browser, value):
        # print('Beginning search...')
        test_browser.get(self.url)
        searchbar = test_browser.find_element(By.CSS_SELECTOR, self.searchbar_selector)
        searchbar.send_keys(value)
        searchbar.send_keys(Keys.ENTER)
        # print('Search complete...')
        return test_browser

    def test_finding_good_by_name(self, browser):
        # print('Performing search by name test...')
        self.initiate_searching(browser, self.good_name)
        assert browser.current_url == self.expected_link

    def test_finding_good_by_article(self, browser):
        # print('Performing search by article test...')
        self.initiate_searching(browser, self.good_article)
        assert browser.current_url == self.expected_link

    def test_should_lead_to_defined_category(self, browser):
        # print('Performing category search test')
        self.initiate_searching(browser, self.category)
        page_h1 = browser.find_element(By.CSS_SELECTOR, 'h1.title').text
        assert self.category_link in browser.current_url and \
               self.category.lower()[:-2] in page_h1.lower() and \
               'категориях' not in page_h1.lower()

    @pytest.mark.xfail
    def test_should_not_lead_to_defined_catefory(self, browser):
        self.initiate_searching(browser, 'Часы')
        page_h1 = browser.find_element(By.CSS_SELECTOR, 'h1.title').text
        assert 'категориях' not in page_h1.lower() or 'часы' in page_h1.lower()


