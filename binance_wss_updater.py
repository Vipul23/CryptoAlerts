import asyncio
import websockets
import os
import json
import redis


class redis_op(object):
    def __init__(self):
        self.r = self.connect()
        self.persist_dict = self.load()

    def save(self):
        self.r.hset(redis_key, mapping=self.persist_dict)

    def load(self):
        persist_dict = self.r.hgetall(redis_key)
        if persist_dict:
            persist_dict = {k.decode('utf-8'): v.decode('utf-8') for k, v in persist_dict.items()}
        else:
            persist_dict = {}
        return persist_dict

    def connect(self):
        REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        return redis.Redis(host=REDIS_HOST, port=6379)

async def binance_wss_data():
    redis_instance = redis_op()
    backoff_time = 1
    curr_backoff = False
    while True:
        try:
            async for websocket in websockets.connect('wss://stream.binance.com:9443/ws/!miniTicker@arr', ping_interval=60, ping_timeout=180):
                while True:
                    # os.system('clear')
                    if backoff_time > 1 and curr_backoff:
                        print(f"Reconnecting in {backoff_time} seconds")
                        curr_backoff = False
                    data = json.loads(await websocket.recv())
                    number_of_objects = len(data)
                    for i in data:
                        redis_instance.persist_dict[i['s']] = i['c']
                    redis_instance.save()
                    # print(str(number_of_objects)+" Updated")
                    await asyncio.sleep(2)
        except websockets.exceptions.ConnectionClosedOK:
            print("WebSocket connection closed")
            await asyncio.sleep(backoff_time)
            backoff_time *= 2
            curr_backoff = True
        except websockets.exceptions.ConnectionClosed as e:
            print(f"WebSocket connection closed : {e}")
            await asyncio.sleep(backoff_time)
            backoff_time *= 2
            curr_backoff = True
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"WebSocket connection closed with error: {e}")
            await asyncio.sleep(backoff_time)
            backoff_time *= 2
            curr_backoff = True
        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(backoff_time)
            backoff_time *= 2
            curr_backoff = True

redis_key = ':1:binance_data'
asyncio.get_event_loop().run_until_complete(binance_wss_data())