from flask import Flask
from flask import request
from flask import Response
import requests
import json
TOKEN = "6259722499:AAECDwZNjkM8uyCDOFnMD-dsc-JjwL--bqM"
app = Flask(__name__)
 
def parse_message(message):
    print("message-->",message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id,txt
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r
 
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        msg=request.get_json()
       
        chat_id,txt = parse_message(msg)
        if txt == "hi":
            tel_send_message(chat_id,"Hello!!")
        else:    
            tmp_res=requests.get('https://api.coincap.io/v2/assets')
            res=json.loads(tmp_res.text)
            for i in res['data']:
                if i['symbol']==txt.upper():
                    price=float(i['priceUsd'])
                    price=f"{price:.2f}"
                    tel_send_message(chat_id,f"{txt.upper()} : {price} USD")
            else:tel_send_message(chat_id,"NOT A VALID SYMBOL!,\nplease send a valid symbole like ETH,BTC,BNB etc.")
       
        return Response('ok', status=200)
    else:
        return Response('Bad Request',status=403)
 
if __name__ == '__main__':
   app.run(threaded=True)