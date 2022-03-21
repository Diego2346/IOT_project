import telegram
import time
import xml.etree.ElementTree as ET
from telegram.ext import Updater, CommandHandler, MessageHandler,CallbackQueryHandler,Filters
import paho.mqtt.client as paho
from geopy.distance import geodesic
#capbot2021_bot

def on_connect(self,client, userdata,rc):
    print("Connesso al Broker ")
    self.subscribe('CAP/#')
    
def start(update,context):
    id= update.message.from_user.id
    if id not in users: users[id]={'topic': [], 'location':[],'radius': 0} 
    menu = telegram.InlineKeyboardMarkup(inline_keyboard=[
                     [telegram.InlineKeyboardButton(text='TERREMOTI', callback_data='CAP/terremoti'),
                     telegram.InlineKeyboardButton(text='ALLUVIONI', callback_data='CAP/alluvioni'),
                     telegram.InlineKeyboardButton(text='INCENDI', callback_data='CAP/incendi')],
                     ])
    update.message.reply_text('Seleziona/Rimuovi topic:',reply_markup=menu)
    update.message.reply_text('I tuoi topics: '+(','.join([x.strip('CAP/') for x in users[id]['topic']])))
    print(users)

def select_topics(update,context):
    imput = update.callback_query.data
    id = update.callback_query.message.chat_id
    if imput in users[id]['topic']:     users[id]['topic'].remove(imput)
    else:                               users[id]['topic'].append(imput)
    bot.edit_message_text('I tuoi topics: '+(','.join([x.strip('CAP/') for x in users[id]['topic']])),
                          id, update.callback_query.message.message_id+1)
    print(users)  
   
def on_message(client, userdata, msg):
    data=msg.payload.decode("utf-8")
    topic= msg.topic
    root = ET.fromstring(data)
    namespace = {'xmlns': 'urn:oasis:names:tc:emergency:cap:1.2'} 
    event = root.find('.//xmlns:event', namespace).text
    sender = root.find('.//xmlns:senderName', namespace).text
    severity = root.find('.//xmlns:severity', namespace).text
    effective = root.find('.//xmlns:effective', namespace).text
    description = root.find('.//xmlns:description', namespace).text
    instruction = root.find('.//xmlns:instruction', namespace).text
    circle = root.find('.//xmlns:circle', namespace).text
    img = root.find('.//xmlns:resource/xmlns:uri', namespace).text
    coordinate = list(circle.split(' '))[0]
    latitude = list(coordinate.split(','))[0]
    longitude = list(coordinate.split(','))[1] 
    radius = list(circle.split(' '))[1] 

    def send():
            bot.send_photo(id,img,'*' +event+'*\n\nInviato da: '+sender+'\n\nEntita: '+severity+
                             '\n\nOra: '+ effective +'\n\n'+description +'\n\n'+instruction,parse_mode='Markdown')
            bot.send_location(id,latitude,longitude)
           
    for id in users.keys():
        if topic in users[id]['topic']:
         if users[id]['radius']==0 or users[id]['location']=='': send()
         else: 
            distance= geodesic(coordinate,users[id]['location']) 
            print(distance)
            if float(users[id]['radius'])>=distance: send()        
           
    
def location(update,context):
    id = update.message.chat_id
    latitude=update.message.location.latitude
    longitude=update.message.location.longitude
    users[id]['location']= ([latitude,longitude])
    update.message.reply_text('Inserisci il raggio in km entro il quale vuoi ricevere gli alert')
    dp.add_handler(MessageHandler(Filters.text,raggio))
    print (users)
    
def raggio(update,context):
    id = update.message.chat_id
    radius = update.message.text
    try: 
         float(radius)
         users[id]['radius']=radius
         update.message.reply_text('Raggio di '+ radius +' km inserito')
    except ValueError: 
        update.message.reply_text('Devi inserire un numero')
    print (users)

def mia_posizione(update,context):
   id = update.message.chat_id
   if users[id]['location']: 
       update.message.reply_location(users[id]['location'][0],users[id]['location'][1])
       remove = telegram.InlineKeyboardMarkup([[
                telegram.InlineKeyboardButton(text='RIMUOVI POSIZIONE E RAGGIO', callback_data='Rimuovi posizione')]])
       update.message.reply_text('Raggio:'+ users[id]['radius'],reply_markup=remove)
   else:                    
       update.message.reply_text('Non hai ancora inserito nessuna posizione')
       
def rimuovi_posizione(update,context):    
    id = update.callback_query.message.chat_id
    users[id]['location']=''
    users[id]['radius']=0
    update.callback_query.message.reply_text('Rimossi posizione e raggio')
    print(users)  
   
   
if __name__ == '__main__':
    TOKEN = '1535765316:AAETw1JAaiIl4Ankp59UkhsaGozzLz4HEiI'
    broker="localhost"
    port=1883

    
    users={}
    bot = telegram.Bot(TOKEN)  
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("miei_topics", start))
    dp.add_handler(CommandHandler("mia_posizione", mia_posizione))
    dp.add_handler(CallbackQueryHandler(rimuovi_posizione,pattern="Rimuovi posizione"))
    dp.add_handler(MessageHandler(Filters.location,location))
    dp.add_handler(CallbackQueryHandler(select_topics))
    updater.start_polling()
    client= paho.Client("ClientBOT")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker,port)
    client.loop_start()
    
