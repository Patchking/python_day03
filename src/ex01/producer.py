import redis
import json
import random
import logging
from argparse import ArgumentParser
from time import sleep

def generate_record(peoplelist) -> set:
    out = {
        "metadata": {
            "from": random.choice(peoplelist),
            "to": random.choice(peoplelist)
        },
        "amount": random.randint(500, 1000) * 10 * random.choice([1, -1])
    }
    return out
        
def get_people_list(filename: str):
    peoplelist = []
    try:
        with open(filename, "r") as file:
            for str in file:
                peoplelist.append(str.rstrip())
        if len(peoplelist) < 3:
            raise Exception
    except FileNotFoundError as e:
        logging.error(f"File not found in directory")
        exit()
    except Exception as e:
        logging.error(f"We have less then 3 human. Please add more in peoples")
    logging.debug(peoplelist)
    return peoplelist

def argument_parser():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help = "Enter file to load evils", type = str)
    args = parser.parse_args()
    peoplelist = []
    if args.file is not None:
        peoplelist = get_people_list(args.file)
    else:
        peoplelist = [
            "7576850395",
            "8261288157",
            "6017459946",
            "7428560441",
            "7696902557",
            "3310190761",
            "6697253929",
            "1111111111",
            "2222222222",
            "3333333333"
        ]
    return peoplelist
        
    

def main():
    logging.basicConfig(level=logging.INFO)
    peoplelist = argument_parser()

    try:
        red = redis.Redis()
        sleep(1)
        for i in range(10):
            send = json.dumps(generate_record(peoplelist))
            logging.info(f"Send next JSON: {send}")
            red.publish("data_channel", send)
            sleep(0.3)
    except redis.exceptions.ConnectionError as e:
        logging.eror("Redis server is offline or has non-standart config")

    


if __name__ == "__main__":
    main()