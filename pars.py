from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Замените на ваш прокси-сервис.
PROXY_IP = "202.47.188.132"  # Замените на IP вашего прокси.
PROXY_PORT = "8090"  # Замените на порт вашего прокси.

PROXY = f"{PROXY_IP}:{PROXY_PORT}"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

browser = webdriver.Chrome(options=chrome_options)

try:
    browser.get('https://www.centralbank.ae/en/forex-eibor/exchange-rates/')
    
    # Ожидайте, пока текст "Agree and continue" не появится на экране, и нажмите на него.
    agree_text = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Agree and continue")]')))
    agree_text.click()

    # Ожидайте, пока таблица не будет загружена.
    table = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # Извлеките данные из таблицы.
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        cols = [ele.text for ele in cols]
        data.append([ele for ele in cols if ele])

    # Сохраните данные в текстовый файл.
    with open('output.txt', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    browser.quit()
