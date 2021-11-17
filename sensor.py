from asyncio.windows_events import NULL
import random
import time
import json
import asyncio
import config

from paho.mqtt import client as mqtt_client

from types import SimpleNamespace


broker = config.mqtt['broker']
port = config.mqtt['port']
topic = "devices/sensor"
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

    while len(device_list) != 1:
        time.sleep(1)

    for msg in msgs:
        select_best_node(msg)

        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

        time.sleep(0.2)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if (msg.topic == "devices/edge"):
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

    # Updates the device data
    else:
        devices = device_list
        for index, item in enumerate(devices):
            if item.client_id == device.client_id:
                device_list[index] = device


# Based on the data of all devices, it returns the best node to process the data
def select_best_node(sensor_data):
    sensor = json.loads(
        sensor_data, object_hook=lambda d: SimpleNamespace(**d))
    devices = device_list

    selected_node = NULL

    filtered_devices = []

    # Tablet -> Datacenter -> Cloud
    # Aplicação -> Dispositivo -> Rede

    # Verifica primeiro o tipo de aplicação
    for device in devices:
        if(device.application_type == sensor.application_type):
            filtered_devices.append(device)

    # Se tiver dispositivos com o mesmo tipo de aplicação, filtra a lista
    if filtered_devices:
        devices = filtered_devices

    final_round = []

    # Verifica os dados da máquina e da rede
    for device in devices:
        cpu = device.cpu_percentage
        memory = device.memory_percentage
        battery = device.battery_level
        
        mp = ( ((cpu * 0.5) + (memory * 0.3) + (battery * 0.2)) / 1)

        d = (device.client_id, device.network_ip_address, mp)
        
        final_round.append(d)

    least_mp = 100

    for device in final_round:
        if device[2] < least_mp:
            least_mp = device[2]
            selected_node = device

    print(selected_node)

    return selected_node[1] # ip address


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
