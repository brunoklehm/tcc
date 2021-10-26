import random
import time
import json

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "devices/sensors"
#username = ''
#password = ''

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

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
    while True:
        time.sleep(1)
        msg = get_data()
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

def get_data():
  data = {}
  data['application_type'] = random.randint(0, 3)
  data['data_1'] = random.randint(0, 10000000)
  data['data_2'] = random.randint(0, 10000000)
  data['data_3'] = random.randint(0, 10000000)
  data['client_id'] = client_id

  msg = json.dumps(data)
  return msg

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()