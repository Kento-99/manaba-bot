import chromedriver_binary
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser


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
driver.get('https://sso.ritsumei.ac.jp/')

# ユーザー名とパスワードを入力してログイン
username_input = driver.find_element(By.ID, 'User_ID') 
username_input.send_keys(username)
password_input = driver.find_element(By.ID, 'Password')  
password_input.send_keys(password)

# サインインボタンをクリック
sign_in_button = driver.find_element(By.ID, 'Submit')
sign_in_button.click()

# ログイン後のページを開く
wait = WebDriverWait(driver, 10)
wait.until(EC.title_contains('manaba-home'))