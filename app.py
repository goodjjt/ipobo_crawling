import telegram
import requests
import urllib3
import schedule
import time
from datetime import datetime
import time

# Telegram - jjt
telegram_token = "5128692345:AAHkO-3JZ9tZYP2hrS5UAlnYCrO0PiO09_A"
telegram_id = "444879086"
bot = telegram.Bot(token = telegram_token)

# https 처리 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://mirihae.com/camping/selectAjaxDatePinInfo.do'

palyload = {
    'checkType': '',
    'device': 'pc',
    'tocken': '20221101134629-f83c19cb-cb7e-4fd5-87d2-d410391cd094',
    'pageId': 'Z65332353',
    'groupCode': 'epoc',
    'selectStartDate': '2022-12-03',
    'selectEndDate': '2022-12-05',
    'selectMonth': '',
    'selectItemId': '',
    'selectTicketId': '',
    'cnt': '',
    'infoType': ''
}

print("[" + "이포보 오토캠핑장" + "] " + palyload['selectStartDate'] + " ~ " + palyload['selectEndDate']);

def crawling():
    # 이포보 오토캠핑장
    response = requests.post(url, data=palyload, verify=False)

    cnt = 0
    message = "[" + "이포보 오토캠핑장" + "]" + " https://mirihae.com/epoc/camping/Z65332353" + '\n'
    if response.status_code == 200:
        jsonData = response.json()
        for data in jsonData.get('pinCategoryList')[0].get('pinList'):
            if data.get("reserveCnt") == 0:
                cnt += 1
                message = message + data.get("itemNm") + ', '
        print(time.strftime('%Y-%m-%d %H:%M:%S'), ":", cnt)
        if cnt > 0:
            bot.sendMessage(chat_id=telegram_id, text=message)
    else :
        print(response.status_code)


# step3.실행 주기 설정
schedule.every(20).seconds.do(crawling)
# schedule.every(1).minutes.do(message1)

while True:
    schedule.run_pending()
    time.sleep(1)

# if __name__ == '__main__':
#     crawling()