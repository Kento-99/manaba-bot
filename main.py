from linebot import LineBotApi
from linebot.models import TextSendMessage
import configparser

#ConfigParserオブジェクトを生成
config = configparser.ConfigParser()

#設定ファイル読み込み
config.read('config.ini')

CHANNEL_ACCESS_TOKEN = config['DEFAULT']['CHANNEL_ACCESS_TOKEN'] #ここに自分のトークンを入れて下さい

USER_ID = config['DEFAULT']['USER_ID'] #ここに自分のユーザーIDを入れて下さい

text = "hi"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

line_bot_api.push_message(USER_ID, TextSendMessage(text=text))