import argparse
import csv
import os
import requests as req

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_access_by_url(url, headers):
  try:
    response = req.get(url, headers=headers)
    if response.status_code == 200:
      return True
    else:
      return False
  except req.exceptions.RequestException:
    return False


# Аргумент URL который надо закинуть
pars = argparse.ArgumentParser(prog='ANDRX_NGU_parser', description='Lol, try')
pars.add_argument(dest='input_url', type=str, default='', help='input url')
args = pars.parse_args()
url = args.input_url

load_dotenv()

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
headers = {'User-Agent': 'Mozilla/5.0'} # чисто для requests

#END_FOR_GO - маркер выхода
links = ['Личный кабинет студента', 'Войти', 'END_FOR_GO'] # я вначале гуляю по сайту НГУ, а именно по ссылкам


username = os.getenv('LOGIN') # логин от НГУ аккаунта
password = os.getenv('PASSWORD') # пароль от НГУ аккаунта

links_info = ([], [])

found = False
curr_url = url
for link in links:

  found = False
  ch = check_access_by_url(curr_url, headers)
  if not ch:
    print(f'Держу в курсе:\nURL {curr_url} НЕ ДОСТУПЕН ИЛИ НЕ СУЩЕСТВУЕТ')
    break
  else:
    print(f'Держу в курсе:\nURL {curr_url} ДОСТУПЕН')
    driver.execute_script("window.open('" + curr_url + "', '_blank')")
    driver.switch_to.window(driver.window_handles[-1])
    # driver.get(current_url)

    if link != 'END_FOR_GO':
      wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{link}')]")))
      elements = driver.find_elements(By.XPATH, f"//a[contains(text(), '{link}')]")
      if elements:
        new_url = elements[0].get_attribute('href')
        curr_url = new_url if new_url.startswith('http') else '/'.join(curr_url.split('/')[:-1]) + new_url
        found = True
      else:
        print(f'Ссылка с названием \'{link}\' не найдена на странице: {curr_url}')
        break
    else:
      found = True
      break


if found:

  wait.until(EC.presence_of_element_located((By.ID, 'username')))
  wait.until(EC.presence_of_element_located((By.ID, 'password')))
  wait.until(EC.presence_of_element_located((By.ID, 'submitBtn')))
  username_input = driver.find_element(By.ID, 'username')
  password_input = driver.find_element(By.ID, 'password')

  # Вводим данные в поля ввода
  username_input.send_keys(username)
  password_input.send_keys(password)

  # Находим и нажимаем кнопку отправки формы
  submit_btn = driver.find_element(By.ID, 'submitBtn')
  submit_btn.click()

  driver.switch_to.window(driver.window_handles[-1])

  links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.nav-link:not([class*=\' \'])')))
  print("--------------")
  print("Выбирались только ссылки из nav-link, которые не имеют других классов")

  links_text = []
  links_href = []
  links_count_chars = []
  links_count_nums = []

  for link in links:
    link_text = link.text
    link_href = link.get_attribute("href")

    driver.execute_script("window.open('" + link_href + "', '_blank')")
    driver.switch_to.window(driver.window_handles[-1])

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.page-content')))
    page_content = driver.find_element(By.CSS_SELECTOR, '.page-content')
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
    h1_first_el = page_content.find_element(By.TAG_NAME, 'h1')
    h1_first_el_text = h1_first_el.text

    link_count_chars = sum(c.isalpha() for c in page_content.text)
    link_count_nums = sum(c.isdigit() for c in page_content.text)
    
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])

    print("--------------")
    print('Название страницы:', h1_first_el_text)
    print('URL страницы:', link_href)
    print('Кол-во букв в контенте:', link_count_chars)
    print('Кол-во цифр в контенте:', link_count_nums)
    links_text.append(h1_first_el_text)
    links_href.append(link_href)
    links_count_chars.append(link_count_chars)
    links_count_nums.append(link_count_nums)

  with open('result.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Only links from \'nav-link\' that do not have other classes were selected'])
    writer.writerow(['Page', 'Page title', 'Page URL', 'Number of letters in content', 'Number of numbers in content'])
    writer.writerow('')

    for cnt in range(len(links_text)):
      writer.writerow([cnt + 1, links_text[cnt], links_href[cnt], links_count_chars[cnt], links_count_nums[cnt]])

driver.quit()
 

# JavaScript, ебать, но Бетон, короче твердый уеба
# count_chars, count_nums = driver.execute_script("""
    # var body = arguments[0];
    # var children = body.childNodes;
    # var count_chars = 0;
    # var count_nums = 0;
# for (var i = 0; i < children.length; i++)
    # {
    #     if (children[i].nodeType === 3)
    #     {
    #         count_chars += (children[i].nodeValue.trim().match(/[A-Za-zА-Яа-я]/g) || []).length;
    #         count_nums += (children[i].nodeValue.trim().match(/[0-9]/g) || []).length;
    #     }
    #     else if (children[i].tagName !== 'SCRIPT' && children[i].tagName !== 'NOSCRIPT')
    #     {
    #         count_chars += (children[i].textContent.trim().match(/[A-Za-zА-Яа-я]/g) || []).length;
    #         count_nums += (children[i].textContent.trim().match(/[0-9]/g) || []).length;
    #     }
    # }
    # return [count_chars, count_nums]; """, body)

