from iot import *
from time import sleep

# get_client should have configurable on message
# on any message aka config, should update the device



def post_telemetry(device_client, get_client_func, device_id, payload):
    """Connects a device, sends data, and receives data."""
    # [START iot_mqtt_run]
    global minimum_backoff_time
    global MAXIMUM_BACKOFF_TIME

    # Publish to the events or state topic based on the flag.
    sub_topic = 'events'

    mqtt_topic = '/devices/{}/{}'.format(device_id, sub_topic)

    jwt_iat = datetime.datetime.utcnow()
    jwt_exp_mins = jwt_expires_minutes

    # Publish num_messages messages to the MQTT bridge once per second.
    # Process network events.
    device_client.loop()

    # Wait if backoff is required.
    if should_backoff:
        # If backoff time is too large, give up.
        if minimum_backoff_time > MAXIMUM_BACKOFF_TIME:
            print('Exceeded maximum backoff time. Giving up.')
            return

        # Otherwise, wait and connect again.
        delay = minimum_backoff_time + random.randint(0, 1000) / 1000.0
        print('Waiting for {} before reconnecting.'.format(delay))
        sleep(delay)
        minimum_backoff_time *= 2
        device_client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    
    print('Publishing message: \'{}\''.format(payload))
    # [START iot_mqtt_jwt_refresh]
    seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
    if seconds_since_issue > 60 * jwt_exp_mins:
        print('Refreshing token after {}s'.format(seconds_since_issue))
        jwt_iat = datetime.datetime.utcnow()
        device_client = get_client_func()
    # [END iot_mqtt_jwt_refresh]
    # Publish "payload" to the MQTT topic. qos=1 means at least once
    # delivery. Cloud IoT Core also supports qos=0 for at most once
    # delivery.
    device_client.publish(mqtt_topic, payload, qos=1)

    # Send events every second. State should not be updated as often
