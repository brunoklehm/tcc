import random
import json
import psutil

from paho.mqtt import client as mqtt_client

# MQTT Connection Settings
broker = 'broker.emqx.io'
port = 1883
topic = "devices/information"
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'user'
# password = 'pass'


# Connects to MQTT Broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)

    # Only needed if MQTT broker has username as password set
    #client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# Subscribes to the MQTT Topic
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def get_device_data():
    data = {}
    data['cpu'] = psutil.cpu_percent(1)
    data['memory'] = psutil.virtual_memory()[2]

    msg = json.dumps(data)

    return msg


# Main function
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    while True:
        msg = get_device_data()
        result = client.publish(topic, msg)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


if __name__ == '__main__':
    run()
