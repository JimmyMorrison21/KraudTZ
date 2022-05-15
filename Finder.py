import asyncio
import json
import websockets

"""
* Получать цены с binance (по rest или ws), в синхронном или асинхронном режиме (выбор обосновать)
* Сравнивать их с ценами из конфига (будет в файле формата json)
* Если цена соответствует условию из конфига, слать нотификацию в тг
* По возможности покрыть код тестами
"""

##Берем информацию из конфига
with open("config.json", "r") as read_file:
    loaded_json_file = json.load(read_file)

dict(loaded_json_file).keys()
val = [x.replace('/', '') for x in dict(loaded_json_file).keys()]
vals = [x.lower() for x in val]
print(vals)
## Работать будем через ws, тк слишком много информации придется обрабатывать (тратим очень много времени с
# использованием requests (это будет не оптимально, тк цена валюты очень быстро меняется))
val = 'ethusdt'
socket = f'wss://stream.binance.com:9443/stream?streams={val}@miniTicker'
sockets = []
for i in vals:
    sockets.append(f'wss://stream.binance.com:9443/stream?streams={i}@miniTicker')



async def main():
    async with websockets.connect(sockets[0]) as client:
        n = 0
        while True:
            n += 1
            data = json.loads(await client.recv())['data']
            if float(data ['c']) > float(loaded_json_file['BTC/USDT']['price']):
                print(f"Вот это да BTC/USDT {sockets[0]}!")
                break
            if n == 10 :
                break

    async with websockets.connect(sockets[1]) as client:
        n = 0
        while True:
            n += 1
            data = json.loads(await client.recv())['data']
            if float(data ['c']) < float(loaded_json_file['ETH/BTC']['price']):
                print(f"Вот это да ETH/BTC {sockets[1]}!")
                break
            if n == 10 :
                break
    async with websockets.connect(sockets[2]) as client:
        n = 0
        while True:
            n += 1
            data = json.loads(await client.recv())['data']
            if float(data ['c']) >= float(loaded_json_file['DOT/USDT']['price']):
                print(f"Вот это да DOT/USDT {sockets[2]}!")
                break
            if n == 10:
                break
    async with websockets.connect(sockets[3]) as client:
        n = 0
        while True:
            n += 1
            data = json.loads(await client.recv())['data']
            if float(data ['c']) <= float(loaded_json_file['ETH/USDT']['price']):
                print(f"Вот это да ETH/USDT {sockets[3]}!")
                break
            if n == 10:
                break




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())