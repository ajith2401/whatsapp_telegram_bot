from flask import Flask,jsonify
from flask import request
from flask import Response
import requests
import config1 as config
from df_detect_intent_response1 import *
import os
import json
from dotenv import load_dotenv
import random
load_dotenv()

app = Flask(__name__)

f  = open('C:/Users/Mhs82/Desktop/kural-bot/thirukkural.json' , encoding='utf-8')
kural_data = json.load(f) 

TOKEN = os.environ.get('TELEGRAM_TOKEN')

def tel_send_message(chat_id, fulfillment,intent,book_url):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    if intent == "book-type-selection":
            payload = {
              "chat_id": chat_id,
              "text": "aji"+fulfillment,
              "reply_markup": {
              "inline_keyboard": [
                [
                    {"text": "புத்தகம் வாங்க", 
                     "url": book_url},
                ]
            ]
        }
            }
    elif intent=="book": 
        payload = {
        "chat_id": chat_id,
        "text": fulfillment,
        "reply_markup": {
        "inline_keyboard": [
        [
          {
            "text":"நாவல்",
            "callback_data": "novel"
          }
        ],
        [
          {
            "text":"கவிதை",
            "callback_data": "kavidhai"
          }
        ],
        [
          {
            "text":"சிறுகதை தொகுப்பு",
            "callback_data":"story"
          }
        ],
        [
          {
            "text":"சிறுவர் இலக்கியம்",
            "callback_data": "children"
          }
        ],
        [
          {
            "text":kural_data["categories"][4]["label"],
            "callback_data": kural_data["categories"][4]["name"]
          }
        ]
      ]
    }
  }
    else:
          payload = {
                    'chat_id': chat_id,
                    'text': fulfillment
                    }

   
    r = requests.post(url,json=payload)
    print("tele ", payload)
    return r
 
@app.route('/', methods=['GET','POST'])
def index():
 if request.method == 'POST'or request.method == 'GET':
    message = request.get_json()
    print(message)
    try:
        chat_id, text,query_text, intent,book_url = run(message)
        
        if text != None:
                print("at index", text)
                tel_send_message(chat_id,text,intent,book_url)
        else:
                tel_send_message(chat_id, 'from webhook')
    except:
        print("from index-->")
    return Response('ok', status=200)
 else:
        return "<h1>Welcome!</h1>"

def run(message):
    try:
        chat_id, text = tel_parse_message(message)
        chat_id, fulfillment,query_text, intent,book_url  = handle_message(chat_id, text)
        print("at run text ??????????? ",chat_id, fulfillment,query_text, intent)
        return chat_id, fulfillment,query_text, intent,book_url
    except Exception as e:
        print(e)
        return jsonify({"code": 0, "error": str(e)})
    
def tel_parse_message(message):
    
    print("message-->", message)
    try:
        chat_id = message['message']['chat']['id']
        text = str(message['message']['text'])
        text = text.lower()
        print("chat_id-->", chat_id)
        print("text-->", text)
        return chat_id, text
    except:
        print("NO text found-->>")       
        
def handle_message(chat_id, text):
   text = text 
   chat_id = chat_id
   print("before fulfillmentth",chat_id)
   query_text, intent, fulfillment= detect_intent_text(config.project_id, chat_id, text,config.language_code)
   fulfillment,query_text,intent,book_url  = process_intent(query_text, intent, fulfillment)
  
   print("fulfillmentth",chat_id)
   return chat_id, fulfillment,query_text, intent,book_url
    
def process_intent(query_text, intent, fulfillment):
        global book_url
        book_url = ""
        query_text = query_text
        intent = intent
        if intent == "Default Welcome Intent":
            fulfillment = fulfillment

        elif intent =="aram":
           fulfillment = fulfillment

        elif intent == "bad_words":
            fulfillment = fulfillment
          

        elif intent == "book":
           fulfillment = "புத்தக வகையைத் தேர்ந்தெடுங்கள் தோழரே!"
           
        elif intent =="book-type-selection":
            
            query_text = str(query_text)
            print("book-type-selection",query_text)
            if query_text == "நாவல்" or query_text == "novel":
              book_no =  random.randint(1,len(kural_data["books"]["novel"]))
              
              book_url = kural_data["books"]["novel"][book_no]["url"]
              print("booooooooook urlllllll........",book_url)
              fulfillment = "நூற்பெயர்:"+str(kural_data["books"]["novel"][book_no]["label"])+"\n\nஆசிரியர் பெயர்: "+str( kural_data["books"]["novel"][book_no]["author"])+"\n\nநூற்குறிப்பு: "+str( kural_data["books"]["novel"][book_no]["description"])
            elif query_text == "kavidhai" or query_text == "கவிதை":
              book_no =  random.randint(1,len(kural_data["books"]["kavidhai"]))
              print(len(kural_data["books"]["kavidhai"]))
              
              book_url = kural_data["books"]["kavidhai"][book_no]["url"]
              print("booooooooook urlllllll........",book_url)
              fulfillment = str(kural_data["books"]["kavidhai"][book_no]["label"])+"\n\nஆசிரியர் பெயர்: "+str( kural_data["books"]["kavidhai"][book_no]["author"])+"\n\nநூற்குறிப்பு: "+str( kural_data["books"]["kavidhai"][book_no]["description"])
             
            elif query_text == "story" or query_text == "சிறுகதை தொகுப்பு":
              book_no =  random.randint(1,len(kural_data["books"]["story"]))
              print(len(kural_data["books"]["story"]))
              
              book_url = kural_data["books"]["story"][book_no]["url"]
              print("booooooooook urlllllll........",book_url)
              fulfillment ="நூற்பெயர்:"+ str(kural_data["books"]["story"][book_no]["label"])+"\n\nஆசிரியர் பெயர்: "+str( kural_data["books"]["story"][book_no]["author"])+"\n\nநூற்குறிப்பு: "+str( kural_data["books"]["story"][book_no]["description"])
            elif query_text == "katurai" or query_text == "கட்டுரைத் தொகுப்பு":
              book_no =  random.randint(1,len(kural_data["books"]["katurai"]))
              print(len(kural_data["books"]["katurai"]))
              
              book_url = kural_data["books"]["katurai"][book_no]["url"]
              print("booooooooook urlllllll........",book_url)
              fulfillment = "நூற்பெயர்:"+str(kural_data["books"]["katurai"][book_no]["label"])+"\n\nஆசிரியர் பெயர்: "+str(kural_data["books"]["katurai"][book_no]["author"])+"\n\nநூற்குறிப்பு: "+str( kural_data["books"]["katurai"][book_no]["description"])
            elif query_text == "children" or query_text == "சிறுவர் இலக்கியம்":
              book_no =  random.randint(1,len(kural_data["books"]["children"]))
              print(len(kural_data["books"]["children"]))
              
              book_url = kural_data["books"]["children"][book_no]["url"]
              print("booooooooook urlllllll........",book_url)
              fulfillment ="நூற்பெயர்:"+ str(kural_data["books"]["children"][book_no]["label"])+"\n\nஆசிரியர் பெயர்: "+str(kural_data["books"]["children"][book_no]["author"])+"\n\nநூற்குறிப்பு: "+str(kural_data["books"]["children"][book_no]["description"])
            print(fulfillment)
            fulfillment = fulfillment
 
 
 
        elif intent == "creator":
           fulfillment = fulfillment
        
        elif intent =="Default Fallback Intent":
            # fulfillment= language["fallback_intent"]
            fulfillment= fulfillment

        elif intent == "feedback:":
          fulfillment = fulfillment

        elif intent == "General_Tamil":
           fulfillment = fulfillment

        elif intent == "god":
            fulfillment = fulfillment

        elif intent == "kural":
            kural_no = int(query_text)
            fulfillment = "குறள் எண்:"+ str(kural_data["kural"][kural_no-1]["Number"])+ "\n\nகுறள்:" +kural_data["kural"][kural_no-1]["Line1"] + "\n" + kural_data["kural"][kural_no-1]["Line2"] +"\n\nபொருள்:" + kural_data["kural"][kural_no-1]["sp"] + "\n\nThirukkural:" +kural_data["kural"][kural_no-1]["Translation"] + "\n\nExplanation:"+ kural_data["kural"][kural_no-1]["explanation"] 
            fulfillment = fulfillment

        elif intent == "language":
            fulfillment = fulfillment
            
        elif intent == "love":
             fulfillment = fulfillment
    

        elif intent == "porul":
            fulfillment = fulfillment
           

        elif intent == "random":
            kural_no =  random.randint(1,1332)
            fulfillment = "குறள் எண்:"+ str(kural_data["kural"][kural_no-1]["Number"])+ "\n\nகுறள்:" +kural_data["kural"][kural_no+2]["Line1"] + "\n" + kural_data["kural"][kural_no-1]["Line2"] +"\n\nபொருள்:" + kural_data["kural"][kural_no-1]["sp"] + "\n\nThirukkural:" +kural_data["kural"][kural_no-1]["Translation"] + "\n\nExplanation:"+ kural_data["kural"][kural_no-1]["explanation"] 
            fulfillment = fulfillment
            
        elif intent == "random_wrong":
            if query_text not in ["wrong","false","thappu", "தவறு", "தப்பு","its wrong","it was wrong","இது தப்பு", "இது தவறு","it's wrong","இந்த குறள் தவறு","i think it is wrong","இந்தக் குறள் தப்பு","இந்தக் குறள் தவறு","i think it's wrong"]:
               kural_no =  random.randint(1,1332)
               fulfillment = "என்ன தோழரே! நான் குறளை தவறாகச் சொல்லி இருக்கிறேன்! நீங்கள் கண்டுபிடிக்க வில்லையே! உலகப் பொதுமறையை போய் உருப்படியாய் படியுங்கள் தோழரே! சரி கோபிக்காதீர்கள்! \n\nஇதோ உங்களுக்காக ஒரு சரியான குறள். \n"+ "குறள் எண்:"+ str(kural_data["kural"][kural_no-1]["Number"])+ "\n\nகுறள்:" +kural_data["kural"][kural_no-1]["Line1"] + "\n" + kural_data["kural"][kural_no-1]["Line2"] +"\n\nபொருள்:" + kural_data["kural"][kural_no-1]["sp"] + "\n\nThirukkural:" +kural_data["kural"][kural_no-1]["Translation"] + "\n\nExplanation:"+ kural_data["kural"][kural_no-1]["explanation"] 
               fulfillment = fulfillment
            else:
               kural_no =  random.randint(1,1332)
               fulfillment = "அடடே!சமர்த்து! நான் சொன்ன குறள் தப்புனு கண்டுபிடிச்சிட்டிங்களே! \n\nஇதோ உங்களுக்காக ஒரு சரியான குறள். \n"+ "குறள் எண்:"+ str(kural_data["kural"][kural_no-1]["Number"])+ "\n\nகுறள்:" +kural_data["kural"][kural_no-1]["Line1"] + "\n" + kural_data["kural"][kural_no-1]["Line2"] +"\n\nபொருள்:" + kural_data["kural"][kural_no-1]["sp"] + "\n\nThirukkural:" +kural_data["kural"][kural_no-1]["Translation"] + "\n\nExplanation:"+ kural_data["kural"][kural_no-1]["explanation"] 
               fulfillment = fulfillment

        elif intent == "thanks":
            fulfillment = fulfillment
           
        return fulfillment,query_text,intent,book_url

WHATSAPP_VERIFY_TOKEN = os.environ.get('WHATSAPP_VERIFY_TOKEN')

WHATSAPP_API_TOKEN = os.environ.get('WHATSAPP_API_TOKEN')

# whatsapp bot code

@app.route('/ajith_kural_bot')
def hello_world_whatsapp():
    return 'Hello from Flask!'

def tel_send_message_whatsapp(phone_number,reply_text, phone_number_id):
    phone_number_id = str(phone_number_id)
    url = f'https://graph.facebook.com/v15.0/{phone_number_id}/messages?access_token={WHATSAPP_API_TOKEN}'
    payload = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": phone_number,
      "type": "text",
      "text": {
        "preview_url": True,
        "body": reply_text
        }
       }
    r = requests.post(url,json=payload)
    print("tele ", payload)
    return r

@app.route('/api/webhook', methods = ["POST","GET"])
def whatsapp():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == WHATSAPP_VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    elif request.method == 'POST':
        try:
            data = request.get_json()
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            phone_number_id =data["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
            message_type = message["type"]
            try:
                if (message):
                  if (message_type == 'text'):
                      phone_number,user_text, phone_number_id, chat_id,reply_text, query_text, intent,book_url = run_whatsapp(data)
                      fulfillment = str(reply_text)+ str(book_url)
                      if reply_text != None:
                         print("at index", reply_text)
                         tel_send_message_whatsapp(phone_number,reply_text, phone_number_id)
                else:
                    tel_send_message_whatsapp(phone_number, 'from webhook',phone_number_id)
            except Exception as e:
                print("from index-->")
            return Response('ok', status=200)
        except Exception as e:
            with open("/home/jia/mysite/console_data.txt","a") as f:
                f.write("@app.route(/api/webhook, methods = outline exception")
                f.write("\n")
                f.write(str(e))
                f.write("\n")
            return jsonify({"code": 0, "error": str(e)})

    else:
        return "<h1>Welcome!</h1>"

def run_whatsapp(message):
    try:
        phone_number,user_text,phone_number_id = tel_parse_message_whatsapp(message)
        chat_id, reply_text,query_text, intent,book_url  = handle_message(phone_number,user_text)
        return phone_number,user_text, phone_number_id, chat_id,reply_text, query_text, intent,book_url
    except Exception as e:
        return jsonify({"code": 0, "error": str(e)})

def tel_parse_message_whatsapp(data):
    print("message-->", data)
    try:
        phone_number_id =data["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_text = str(message["text"]["body"])
        phone_number =message["from"]
        user_text = user_text.lower()
        print("text-->", user_text)
        return phone_number,user_text,phone_number_id
    except Exception as e:
        print("NO text found-->>")

if __name__ == '__main__':
   app.run(debug=True)