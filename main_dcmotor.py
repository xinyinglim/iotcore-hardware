
#config : {"on" :  bool, "speed" : 0 -> 100}
from iot import *
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
import json



# config:
# {"on": true, "speed": 50}

# iot topic name is dcmotor

dcmotor_registry_id = "dcmotor"
dcmotor_topic_name = "projects/" + project_id + "/topics/dcmotor"



class DCMotor:
    def get_client(self):
        return get_client( project_id, cloud_region, dcmotor_registry_id, self.device_id,
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
                self.configure_dcmotor(config)
            except json.JSONDecodeError:
                print("Unable to decode JSON: Invalid json string : {}".format(payload))

           
        elif message.topic == self.mqtt_command_topic:
            print("received new command")
            print(payload)


    def __init__ (self, i1, i2, enable, device_id, private_key_path):
        self.i1 = i1
        self.i2 = i2
        self.enable = enable
        self.setup_dcmotor()
        self.device_id = device_id
        self.private_key_path = private_key_path
        self.client = self.get_client()
        self.mqtt_config_topic = '/devices/{}/config'.format(device_id)
        self.mqtt_command_topic = '/devices/{}/commands'.format(device_id)

    def setup_dcmotor(self, initial_speed = 0):
        GPIO.setup(self.i1, GPIO.OUT)
        GPIO.setup(self.i2, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)
        self.pwm = GPIO.PWM(self.enable, 50)
        self.pwm.start(0)
        GPIO.output(self.i1, True)
        GPIO.output(self.i2, False)
        GPIO.output(self.enable, True)
        self.pwm.ChangeDutyCycle(initial_speed)

    def off(self):
        print(self.pwm)
        self.pwm.ChangeDutyCycle(0)
        
    
    def on(self, speed):
        #speed must be between 0 and 100
        if speed < 0 and speed > 100:
            raise Exception("Speed is out of range") 
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        print(self.off())
        self.pwm.stop()

    def configure_dcmotor(self,config) : 
        if "on" not in config:
            print ("Missing argument: 'on'")
            return
        if not config["on"] :
            print("turning off")
            self.off()
            return
        if "speed" not in config:
            print ("'speed' not found in config, will use default of 50'")
            self.on(50)
            return
        elif "speed" in config and config["speed"] < 0 and config["speed"] > 100 :
            print ("Invalid value of speed : " + config["speed"])
        else :
            print("set speed")
            self.on(config["speed"])
            

# creating an instance  
# device_id = "dcmotor1"
# dcmotor_private_key_file = "./keys/dcmotor_rsa_private.pem"

# dcmotor = DCMotor(input1_pin,input2_pin,enable_pin, device_id, dcmotor_private_key_file)


        
        


