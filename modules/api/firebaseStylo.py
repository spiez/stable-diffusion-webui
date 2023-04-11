
import json
import os 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('stylo-c2cc2-firebase-adminsdk-e95ll-ab09891f1b.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://stylo-c2cc2-default-rtdb.firebaseio.com'
})

def setServerBusy(isBusy: bool):
  os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
  with open('tunnels.json') as data_file:    
    datajson = json.load(data_file)

  ngrokUrl = datajson['tunnels'][0].get('public_url')
  ref = db.reference('server_status')
  ref.set({
    ngrokUrl + '/busy': isBusy
  })


