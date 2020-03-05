from gpiozero import Servo
from time import sleep
from threading import Thread, Event
from iot import *
import json

servo_registry_id = "servo"
servo_topic_name = "projects/"+ project_id +"/topics/servo"


## config
#  {"motion_type" : "wave"}
#  {"motion_type" : "move_pos", "pos" : -1}

class DeviceServo:

    def get_client(self):
        return get_client( project_id, cloud_region, servo_registry_id, self.device_id,
        self.private_key_path, algorithm, ca_certs, mqtt_bridge_hostname,
        mqtt_bridge_port, self.on_message)

    def on_message(self,unused_client, unused_userdata, message):
        print("received message")
        print(message.topic)    
        payload = message.payload.decode("utf-8") 
        print(payload)

        if message.topic == self.mqtt_config_topic :
            print("received new config")
            print(payload)
            try:
                config = json.loads(payload)
                self.process_new_config(config)
            except json.JSONDecodeError:
                print("Unable to decode JSON: Invalid json string : {}".format(payload))

    def process_new_config(self,config):
        print("process new config")
        #{ motion_type: "wave" / "move_pos", pos: -1 -> 1}
        if "motion_type" not in config :
            print ("'motion_type' property is not found in config")
            return
        print("pass")
        print (config)
        print(config["motion_type"])
        if config["motion_type"] == "wave":
            print("starting wave")
            self.start_wave()
        elif config["motion_type"] == "move_pos":
            print("moving pos")
            if "pos" not in config:
                print("'pos' is not specified for move_pos config")
                return
            print("moving pos")
            self.move_position(config["pos"])
        else:
            print (" new motion type: '{}', functionality to be added".format(config["motion_type"]))
        print ("end")


    def __init__(self,pin, device_id, private_key_path):
        self.servo = Servo(pin)
        self.thread = None
        self.event = None
        self.device_id = device_id
        self.private_key_path = private_key_path
        self.client = self.get_client()
        self.mqtt_config_topic = '/devices/{}/config'.format(device_id)
        self.mqtt_command_topic = '/devices/{}/commands'.format(device_id)


    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()
        if self.event != None:
            self.event.set()
            self.thread.join()
            self.thread = None
            self.event = None
        self.move_position(0)
    
    def start_wave(self):
        print("beginning wave")
        def wave():
            while True:
                if self.event.isSet():
                    break
                else:
                    self.servo.max()
                    sleep(1)
                    self.servo.min()
                    sleep(1)
        if self.event != None:
            self.event.set()
            self.thread.join()
        self.thread = Thread(target = wave)
        self.event = Event()
        self.thread.start()

    def move_position(self, pos):
        print("moving to position: {}".format(pos))
        # position is between 1 and -1
        if pos < -1 or pos > 1 :
            raise Exception("Invalid pos: {}".format(pos))
        if self.event != None:
            self.event.set()
            self.thread.join()
        self.thread = None
        self.event = None
        if pos == 1 :
            self.servo.min()
        else:
            self.servo.max()
        
        # self.servo.value = pos

        
# creating an instance
# servo_gpio=4
# servo_device_id = "servo1"
# servo_private_key_file = "./keys/servo_rsa_private.pem"
# servo = DeviceServo(servo_gpio,servo_device_id,servo_private_key_file)
