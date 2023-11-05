import redis
import json
import logging
from argparse import ArgumentParser

def main():
    logging.basicConfig(level=logging.ERROR)
    parser = ArgumentParser()
    parser.add_argument("-e", "--evil", help = "Enter evils as follow [12..90,12..90] with exact 10 digits", type = str)
    args = parser.parse_args()
    evils = []
    if args.evil:
        evils = args.evil.split(",")
        evils = list(filter(lambda ret: (len(ret) == 10), evils))
    logging.info(evils)
    try:
        red = redis.Redis()

        ps = red.pubsub()
        ps.subscribe("data_channel")

        for msg in ps.listen():
            if msg["type"] == "message":
                recieved = json.loads(msg["data"])
                if recieved["amount"] > 0:
                    if recieved["metadata"]["from"] not in evils and recieved["metadata"]["to"] in evils:
                        recieved["metadata"]["from"], recieved["metadata"]["to"] = recieved["metadata"]["to"], recieved["metadata"]["from"]
                else:
                    if recieved["metadata"]["from"] in evils and recieved["metadata"]["to"] not in evils:
                        recieved["metadata"]["from"], recieved["metadata"]["to"] = recieved["metadata"]["to"], recieved["metadata"]["from"]
                print(recieved)
                # logging.info(recieved)
    except redis.exceptions.ConnectionError as e:
        logging.error("Redis server is offline or has non-standart config")
    except Exception as e:
        logging.error("Whoops. Something went wrong")
    except KeyboardInterrupt as e:
        print("Exit()")

if __name__ == "__main__":
    main()