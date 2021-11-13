from asyncio.windows_events import NULL
import random
import json
import psutil
import config
import asyncio
import time

from types import SimpleNamespace


from paho.mqtt import client as mqtt_client
from icmplib import async_ping


# MQTT Connection Settings
broker = config.mqtt['broker']
port = config.mqtt['port']
topic = config.mqtt['topic']
username = config.mqtt['username']
password = config.mqtt['password']

# Generates a random client ID
client_id = f'device-mqtt-{random.randint(0, 100000)}'

device_list = []

# Connects to MQTT Broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)

    # Only needed if MQTT broker has username as password set
    # client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# Subscribes to the MQTT Topic
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        
        if (msg.topic == "devices/edge"):
            # Add device information to the list of devices
            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            add_device(msg.payload.decode())

        
        elif (msg.topic == "devices/sensors"):
            # Selects the best node to process data
            select_best_node()

    client.subscribe(topic)
    client.on_message = on_message


def add_device(msg):
    # transforms the json into a python object
    device = json.loads(msg, object_hook=lambda d: SimpleNamespace(**d))

    # Inserts the device if not in list
    if not any(x.client_id == device.client_id for x in device_list):
        device_list.append(device)
        print("Device added to the list: " + str(device.client_id))
        


# Gets the information of the device at the current moment
def get_device_data():
    data = {}
    data['client_id'] = client_id
    data['cpu_percentage'] = psutil.cpu_percent() # CPU Percentage
    data['cpu_frequency'] = psutil.cpu_freq().max # CPU Frequency
    data['cpu_count'] = psutil.cpu_count() # CPU Count
    data['memory_total'] = psutil.virtual_memory().total # Memory Total
    data['memory_percentage'] = psutil.virtual_memory().percent # Memory Percentage
    data['cloud_latency'] = asyncio.run(check_cloud_latency()) # Cloud Latency
    
    # Não está conseguindo pegar a porcentagem de uso de disco corretamente
    # data['disk_partitions'] = psutil.disk_partitions()
    # data['disk_usage'] = psutil.disk_usage(psutil.disk_partitions()[0][0]) # Disk Usage

    # data['network_ip_address']

    # Battery doesn't work on windows
    data['battery_level'] = psutil.sensors_battery().percent if psutil.sensors_battery() else NULL# Battery Percentage
    data['battery_remaining'] = psutil.sensors_battery().secsleft if psutil.sensors_battery() else NULL # Battery Seconds Remaining
    data['application_type'] = config.application_type # Application Type

    # data['location'] ? não sei se é possível pegar esse tipo de informação com o psutil
    # more to be added

    msg = json.dumps(data)
    return msg


# Function that checks latency with cloud regularly
async def check_cloud_latency():
    host = await async_ping(config.cloud_ip, count=1, interval=0.2)
    return host.avg_rtt
    # Fazer ping dos 3 dispositivos


# Based on the data of all devices, it returns the best node to process the data
def select_best_node():
    # Tablet -> Datacenter -> Cloud
    # Aplicação -> Dispositivo -> Rede
    # Verificar primeiro a aplicação
    for device in device_list:
        print(device)

# Graficos da máquina no tablet
# Graficos do site no datacenter
# Graficos da empresa na cloud
# Verifica aplicação
# Verifica dispositivo
# Verifica rede

# Resultado será a latencia geral

# Rodar uma vez pra nuvem = 30
# Rodar uma vez pro tablet = 10, 0ms
# Rodar uma vez pro datacenter = 10, 0.5ms
# Rodar uma vez pro cloud = 10, 2ms


# Main function
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    print("Algorithm started")
    while True:
        msg = get_device_data()
        result = client.publish(topic, msg)

        # result: [0, 1]
        status = result[0]

        if status == 0:
            # print(f"Send `{msg}` to topic `{topic}`")
            pass
        else:
            print(f"Failed to send message to topic {topic}")

        time.sleep(0.5)


# This is where it all starts :)
if __name__ == '__main__':
    run()


# Tablet, Gateway e Cloud