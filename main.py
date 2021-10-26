import random
import json
import psutil
import config

from paho.mqtt import client as mqtt_client
from icmplib import async_ping


# MQTT Connection Settings
broker = config.mqtt['broker']
port = config.mqtt['port']
topic = config.mqtt['topic']
username = config.mqtt['username']
password = config.mqtt['password']

# Generates a random client ID
client_id = f'python-mqtt-{random.randint(0, 1000)}'

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


# Gets the information of the device at the current moment
def get_device_data():
    data = {}
    data['cpu_percentage'] = psutil.cpu_percent(1) # CPU Percentage
    data['cpu_frequency'] = psutil.cpu_freq().max # CPU Frequency
    data['cpu_count'] = psutil.cpu_count() # CPU Count
    data['memory_percentage'] = psutil.virtual_memory()[2] # Memory Percentage
    # pegar total de GBs da memoria?
    # data['network_ip_address']
    # data['disk_usage']
    # data['battery_level']
    # data['network_speed']
    # data['cloud_latency']
    # data['location'] ? não sei se é possível pegar esse tipo de informação com o psutil
    data['application_type'] = config['application_type']
    # more to be added

    msg = json.dumps(data)
    return msg


# Function that checks latency with cloud regularly
async def check_cloud_latency():
    await ping_server()


def ping_server():
    async_ping("8.8.8.8", count=4, interval=1, timeout=2, id=None, source=None, family=None, privileged=True)

def select_best_node():
    # Aplicação -> Dispositivo -> Rede
    # Verificar primeiro a aplicação
    pass


# Main function
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    while True:
        msg = get_device_data()
        result = client.publish(topic, msg)

        # check_cloud_latency()

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


if __name__ == '__main__':
    run()

# Tablet, Gateway e Cloud