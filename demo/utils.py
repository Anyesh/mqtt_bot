import requests
import json
import random


def response_message(_id, _text):
    res_msg = json.dumps({
        "recipient": {
            "id": _id
        },
        "message": {
            "text": _text
        }
    })

    return res_msg


def get_started(post_message_url, _id, user_details):

    _text = 'Hello ' + user_details['first_name'] + \
        '! ' + 'welcome to MQTT Bot'
    response_msg = response_message(_id, _text)

    status = requests.post(
        post_message_url,
        headers={"Content-Type": "application/json"},
        data=response_msg)


def nlp_replies(incoming_message, msg, _id, user_details, post_message_url):
    if 'text' in msg:
        message = incoming_message['entry'][0]['messaging'][0]['message']['text']

    elif 'attachments' in msg:
        message = incoming_message['entry'][0]['messaging'][0]['message']['attachments']

    if 'nlp' in msg:
        entity = incoming_message['entry'][0]['messaging'][0]['message']['nlp']['entities']
        if 'greetings' in entity:
            conf = incoming_message['entry'][0]['messaging'][0]['message']['nlp']['entities']['greetings'][0]['confidence']
            print(conf)
            if float(conf) > 0.85:
                message_reply(post_message_url, _id,
                              user_details, ctx='greetings')

        elif 'thanks' in entity:
            conf = incoming_message['entry'][0]['messaging'][0]['message']['nlp']['entities']['thanks'][0]['confidence']
            print('Confidence level:', conf)
            if float(conf) > 0.85:
                message_reply(post_message_url, _id,
                              user_details, ctx='thanks')

        elif 'bye' in entity:
            conf = incoming_message['entry'][0]['messaging'][0]['message']['nlp']['entities']['bye'][0]['confidence']
            print(conf)
            if float(conf) > 0.85:
                message_reply(post_message_url, _id, user_details, ctx='bye')
        else:
            error_response(post_message_url, _id)
    else:
        error_response(post_message_url, _id)


def message_reply(post_message_url, _id, user_details, ctx):
    context = {
        'greetings':
        ['Hello ' + user_details['first_name'] + '! ' + 'what can i do for you?',
         'Hii ' + user_details['first_name'] +
         '! ' + 'How are you doing?',
         'Oh hi ' + user_details['first_name'] + ':)',
         """Hello there :)""",
         """hey hey :)"""],

        'thanks': ['Never mind :)', 'Ok :)', 'pleasure :)'],

        'bye': ['have a good time :)', 'sure!! :)', 'biee!! :)']
    }

    _text = random.choice(context[str(ctx)])
    response_msg = response_message(_id, _text)

    status = requests.post(
        post_message_url,
        headers={"Content-Type": "application/json"},
        data=response_msg)


def error_response(post_message_url, _id):

    msgs = {'errors': ['I dont think i understand what you said.', 'Sorry, i didnt get you', 'Sorry i didnt understand what you said.']}
    _text = random.choice(msgs['errors'])

    response_msg = response_message(_id, _text)

    status = requests.post(
        post_message_url,
        headers={"Content-Type": "application/json"},
        data=response_msg)
