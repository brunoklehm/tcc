import random
import time
import json
import asyncio

from paho.mqtt import client as mqtt_client

from types import SimpleNamespace


broker = 'broker.emqx.io'
port = 1883
topic = "devices/edge"
#username = ''
#password = ''

# generate client ID with pub prefix randomly
client_id = f'sensor-mqtt-{random.randint(0, 1000)}'

device_list = []

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msgs = []
    for x in range(0, 3):
        for y in range(0, 10):
            msgs.append(get_data(x))

    for msg in msgs:
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

        time.sleep(1)
        


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(str(msg.topic))
        if (msg.topic == "devices/edge"):
            print("teste")
            # Add device information to the list of devices
            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            add_device(msg.payload.decode())

    client.subscribe("devices/edge")
    client.on_message = on_message


def add_device(msg):
    # transforms the json into a python object
    device = json.loads(msg, object_hook=lambda d: SimpleNamespace(**d))

    # Inserts the device if not in list
    if not any(x.client_id == device.client_id for x in device_list):
        device_list.append(device)
        print("Device added to the list: " + str(device.client_id))


# Based on the data of all devices, it returns the best node to process the data
def select_best_node():
    # Tablet -> Datacenter -> Cloud
    # Aplicação -> Dispositivo -> Rede
    # Verificar primeiro a aplicação
    for device in device_list:
        print(device)


def get_data(application_type):
  data = {}
  data['application_type'] = application_type
  data['data_1'] = random.randint(0, 10000000)
  data['data_2'] = random.randint(0, 10000000)
  data['data_3'] = random.randint(0, 10000000)
  data['client_id'] = client_id

  msg = json.dumps(data)
  return msg

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()