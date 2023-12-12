from datetime import datetime
from flask import Flask, request
from pymessenger import Bot
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask("Echo Bot")

filehandle = open("message.log","a")

FB_ACCESS_TOKEN = '' 

bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hurricane complex token"


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return 200


@app.route('/', methods=['POST'])
def webhook():

    data = request.get_json()
    print(data)

    if data['object'] == "page":
        entries = data['entry']
        
        for entry in entries:
            messaging = entry['messaging']

            for messaging_event in messaging:

                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    
                    if messaging_event['message'].get('text'):
                        
                        query = messaging_event['message']['text']

                        filehandle.write("{},{}\n".format(sender_id, query))
                        filehandle.flush()

                        bot.send_text_message(sender_id, str(datetime.now()))

    return "ok", 200




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000, use_reloader = True)
