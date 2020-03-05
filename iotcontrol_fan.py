from iot import *
# units are in cm for showcase
from gpiozero import DistanceSensor, LED
from time import sleep
import datetime
from main_servo import DeviceServo
from iotdevice import *
from main_dcmotor import DCMotor
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#dcmotor

device_id = "dcmotor1"
dcmotor_private_key_file = "./keys/dcmotor_rsa_private.pem"

dcmotor_input1_pin = 2
dcmotor_input2_pin = 3
dcmotor_enable_pin = 4
dcmotor = DCMotor(dcmotor_input1_pin,dcmotor_input2_pin,dcmotor_enable_pin, device_id, dcmotor_private_key_file)




servo_device_id = "servo1"
servo_registry_id = "servo"
servo_private_key_file = "./keys/servo_rsa_private.pem"
servo_gpio = 22
servo = DeviceServo(servo_gpio,servo_device_id,servo_private_key_file)

# #todo move some functions into servo class
# def servo_on_message(unused_client, unused_userdata, message):
#     print("received message")
#     print(message.topic)    
#     payload = str(message.payload)
#     print(payload)

#     if message.topic == servo_mqtt_config_topic :
#         print("received new config")
#         print(payload)
#     elif message.topic == servo_mqtt_command_topic:
#         print("received new command")
#         print(payload)


# def servo_get_client():
#     return get_client( project_id, cloud_region, servo_registry_id, servo_device_id,
#         servo_private_key_file, algorithm, ca_certs, mqtt_bridge_hostname,
#         mqtt_bridge_port, servo_on_message)


# # todo move up
# servo_client = servo_get_client()


# def listenToSubscription():
#     # from listen_for_messages
#     # if receives a status change message, update variable
#     # update: house_boundary
#     # update: alarm_active
#     global minimum_backoff_time
#     jwt_iat = datetime.datetime.utcnow()
#     jwt_exp_mins = jwt_expires_minutes
#     # Use gateway to connect to server
#     client = get_client(
#         project_id, cloud_region, registry_id, device_id,
#         private_key_file, algorithm, ca_certs, mqtt_bridge_hostname,
#         mqtt_bridge_port)
#     # while True:
#     #     client.subscri

try:
    while True:
    # post_telemetry(servo_client, servo_get_client, servo_device_id, b'{"testing": True}')
        sleep(50)
except KeyboardInterrupt:
    dcmotor.stop()
    # servo_client.disconnect()
    # servo_client.loop_stop()
    GPIO.cleanup()
