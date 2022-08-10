import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def cart_checkout_asserts(browser):
    # проверка названия и цены в корзине и на странице оплаты (одинаковые селекторы)
    assert browser.find_element(By.CLASS_NAME, 'inventory_item_name').text == goods_dict[item_num]['name']
    assert browser.find_element(By.CLASS_NAME, 'inventory_item_price').text.strip().replace(' ', '') == \
           goods_dict[item_num]['price']
    return browser


goods_dict = {'1': {'name': 'Sauce Labs Backpack', 'ID': 'item_4_title_link', 'price': '$29.99'},
              '2': {'name': 'Sauce Labs Bike Light', 'ID': 'item_0_title_link', 'price': '$9.99'},
              '3': {'name': 'Sauce Labs Bolt T-Shirt', 'ID': 'item_1_title_link', 'price': '$15.99'},
              '4': {'name': 'Sauce Labs Fleece Jacket', 'ID': 'item_5_title_link', 'price': '$49.99'},
              '5': {'name': 'Sauce Labs Onesie', 'ID': 'item_2_title_link', 'price': '$7.99'},
              '6': {'name': 'Test.allTheThings() T-Shirt (Red)', 'ID': 'item_3_title_link', 'price': '$15.99'}}

print('Приветствуем в нашем магазине!')
print('Пожалуйста, выберите один из следующих товаров по номеру для продолжения покупки:')
for good_num, good_values in goods_dict.items():
    print(f'{good_num}: {good_values["name"]}, цена - {good_values["price"]}')  # Приветствие и вывод имеющихся товаров

item_num = None
while item_num not in goods_dict.keys():
    item_num = input('\nДля продолжения введите номер: ')
    if item_num in goods_dict.keys():
        break
    print('Вы ввели неверное значение, пожалуйста введите заново')  # обработка неверных значений item_num

print('Запускаю браузер...')
browser = webdriver.Chrome()
browser.set_window_size(1600, 900)
browser.implicitly_wait(5)
browser.get('https://www.saucedemo.com/')
# Вход в систему
print('Вхожу в систему..')
browser.find_element(By.ID, 'user-name').send_keys('standard_user')
browser.find_element(By.ID, 'password').send_keys('secret_sauce')
browser.find_element(By.ID, 'login-button').click()

assert browser.current_url == 'https://www.saucedemo.com/inventory.html'  # Проверяем, что перешли в каталог
print('Вход в систему выполнен успешно..')

browser.find_element(By.ID, goods_dict[item_num]['ID']).click()  # Находим нужный товар по значениям из словаря
print('Перехожу на страницу товара..')

assert browser.find_element(By.CLASS_NAME, 'inventory_details_name').text == goods_dict[item_num]['name']
# сверяем название и цену товара на совпадение в словаре
assert browser.find_element(By.CLASS_NAME, 'inventory_details_price').text.strip().replace(' ', '') == \
       goods_dict[item_num]['price']

print('Товар выбран верно, добавляю в корзину..')

add_to_cart = browser.find_element(By.CSS_SELECTOR, '.inventory_details_desc_container button')
add_to_cart.click()  # находим кнопку добавления в корзину и нажимаем

print('Перехожу в корзину..')

browser.find_element(By.CLASS_NAME, 'shopping_cart_link').click()  # переходим в корзину

assert browser.current_url == 'https://www.saucedemo.com/cart.html'  # проверяем, что перешли в корзину

print('Выполнен переход в корзину, сверяю товар..')

cart_checkout_asserts(browser)  # сверяем название + цену

print('Сверка прошла успешно, перехожу на страницу оформления доставки..')

browser.find_element(By.ID, 'checkout').click() # переходим в оплату

assert browser.current_url == 'https://www.saucedemo.com/checkout-step-one.html'  # сверяем переход

print('Успешно, начинаю заполнение полей и переход на страницу оплаты..')

browser.find_element(By.XPATH, '//*[@id="first-name"]').send_keys("123")  # input('Введите ваше Имя: '))
browser.find_element(By.XPATH, '//*[@id="last-name"]').send_keys("123")  # input('Введите вашу Фамилию: '))
browser.find_element(By.XPATH, '//*[@id="postal-code"]').send_keys("123")  # input('Введите почтовый : '))
browser.find_element(By.XPATH, '//*[@id="continue"]').click()  # заполняем фамилию, имя и индекс, переходим далее

assert browser.current_url == 'https://www.saucedemo.com/checkout-step-two.html'  # сверяем переход

print('Сверяю цену и название товара..')

cart_checkout_asserts(browser)  # сверяем название + цену

float_price = float(goods_dict[item_num]['price'].replace('$', ''))
tax_price = round(float_price * 0.08, 2)
total_price = f'Total: ${str(round(float_price + tax_price, 2))}'  # высчитываем налог и итоговую цену
print(f'Ожидаемая итоговая цена: {total_price.replace("Total: ", "")}')

assert browser.find_element(By.CLASS_NAME,
                            'summary_total_label').text == total_price  # сверяем высчитанную итоговую цену с подсчитанной сайтом

print('Цены совпали, завершаю оплату..')

browser.find_element(By.ID, 'finish').click()

assert browser.current_url == 'https://www.saucedemo.com/checkout-complete.html'
print('Оплата завершена успешно...')
browser.close()
