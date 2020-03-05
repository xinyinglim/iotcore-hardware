from RpiMotorLib import RpiMotorLib

import RPi.GPIO as GPIO
from time import sleep
from iot import *
import json



stepper_registry_id = "stepper"

#{"new_positon": "A"}

class DeviceStepper:

    def get_client(self):
        return get_client( project_id, cloud_region, stepper_registry_id, self.device_id,
        self.private_key_path, algorithm, ca_certs, mqtt_bridge_hostname,
        mqtt_bridge_port, self.on_message)

    def on_message(self,unused_client, unused_userdata, message):
        print("received message")
        print(message.topic)    
        payload = message.payload.decode("utf-8")

        if message.topic == self.mqtt_config_topic :
            print("received new config")
            config = json.loads(payload)
            print(config)
            if "new_pos" not in config:
                print("'new_pos' property not in config")
                return
            print("moving")
            print(config["new_pos"])
            if not self.initialized :
                self.current_position = config["new_pos"]
                self.initialized = True
            else:
                self.move_to(config["new_pos"])
            print(payload)
        elif message.topic == self.mqtt_command_topic:
            print("received new command")
            print(payload)


    def __init__(self, pin1, pin2, pin3, pin4, section_positions, start_pos, device_id, private_key_path):
        if len(section_positions) == 0 :
            raise Exception("Must have at least one section position")
        self.gpioPins = [pin1, pin2, pin3, pin4]
        self.section_positions = section_positions
        self.current_position = start_pos
        self.stepper = RpiMotorLib.BYJMotor("StepperMotor", "28BYJ")
        self.wait_time = 0.01
        self.verbose = False
        self.step_type = "full"
        self.initial_delay = .5
        self.device_id = device_id
        self.private_key_path = private_key_path
        self.client = self.get_client()
        self.mqtt_config_topic = '/devices/{}/config'.format(self.device_id)
        self.mqtt_command_topic = '/devices/{}/commands'.format(self.device_id)
        self.initialized = False


    def move_to(self, new_pos):
        if new_pos not in self.section_positions:
            print ("Invalid position: '{}'".format(new_pos))
        num_steps, counterclockwise = self.calculate_steps_between(self.current_position, new_pos)
        self.current_position = new_pos
        print("Moving {} steps, counterclockwise: {}".format(num_steps, counterclockwise))
        try :
            self.stepper.motor_run(self.gpioPins, self.wait_time, num_steps, counterclockwise,self.verbose,self.step_type, self.initial_delay)
            sleep(1)
        except KeyboardInterrupt:
            print("Interrupted")
            GPIO.cleanup()
       
        
    def cleanup(self):
        GPIO.cleanup()

    def calculate_steps_between (self, position1, position2):
        # returns two arguments  number of steps for stepper to take, and T
        if position1 not in self.section_positions or position2 not in self.section_positions:
            raise Exception ("Invalid positions A: {} and/or B: {}".format(position1, position2))
        if position1 == position2:
            return 0, True
        step_difference = self.section_positions[position2] - self.section_positions[position1]
        counter_clockwise = True
        if step_difference < 0 :
            counter_clockwise = False
        return abs(step_difference), counter_clockwise

    