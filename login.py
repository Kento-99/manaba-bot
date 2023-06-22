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

# ログイン後のページを開く
wait = WebDriverWait(driver, 10)
wait.until(EC.title_contains('manaba-home'))