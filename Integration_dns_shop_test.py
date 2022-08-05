import time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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

    def test_should_lead_to_defined_category(self, browser):  # APPLY TO SINGLE WORD CATEGORIES ONLY
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


class TestCart:
    url = 'https://www.dns-shop.ru/'
    goods_articles = {'notebook': 4874678, 'accessory': 1323034,
                      'bonuses': 4890553, 'online_payment': 4839637}
    searchbar_selector = '#header-search [placeholder=\'Поиск по сайту\']'

    def initiate_searching(self, test_browser, value):
        # print('Beginning search...')
        searchbar = test_browser.find_element(By.CSS_SELECTOR, self.searchbar_selector)
        searchbar.send_keys(value)
        searchbar.send_keys(Keys.ENTER)
        # print('Search complete...')
        return test_browser

    def test_all_goods_should_be_in_cart(self, browser):
        browser.get(self.url)
        for category, article in self.goods_articles.items():
            self.initiate_searching(browser, article)

            WebDriverWait(browser, 5).until(
                EC.all_of(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-card-top__buy .buy-btn')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.product-card-top__buy .buy-btn'))
                )
            )
            # WebDriverWait(browser, 10).until(
            #     EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-card-top__buy .buy-btn')))
            #
            # WebDriverWait(browser, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, '.product-card-top__buy .buy-btn')))
            browser.find_element(By.CSS_SELECTOR, '.product-card-top__buy .buy-btn').click()
            time.sleep(5)
        browser.find_element(By.CLASS_NAME, 'cart-link').click()
        articles = []
        for i in range(len(self.goods_articles)):
            article = browser.find_element(By.CSS_SELECTOR,
                                 f'div.cart-items__product:nth-child({2 + i}) .cart-items__product-code').text
            articles.append(article)
        assert all(map(lambda x: int(x) in self.goods_articles.values(), articles))
