import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

# Тест кейс = Проверка корректности алгоритма поиска YouTube
# Среда тестирования - Google Chrome, v. 104.0.5112.81, 64-bit, OS Win10
# Шаги теста:
# 1. Зайти на главную страницу YouTube https://www.youtube.com/
# 2. В поиской строке ввести «Star wars lofi» (регистр значения не имеет) и нажать кнопку поиска
# Ожидаемый результат: название первого видео в результатах поиска - Star Wars Lofi Hip Hop,
# название канала первого видео в результатах поиска - Closed on Sunday (привести значения к единому регистру)

browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('https://www.youtube.com/')
browser.find_element(By.CSS_SELECTOR, 'input#search').send_keys('lofi hip hop')
browser.find_element(By.CSS_SELECTOR, 'button#search-icon-legacy').click()
video_name = browser.find_element(By.CSS_SELECTOR,
                                  'ytd-video-renderer.ytd-item-section-renderer:nth-child(1) #video-title yt-formatted-string')
channel = browser.find_element(By.CSS_SELECTOR,
                               'ytd-video-renderer.ytd-item-section-renderer:nth-child(1) ytd-channel-name.long-byline a')
assert channel.text.lower() == 'Closed on Sunday'.lower()
assert video_name.text.lower() == 'Star Wars Lofi Hip Hop'.lower()
