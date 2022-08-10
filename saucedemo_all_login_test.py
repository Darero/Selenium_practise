from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from random import choice, shuffle
import time


# На всякий случай добавлен несуществующий пользователь, для глючного пользователя явные ожидания не понадобились, ибо,
# как я понял, драйвер виснет намертво. Спасибо за квест!


class TestRegistrationForm:
    url = 'https://www.saucedemo.com/'
    users = ['standard_user', 'locked_out_user', 'problem_user', 'performance_glitch_user', 'wrong_user']
    password = 'secret_sauce'

    def start_class_browser(self):  # запускаем браузер
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1600, 900)

    def login_user(self, user):  # отдельный метод для заполнения полей
        assert self.browser.current_url == 'https://www.saucedemo.com/'
        print('Начинаю заполнение полей..')
        self.browser.find_element(By.ID, 'user-name').send_keys(user)
        self.browser.find_element(By.ID, 'password').send_keys(self.password)
        print('Поля заполнены, вхожу на сайт..')
        self.browser.find_element(By.ID, 'login-button').click()

    def test_user(self, username=None):  # отдельный метод для тестирования пользователя,
        self.start_class_browser()
        if username is None:  # если пользователь не указан - берется случайный из списка класса
            user = choice(self.users)
        else:
            user = username
        print(f'Инициирую проверку пользователя {username}')
        try:
            self.browser.get(self.url)
            self.start_time = time.time()  # запись времени для выявления проблемного пользователя
            self.login_user(user)
            self.browser.find_element(By.CLASS_NAME, 'title')  # проверка входа по титульнику страницы
            print('Вход на сайт произведен успешно, сканирую изображения')
            for i in range(6):  # сканирование изображений на сайте
                img = self.browser.find_element(By.CSS_SELECTOR, f'#item_{i}_img_link img')
                img_att = img.get_attribute('src')  # забираем атрибут src
                if img_att == 'https://www.saucedemo.com/static/media/sl-404.168b1cce.jpg':
                    return print(f'\nУ пользователя {user} возникла ошибка с изображением.')
            delta_time = time.time() - self.start_time  # вычисляем время входа на сайт
            print(f'Время входа на сайт: {round(delta_time, 2)} секунд')
            if delta_time > 4:
                return print(f'\nУ пользователя {user} обнаружена плохая производительность.')
            print(f'\nПользователь {user} отработал в штатном режиме')
        except NoSuchElementException:  # если упали в ошибку отсутствия элемента
            print('Не удалось войти на сайт')
            try:
                exception_text = self.browser.find_element(By.TAG_NAME, 'h3').text  # обрабатываем текст ошибки
                if exception_text == 'Epic sadface: Sorry, this user has been locked out.':
                    return print(f'\nИзвините, пользователь {user} заблокирован.')
                elif exception_text == 'Epic sadface: Username and password do not match any user in this service':
                    return print(f'\nИзвините, пользователя {user} не существует.')
                # else:
                #     WebDriverWait(self.browser, 6).until(EC.element_located_to_be_selected((By.CLASS_NAME, 'title')))
                #     delta_time = time.time() - self.start_time
                #     if delta_time > 4:
                #         return print(f'\nУ пользователя {user} обнаружено плохое интернет-соединение.')
                #     else:
            except Exception as e:
                print(f'\nВозникла непредвиденная ошибка {e}')  # на всякий случай
        finally:
            print('\nПроверка закончена, выхожу из браузера\n')
            self.browser.close()  # вместо фикстуры

    def test_all_users(self): # тестируем всех пользователей из списка класса
        temp_user_list = self.users[:] # на всякий случай копируем
        shuffle(temp_user_list) # перемешиваем на всякий случай
        for i in temp_user_list:
            self.test_user(i)
