#!/bin/bash

python3.11 "producer.py" &
python3.11 "consumer.py" $1 $2
