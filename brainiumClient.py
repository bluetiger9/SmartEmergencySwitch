import uuid

import paho.mqtt.client as mqtt
import sys

import logging
logging.basicConfig(level=logging.DEBUG)

import json

mqtt_user_name = 'oauth2-user'
mqtt_password = sys.argv[3]  # copy and paste here external client id from your account
user_id = sys.argv[1]  # copy and paste here your user id
device_id = sys.argv[2]  # copy and paste here your device id

print("user: " + user_id)
print("device: " + device_id)

alerts_topic = '/v1/users/{user_id}/in/alerts'.format(user_id=user_id)

alerts_topic_device_spec = '/v1/users/{user_id}/in/devices/{device_id}/datasources/alerts'.format(user_id=user_id, device_id=device_id)

pdm_events_topic_device_spec = '/v1/users/{user_id}/in/devices/{device_id}/datasources/PDM_EVENT'.format(user_id=user_id, device_id=device_id)

print("alerts topic: " + alerts_topic)
print("alerts topic device specific: " + alerts_topic_device_spec)

ca_cert_path = 'cacert.crt'


def on_connect(client, userdata, flags, rc):
    print('Connected with result code {code}'.format(code=rc))


def on_message(client, userdata, msg):
    print('Msg received from topic={topic}\n{content}'.format(topic=msg.topic, content=str(msg.payload)))
    decoded = json.loads(msg.payload.decode('utf-8'))
    #print(decoded)
    anomalyType = decoded['anomalyType']
    stateType = decoded['stateType']
    print("Anomaly Type: " + str(anomalyType))
    print("State Type: " + str(stateType))
    if anomalyType == "SPIKE" or anomalyType == "EXTENDED_DYNAMIC" or ("Clog" in stateType):
        print("Detected anomaly")
        anomalyCallback()

def main():
    client = mqtt.Client(client_id=str(uuid.uuid4()), transport='websockets')
    client.on_connect = on_connect
    client.on_message = on_message

    client.enable_logger()

    client.tls_set(ca_certs=ca_cert_path)
    client.username_pw_set(mqtt_user_name, mqtt_password)

    client.connect('ns01-wss.brainium.com', 443)

    #client.subscribe(alerts_topic)
    #client.subscribe(alerts_topic_device_spec)
    client.subscribe(pdm_events_topic_device_spec)
    #client.subscribe("#")

    client.loop_forever()


if __name__ == "__main__":
    main()

