#!/bin/bash

python3 request_client.py 1 &
python3 request_client.py 2 &
python3 request_client.py 3 &
python3 request_client.py 4 &
python3 request_client.py 5 &

# python3 request_client.py > /dev/null 2>&1 &

