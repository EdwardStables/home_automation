#!/usr/bin/env python3

import argparse
from system_base import Coffee
from mqtt_wrapper import mqtt_subscriber
from time import sleep

def get_args():
    parser = argparse.ArgumentParser(description="Run server in background for automation system")
    parser.add_argument("-n", dest="hostname", type=str, default="localhost", help="Hostname")
    parser.add_argument("-p", dest="port", type=int, default=8080, help="Port")
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    hostname = args.hostname
    port = args.port

    systems = [
        Coffee(mqtt_subscriber(hostname, port))
    ]

    while True:
        sleep(1)


if __name__ == "__main__":
    main()
