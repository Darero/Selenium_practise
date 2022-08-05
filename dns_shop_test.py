from selenium import webdriver
from selenium.webdriver.common.by import By

# Тест-кейс: Проверка корректной работы добавления товаров в сравнение
# Среда тестирования - Google Chrome, v. 104.0.5112.81, 64-bit, OS Win10, ширина страницы от 992px
# Шаги теста:
# 1. Зайти на главную страницу DNS - https://www.dns-shop.ru/
# 2. Перейти в любую из подкатегорий (в выпадающем меню при наведении на категорию) товаров в меню слева,
# при наличии дополнительных подкатегорий - выбирать любые из них, до тех пор, пока не откроется каталог товаров
# 3. У любых двух товаров поставить галочку «Сравнить», запомнить названия товаров (без характеристик товара).
# 4. Перейти во вкладку «Сравнить» в голове страницы.
# Ожидаемый результат: названия товаров совпадают с добавленными в меню сравнения.

homepage = 'https://www.dns-shop.ru/'
browser = webdriver.Chrome()
browser.set_window_size(1600, 900)
browser.implicitly_wait(5)
browser.get(homepage)
browser.find_element(By.LINK_TEXT, 'ТВ и мультимедиа').click()

browser.find_element(By.CSS_SELECTOR, '.subcategory__item-container a:nth-child(1)').click()
browser.find_element(By.CSS_SELECTOR, '.subcategory__item-container a:nth-child(1)').click()

expected_names = []

for i in range(2):
    selector = f'.products-list__content .catalog-products:nth-child(2) div.catalog-product:nth-child({i + 1})'
    good_name = browser.find_element(By.CSS_SELECTOR, selector + ' .catalog-product__name span').text
    good_name = good_name[:good_name.find(' [')]
    browser.find_element(By.CSS_SELECTOR, selector + ' .compare-checkbox label').click()
    expected_names.append(good_name)

browser.find_element(By.CSS_SELECTOR, '.compare-link').click()

for i in range(2):
    selector = f'.products-slider__list .products-slider__item:nth-child({i + 1}) .products-slider__product-name a'
    received_name = browser.find_element(By.CSS_SELECTOR, selector).text
    assert received_name in expected_names, "Неверное название товара"

browser.quit()
