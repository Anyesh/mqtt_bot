import time
import paho.mqtt.client as mqtt


broker = 'vps.datalogy.asia'
port = 1883

username = 'inno'
password = 'vake'

# broker = 'iot.eclipse.org'
# port = 1883
# def on_connect(client, userdata, flags, rc):
#   print("Connected with result code "+str(rc))
#   client.subscribe("report")

def on_message(client, userdata, msg):
    print(msg.payload.decode())
    client.disconnect()
    client.loop_stop()


def _broker(client_id, sub, state):

    client = mqtt.Client(client_id)
    print('Client:', client_id)
    print('Subscribed to:', sub)
    print('state:', state)

    # client.on_message = on_message
    client.username_pw_set(username, password)
    client.connect(broker, port)
    client.loop_start()

    client.subscribe(sub)

    client.publish(sub, state)

    client.disconnect()
    client.loop_stop()




