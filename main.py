from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
from bs4 import BeautifulSoup
import datetime
from linebot import LineBotApi
from linebot.models import FlexSendMessage
import urllib.parse

#ConfigParserオブジェクトを生成
config = configparser.ConfigParser()

#設定ファイル読み込み
config.read('config.ini')

#linebotの送信前準備
CHANNEL_ACCESS_TOKEN = config['DEFAULT']['CHANNEL_ACCESS_TOKEN'] 
USER_ID = config['DEFAULT']['USER_ID'] 

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# ログインに使用するユーザー名とパスワード
username =config['DEFAULT']['username']
password =config['DEFAULT']['password']

# WebDriverでChromeブラウザを起動
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') 
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

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
minitest = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div/div[4]/div[2]/div[2]/div/a')
minitest.click()
# ページ遷移の完了を待機
wait.until(EC.staleness_of(minitest))

# HTMLを再読み込み
driver.refresh()
html = driver.page_source

# BeautifulSoupでHTMLを解析
soup1 = BeautifulSoup(html, 'html.parser')

# trタグごとに中のtdタグの情報を取得し、配列に折りたたむ
#課題の期限を読み取り一日前に迫っている場合配列をkadai_arrayに追加する
kadai_array1 = []
today = datetime.datetime.now()

for tr_tag in soup1.find_all('tr'):
    td_tags = tr_tag.find_all('td')
    minitest_data = [td.text for td in td_tags]
    # aタグのhref属性を取得
    a_tags = tr_tag.find_all('a')
    for a in a_tags:
        href = a.get('href')
        if href:
            # URLを絶対パスに変換して配列に追加
            base_url ="https://ct.ritsumei.ac.jp/ct/"
            absolute_url = urllib.parse.urljoin(base_url, href)
            minitest_data.append(absolute_url)
    if len(minitest_data) > 2 and minitest_data[2] != '期限' and minitest_data[2] != '':
     deadline = datetime.datetime.strptime(minitest_data[2], '%Y-%m-%d %H:%M')
     if datetime.timedelta(hours=0) <= (deadline - today) <= datetime.timedelta(hours=24):#課題の期限を読み取り、一日以内の場合kadai_arrayに追加する
      kadai_array1.append(minitest_data)


#アンケートの<a>タグをクリック
questionary = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div/ul/li[2]/a')
questionary.click()
# ページ遷移の完了を待機
wait.until(EC.staleness_of(questionary))

# HTMLを再読み込み
driver.refresh()
html = driver.page_source

# BeautifulSoupでHTMLを解析
soup2 = BeautifulSoup(html, 'html.parser')

# trタグごとに中のtdタグの情報を取得し、配列に折りたたむ
kadai_array2 = []

for tr_tag in soup2.find_all('tr'):
    td_tags = tr_tag.find_all('td')
    questionary_data = [td.text for td in td_tags]
    # aタグのhref属性を取得
    a_tags = tr_tag.find_all('a')
    for a in a_tags:
        href = a.get('href')
        if href:
            # URLを絶対パスに変換して配列に追加
            base_url ="https://ct.ritsumei.ac.jp/ct/"
            absolute_url = urllib.parse.urljoin(base_url, href)
            questionary_data.append(absolute_url)
    if len(questionary_data) > 2 and questionary_data[2] != '期限' and questionary_data[2] != '':
     deadline = datetime.datetime.strptime(questionary_data[2], '%Y-%m-%d %H:%M')
     if datetime.timedelta(hours=0) <= (deadline - today) <= datetime.timedelta(hours=24):#課題の期限を読み取り、一日以内の場合kadai_arrayに追加する
      kadai_array2.append(questionary_data)


#レポートの<a>タグをクリック
report = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div/ul/li[3]/a')
report.click()
# ページ遷移の完了を待機
wait.until(EC.staleness_of(report))

# HTMLを再読み込み
driver.refresh()
html = driver.page_source

# BeautifulSoupでHTMLを解析
soup3 = BeautifulSoup(html, 'html.parser')

# trタグごとに中のtdタグの情報を取得し、配列に折りたたむ
kadai_array3 = []

for tr_tag in soup3.find_all('tr'):
    td_tags = tr_tag.find_all('td')
    report_data = [td.text for td in td_tags]
    # aタグのhref属性を取得
    a_tags = tr_tag.find_all('a')
    for a in a_tags:
        href = a.get('href')
        if href:
            # URLを絶対パスに変換して配列に追加
            base_url ="https://ct.ritsumei.ac.jp/ct/"
            absolute_url = urllib.parse.urljoin(base_url, href)
            report_data.append(absolute_url)
    if len(report_data) > 2 and report_data[2] != '期限' and report_data[2] != '':
     deadline = datetime.datetime.strptime(report_data[2], '%Y-%m-%d %H:%M')
     if datetime.timedelta(hours=0) <= (deadline - today) <= datetime.timedelta(hours=24):#課題の期限を読み取り、一日以内の場合kadai_arrayに追加する
      kadai_array3.append(report_data)

# 結果をlinebotが送信
for kadai_array, category_name in [(kadai_array1, "小テスト"), (kadai_array2, "アンケート"), (kadai_array3, "レポート")]:
    if kadai_array:
        for data_row in kadai_array:
            message={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": data_row[1],
                        "weight": "bold",
                        "size": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": f'{data_row[0].strip()}の期限が迫っています',
                                "wrap": True,
                                "color": "#666666",
                                "size": "md",
                                "flex": 5,
                                "margin": "sm"
                            }
                            ],
                            "spacing": "none",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "期限",
                                "color": "#aaaaaa",
                                "size": "md",
                                "flex": 1,
                                "margin": "none"
                            },
                            {
                                "type": "text",
                                "text": data_row[2],
                                "wrap": True,
                                "color": "#666666",
                                "size": "md",
                                "flex": 5
                            }
                            ],
                            "margin": "xl"
                        }
                        ]
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "uri": data_row[3],
                        "label": "manaba"
                        },
                        "color": "#b8d200"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "margin": "sm"
                    }
                    ],
                    "flex": 0
                }
                }
            flex_message = FlexSendMessage(alt_text='課題',contents=message)
            line_bot_api.push_message(USER_ID,flex_message)

#webdriverの終了処理
driver.quit()
