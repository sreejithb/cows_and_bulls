#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import webapp2
import json
import random
from google.appengine.api import urlfetch
#from enchant import enchant as e
#import nltk
#from nltk.corpus import words
PAGE_ACCESS_TOKEN = "EAAEApDRZCry0BAB0plcZATH3OZCwW2AqQThiZCkeCuMLxNHjRjVUZAB33rJZArWOgPOsy7Wu0I8XP7I1ZAtbGzcQuOVoGpZAc4r3gfN7hjeZC5Hp323o99zkt2zqmKcfSvHf4gnfRgZCGd34HmLmVJeVuxYi8wG5fp3hIs1ZCEQkjAiFwZDZD"
wordlist = [u'able', u'acid', u'aged', u'also', u'army', u'back', u'band', u'bank', u'base', u'bath', u'bear', u'beat', u'belt', u'best', u'bird', u'blow', u'blue', u'boat', u'body', u'bond', u'bone', u'born', u'both', u'bowl', u'bulk', u'burn', u'bush', u'busy', u'calm', u'came', u'camp', u'card', u'care', u'case', u'cash', u'cast', u'chat', u'chip', u'city', u'club', u'coal', u'coat', u'code', u'cold', u'come', u'cope', u'copy', u'CORE', u'cost', u'crew', u'crop', u'dark', u'date', u'dawn', u'days', u'deal', u'dean', u'dear', u'debt', u'deny', u'desk', u'dial', u'dick', u'diet', u'disc', u'disk', u'does', u'done', u'dose', u'down', u'draw', u'drew', u'drop', u'drug', u'dual', u'duke', u'dust', u'duty', u'each', u'earn', u'east', u'easy', u'evil', u'exit', u'face', u'fact', u'fail', u'fair', u'farm', u'fast', u'fate', u'fear', u'felt', u'file', u'film', u'find', u'fine', u'fire', u'firm', u'fish', u'five', u'flat', u'flow', u'ford', u'form', u'fort', u'four', u'from', u'fuel', u'fund', u'gain', u'game', u'gate', u'gave', u'gear', u'gift', u'girl', u'give', u'glad', u'goal', u'goes', u'gold', u'Golf', u'gone', u'gray', u'grew', u'grey', u'grow', u'gulf', u'hair', u'half', u'hand', u'hang', u'hard', u'harm', u'hate', u'have', u'head', u'hear', u'heat', u'held', u'help', u'hero', u'hire', u'hold', u'hole', u'holy', u'home', u'hope', u'host', u'hour', u'huge', u'hung', u'hunt', u'hurt', u'idea', u'inch', u'into', u'iron', u'item', u'jack', u'jane', u'jean', u'john', u'join', u'jump', u'jury', u'just', u'kent', u'kept', u'kind', u'king', u'knew', u'know', u'lack', u'lady', u'laid', u'lake', u'land', u'lane', u'last', u'late', u'lead', u'left', u'life', u'lift', u'like', u'line', u'link', u'list', u'live', u'load', u'loan', u'lock', u'long', u'lord', u'lose', u'lost', u'love', u'luck', u'made', u'mail', u'main', u'make', u'male', u'many', u'Mark', u'meal', u'mean', u'meat', u'menu', u'mike', u'mile', u'milk', u'mind', u'mine', u'mode', u'more', u'most', u'move', u'much', u'must', u'name', u'navy', u'near', u'neck', u'news', u'next', u'nice', u'nick', u'nose', u'note', u'okay', u'once', u'only', u'open', u'oral', u'over', u'pace', u'pack', u'page', u'paid', u'pain', u'pair', u'palm', u'park', u'part', u'past', u'path', u'peak', u'pick', u'pink', u'plan', u'play', u'plot', u'plug', u'plus', u'port', u'post', u'pure', u'push', u'race', u'rail', u'rain', u'rank', u'rate', u'read', u'real', u'rely', u'rent', u'rest', u'rice', u'rich', u'ride', u'ring', u'rise', u'risk', u'road', u'rock', u'role', u'rose', u'rule', u'rush', u'ruth', u'safe', u'said', u'sake', u'sale', u'salt', u'same', u'sand', u'save', u'seat', u'self', u'send', u'sent', u'sept', u'ship', u'shop', u'shot', u'show', u'shut', u'sick', u'side', u'sign', u'site', u'size', u'skin', u'slip', u'slow', u'snow', u'soft', u'soil', u'sold', u'sole', u'some', u'song', u'sort', u'soul', u'spot', u'star', u'stay', u'step', u'stop', u'such', u'suit', u'sure', u'take', u'tale', u'talk', u'tank', u'tape', u'task', u'team', u'tech', u'tend', u'term', u'than', u'them', u'then', u'they', u'thin', u'this', u'thus', u'time', u'tiny', u'told', u'tone', u'tony', u'tour', u'town', u'trip', u'true', u'tune', u'turn', u'twin', u'type', u'unit', u'upon', u'used', u'user', u'vary', u'vast', u'very', u'vice', u'view', u'vote', u'wage', u'wait', u'wake', u'walk', u'want', u'ward', u'warm', u'wash', u'wave', u'ways', u'weak', u'wear', u'went', u'west', u'what', u'when', u'whom', u'wide', u'wife', u'wild', u'wind', u'wine', u'wing', u'wire', u'wise', u'wish', u'with', u'word', u'wore', u'work', u'yard', u'yeah', u'year', u'your', u'zero', u'zone']
#gamestarted = 0
#currentWord = ""
#gamestep = 0
activeusers = {}
activegamesteps = {}

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info('SREE')
        self.response.write('I hereby declare that the Cows and Bulls app is not collecting and storing any personal information like the email, password or credit card information of any of its users. \nOnly your facebook id is stored during runtime to keep track of the word you are supposed to guess and to distinguish yourself from other players.\nWe are also not selling anything to anyone.')

class Webhook(webapp2.RequestHandler):
    def get(self):
        verification_token = 'flat_verify_token'
        if((self.request.get('hub.mode') == 'subscribe')&(self.request.get('hub.verify_token')== verification_token)):
            self.response.set_status(200)
            self.response.write(self.request.get('hub.challenge'))
        else:
            self.response.write("Not Working")
    def post(self):
        def dolog(message1):
            logging.info("SREE"+message1)

        def post_structured_message(fbid):
            hd ={"Content-Type": "application/json"}
            post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
            response_msg = json.dumps(
            {
                "recipient": {"id": fbid},
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": [{
                                "title": "rift",
                                "subtitle": "Next-generation virtual reality",
                                "item_url": "https://www.oculus.com/en-us/rift/",
                                "image_url": "https://lh3.googleusercontent.com/Q6Zv7EaCj-AbxKmsmhjA9yCg_dZVs7uuRWZZbmwYBtjkVHC-1FRMd8qmj7Z7XfrL3Hc2=w300-rw",
                                "buttons": [{
                                    "type": "web_url",
                                    "url": "https://www.oculus.com/en-us/rift/",
                                    "title": "Open Web URL"},
                                    {"type": "postback",
                                    "title": "Call Postback",
                                    "payload": "Payload for first bubble",}],
                                }, {
                                "title": "touch",
                                "subtitle": "Your Hands, Now in VR",
                                "item_url": "https://www.oculus.com/en-us/touch/",
                                "image_url": "http://messengerdemo.parseapp.com/img/touch.png",
                                "buttons": [{
                                    "type": "web_url",
                                    "url": "https://www.oculus.com/en-us/touch/",
                                    "title": "Open Web URL"}, {
                                    "type": "postback",
                                    "title": "Call Postback",
                                    "payload": "Payload for second bubble",}]
                            }]
                        }
                    }
                }
            })
            #response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":fbid}})
            result = urlfetch.fetch(url=post_message_url,payload=response_msg,method=urlfetch.POST,headers=hd)
            logging.info(deb+result.content)

        def post_button_message(fbid):
            hd ={"Content-Type": "application/json"}
            post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
            response_msg = json.dumps(
                {
                "recipient": {"id": fbid},
                "message": {
                    "attachment":{
                        "type":"template",
                        "payload":{
                            "template_type":"button",
                            "text":"Sreejith's battery is low!\nWhat do you want to do next?",
                            "buttons":[{
                                "type":"postback",
                                "title":"Where is he now?",
                                "payload":"WHERE"},{
                                "type":"postback",
                                "title":"How much is left?",
                                "payload":"HOW_MUCH"}
                            ]
                        }
                    }
                }
            })
            result = urlfetch.fetch(url=post_message_url,payload=response_msg,method=urlfetch.POST,headers=hd)
            logging.info(deb+result.content)

        def post_another_game(fbid):
            hd ={"Content-Type": "application/json"}
            post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
            response_msg = json.dumps(
                {
                "recipient": {"id": fbid},
                "message": {
                    "attachment":{
                        "type":"template",
                        "payload":{
                            "template_type":"button",
                            "text":"Wanna play a new game? (Click one of the buttons below)",
                            "buttons":[{
                                "type":"postback",
                                "title":"Yes",
                                "payload":"YES"},{
                                "type":"postback",
                                "title":"No",
                                "payload":"NO"},{
                                "type":"postback",
                                "title":"How does this work?",
                                "payload":"HELP"}
                            ]
                        }
                    }
                }
            })
            result = urlfetch.fetch(url=post_message_url,payload=response_msg,method=urlfetch.POST,headers=hd)
            logging.info(deb+result.content)

        def post_facebook_message(fbid, received_message):
        	#wordurl = 'http://wordfinder.yourdictionary.com/letter-words/4'
            hd ={"Content-Type": "application/json"}
            #wordpage = urlfetch.fetch(wordurl)
            #url = 'http://www.google.com/humans.txt'
            try:
                #resulttemp = urlfetch.fetch(url)
                post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
                #response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":"tst"}})
                response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":received_message}})
                result = urlfetch.fetch(url=post_message_url,payload=response_msg,method=urlfetch.POST,headers=hd)
                logging.info(deb+result.content)
            except urlfetch.Error:
                logging.exception('Caught exception fetching url')

        def post_start_game(fbid,received_message):
            hd ={"Content-Type": "application/json"}
            #global gamestarted
            #global currentWord
            #global gamestep
            gamejustended = 0;
            messback = ""
            try:
                if (fbid in activeusers):
                    if len(received_message) != 4:
                        messback = "Sorry I dont understand. Please type in just your guess which should be a 4 letter word"
                    else:
                        if (fbid in activegamesteps):
                            gamestep = activegamesteps[fbid]
                        else:
                            gamestep = 0
                        activegamesteps[fbid] = gamestep + 1;
                        b,c = checkbc(received_message.lower(),activeusers[fbid].lower())
                        if (b==4):
                            messback = "Congratulations! You guessed it right!"
                            activeusers.pop(fbid,None)
                            gamejustended = 1
                            #post_another_game(fbid)
                        else:
                            messback = "Guesses: " + str(gamestep) + "\n" + "Bulls:"+str(b)+" Cows:"+str(c)
                            if (gamestep >=15):
                                messback = messback + "\nSorry. You didn't guess it.\nThe word was: " + activeusers[fbid]
                                gamejustended = 1
                                activeusers.pop(fbid,None )
                                #post_another_game(fbid)


                else:
                    activegamesteps[fbid] = 0
                    currentWord = random.choice(wordlist).lower()
                    activeusers[fbid] = currentWord
                    messback = "Mooo..I have a 4 letter word.\nTo make it simple for you, the word has no repeating alphabets\nMake your first guess (Type in just the word please)"
                    #gamestarted = 1

                post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
                #response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":"tst"}})
                response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":messback}})
                result = urlfetch.fetch(url=post_message_url,payload=response_msg,method=urlfetch.POST,headers=hd)

                if (gamejustended == 1):
                    post_another_game(fbid)
                logging.info(deb+result.content)
            except urlfetch.Error:
                logging.exception('Caught exception fetching url')

        def checkbc(guessword,currentWord):
            #global currentWord
            ref = set(currentWord)
            guess = set(guessword)
            intersect = ref & guess
            bulls = 0
            cows = 0
            for i in range(0,len(currentWord)):
                if guessword[i] == currentWord[i]:
                    bulls = bulls + 1
            cows = len(intersect)-bulls
            return bulls,cows

        def handle_postback(event):
        	#helptext = "I will pick a 4 letter word and your task is to guess the word"
        	#.\nFor every guess you make, I will tell you how many Bulls and Cows you got correct"
			#helptext = helptext +"\nFor every alphabet in your guess, I will look at whether it is present in my word."
			#helptext = helptext + "\nIf an alphabet in your word is present in mine at the same place, its counted as a bull."
			#helptext = helptext + "\nIf an alphabet in your word is present in mine but at a different place, its counted as a cow."
			#helptext = helptext + "For instance, if my word is TOAD and your guess is GOAT, it will be 2 bulls (for the O and A) and 1 cow (for the T)"

            #global gamestarted
            senderID = event['sender']['id']
            recipientID = event['recipient']['id']
            timeOfPostback = event['timestamp']
            payload = event['postback']['payload']
            if payload == 'YES':
                post_start_game(senderID,"")
                #post_another_game(senderID)
            elif payload == 'NO':
                activeusers.pop(senderID,None)
                post_facebook_message(senderID,"Alright then")
            elif payload == "HELP":
            	helpt = "I will pick a 4 letter word and your task is to guess the word.\n"
            	helpt = helpt + "For every guess you make, I will tell you how many Bulls and Cows you got correct\n\n"
            	post_facebook_message(senderID,helpt)
            	helpt = "If an alphabet in your word is present in mine at the same place, its counted as a bull"
            	post_facebook_message(senderID,helpt)
            	helpt = "If an alphabet in your word is present in mine but at a different place, its counted as a cow"
            	post_facebook_message(senderID,helpt)
            	helpt = "For instance, if my word is TOAD and your guess is GOAT, it will be 2 bulls (for the O and A) and 1 cow (for the T)"
            	post_facebook_message(senderID,helpt)
            	post_another_game(senderID)
            else:
            	post_facebook_message(senderID,"Something went wrong!")

            #if (payload == 'HOW_MUCH'):
                #post_facebook_message(senderID,"14% Left")
            #else:
                #post_facebook_message(senderID,"At Work")

        deb = "SREE"
        data = self.request.body
        logging.info(deb+data)
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        logging.info(deb)
        for entry in incoming_message['entry']:
            logging.info(deb)
            for message in entry['messaging']:
                logging.info(deb)
                if 'message' in message:
                    logging.info(deb)
                    # Print the message to the terminal
                    #pprint(message)
                    logging.info(message)
                    dolog(deb)
                    #if(message['message']['text']=='generic'):
                        #post_structured_message(message['sender']['id'])
                    #elif(message['message']['text']=="button"):
                        #post_button_message(message['sender']['id'])
                    #else:
                        #generic_message = "Shhhhh.. Let me sleep. \nI got nothing for you at the moment"
                        #post_facebook_message(message['sender']['id'], message['message']['text'])
                    fbid = message['sender']['id']
                    if(fbid in activeusers):
                    	post_start_game(message['sender']['id'], message['message']['text'])
                    else:
                    	post_another_game(message['sender']['id'])
                elif 'postback' in message:
                    handle_postback(message)


        #data2 = self.request.get("entry")
        #data3 = self.request.POST("entry")

        self.response.set_status(200)
        self.response.write("Received")

    def receivedMessage(event):
        logging.info("SREE INSIDE RECEIVED MESSAGE")





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/webhook2', Webhook)
], debug=True)
