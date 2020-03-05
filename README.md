# Connecting Raspberry Pi to Cloud IoT Core

This is part of the IoT Cafe Project.

These programs are loaded into Raspberry Pis that are connected to hardware.

The Raspberry Pis open a connection with Cloud IoT Core and wait for configuration updates.

3 hardware types are supported at the moment:
- Servo (an umbrella)
- DC Motor (a fan)
- Stepper Motor (a recommendation system)

In the context of the IoT Cafe, whenever there is a change in weather, IoT Core will send new configuration changes to the raspberry pi which will then adjust the hardware accordingly.

# How to use
1. Create key from devices in IoT Core
 - Keys are labelled 
    - dcmotor_rsa_private.pem
    - dht11_rsa_private.pem
    - servo_rsa_private.pem
    - stepper_rsa_private.pem
2. Save keys in keys folder
3. Assemble hardware with Raspberry Pi
4. Change Project ID
5. Run python programs
    - iotcontrol_fan.py
    - iotcontrol_menu.py
Fan will control Fan and umbrella hardware
Menu will control Menu recommendation system hardware