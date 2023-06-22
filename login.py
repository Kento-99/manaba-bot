import chromedriver_binary
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
import time

#ConfigParserオブジェクトを生成
config = configparser.ConfigParser()

#設定ファイル読み込み
config.read('config.ini')

# ログインに使用するユーザー名とパスワード
username =config['DEFAULT']['username']
password =config['DEFAULT']['password']

# WebDriverでChromeブラウザを起動
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') 
driver = webdriver.Chrome(options=options)

# manabaのログインページを開く
driver.get('https://ct.ritsumei.ac.jp/ct/%E3%80%8D')

# ユーザー名とパスワードを入力してログイン
wait = WebDriverWait(driver,20)
wait.until(EC.visibility_of_element_located((By.ID, 'User_ID')))
username_input = driver.find_element(By.ID, 'User_ID') 
username_input.send_keys(username)
wait.until(EC.visibility_of_element_located((By.ID, 'Password')))
password_input = driver.find_element(By.ID, 'Password')  
password_input.send_keys(password)

# サインインボタンをクリック
wait.until(EC.element_to_be_clickable((By.ID, 'Submit')))
sign_in_button = driver.find_element(By.ID, 'Submit')
sign_in_button.click()
wait = WebDriverWait(driver, 10)
# ページ遷移の完了を待機
wait.until(EC.staleness_of(sign_in_button))

# HTMLを再読み込み
driver.refresh()
html = driver.page_source

#マイページボタンをクリック
wait.until(EC.element_to_be_clickable((By.ID, 'mypagelogo')))
mypage_button = driver.find_element(By.ID, 'mypagelogo')
mypage_button.click()
# ページ遷移の完了を待機
wait.until(EC.staleness_of(mypage_button))

# HTMLを再読み込み
driver.refresh()
html = driver.page_source

# 未提出課題の<a>タグをクリック
link = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div/div[4]/div[2]/div[2]/div/a')
link.click()
# ページ遷移の完了を待機
wait.until(EC.staleness_of(link))

# HTMLを再読み込み
driver.refresh()
html = driver.page_source

# <td>タグを指定して要素を取得
td_element = driver.find_element(By.TAG_NAME, 'td')

# <td>タグの中身を取得して出力
print(td_element.text)
