from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import json, requests, random, re
from pprint import pprint
from django.utils.decorators import method_decorator
import paho.mqtt.client as mqtt
from .services import _broker

PAGE_ACCESS_TOKEN = "EAACb90wmKqkBAMXZCZAqwZAVCYEzAB8r78j1OXtf1zhRtapfkhGczwh50VZCkKUT8PBXvKHDpWrnd9Hv4I2ERKOCckCunhrymHpNpZBIzCLmF7Q8jpQmZBr492Uki3idHWOphqQgJiQ0OeVWX9fKKhuVpKIbps1pW7RP4gCxZCqFQZDZD"
TOKEN = 'cruz_token'

post_message_url = (
    'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(
        PAGE_ACCESS_TOKEN))

broker = 'vps.datalogy.asia'
port = 1883

username = 'inno'
password = 'vake'

_id = 0

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("report")

def on_message(client, userdata, msg):
    _text = str(msg.payload.decode())
    response_msg = json.dumps({
        "recipient": {
            "id": 1791221587568171
        },
        "message": {
            "text": _text
        }
    })
    requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    client.disconnect()

def listner(client_id, username, password, broker, port):
    client = mqtt.Client(str(client_id))

    client.username_pw_set(username, password)

    client.connect(broker, port, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


class IndexView(View):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
         # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))

        global _id
        _id = incoming_message['entry'][0]['messaging'][0]['sender']['id']
        user_details_url = "https://graph.facebook.com/v2.6/%s" % _id
        user_details_params = {
            'fields': 'first_name,last_name,profile_pic',
            'access_token': PAGE_ACCESS_TOKEN
        }
        user_details = requests.get(user_details_url,
                                    user_details_params).json()

        if "postback" in incoming_message['entry'][0]['messaging'][0]:
            if incoming_message['entry'][0]['messaging'][0]['postback'][
                    'payload'] == "GET_STARTED":

                _text = 'Hello ' + user_details['first_name'] + '!! ' + 'welcome to mqtt_test!'
                response_msg = json.dumps({
                    "recipient": {
                        "id": _id
                    },
                    "message": {
                        "text": _text
                    }
                })
                status = requests.post(
                    post_message_url,
                    headers={"Content-Type": "application/json"},
                    data=response_msg)
                return HttpResponse()

            if incoming_message['entry'][0]['messaging'][0]['postback']['payload'] == 'BULB_ON':
                _broker(str(_id), 'house/bulb1', 'on')
                _text = 'Server: bulb turned on'
                listner(_id, username, password, broker, port)

                response_msg = json.dumps({
                    "recipient": {
                        "id": _id
                    },
                    "message": {
                        "text": _text
                    }
                })
                # status = requests.post(
                #     post_message_url,
                #     headers={"Content-Type": "application/json"},
                #     data=response_msg)
                return HttpResponse()

            if incoming_message['entry'][0]['messaging'][0]['postback']['payload'] == 'BULB_OFF':
                _broker(_id, 'house/bulb1', 'off')
                _text = 'Server: bulb turned off'
                listner(_id, username, password, broker, port)

                response_msg = json.dumps({
                    "recipient": {
                        "id": _id
                    },
                    "message": {
                        "text": _text
                    }
                })
                # status = requests.post(
                #     post_message_url,
                #     headers={"Content-Type": "application/json"},
                #     data=response_msg)
                return HttpResponse()
