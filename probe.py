# import asyncio
# import json
# import websockets
#
# """
# * Получать цены с binance (по rest или ws), в синхронном или асинхронном режиме (выбор обосновать)
# * Сравнивать их с ценами из конфига (будет в файле формата json)
# * Если цена соответствует условию из конфига, слать нотификацию в тг
# * По возможности покрыть код тестами
# """
#
##Берем информацию из конфига
# with open("config.json", "r") as read_file:
#     loaded_json_file = json.load(read_file)
#
# dict(loaded_json_file).keys()
# val = [x.replace('/', '') for x in dict(loaded_json_file).keys()]
# vals = [x.lower() for x in val]
# print(vals)
# ## Работать будем через ws, тк слишком много информации придется обрабатывать (тратим очень много времени с
# # использованием requests (это будет не оптимально, тк цена валюты очень быстро меняется))
# sockets = []
# for i in vals:
#     sockets.append(f'wss://stream.binance.com:9443/stream?streams={i}@miniTicker')
#
#
#
# async def main(socket):
#     async with websockets.connect(socket) as client:
#         while True:
#             data = json.loads(await client.recv())['data']
#             for key in loaded_json_file.keys():
#                 if key =='BTC/USDT' and loaded_json_file[key]['trigger'] == 'more':
#                     if float(data['c']) > float(loaded_json_file[key]['price']):
#                         print(f"Вот это да {key} по цене {data['c']}!")
#                         break
#
#                 elif key =='ETH/BTC' and loaded_json_file[key]['trigger'] == 'less':
#                     if float(data['c']) < float(loaded_json_file[key]['price']):
#                         print(f"Вот это да {key} по цене {data['c']}!")
#                         break
#
#                 elif key =='DOT/USDT' and loaded_json_file[key]['trigger'] == 'more_eq':
#                     if float(data['c']) >= float(loaded_json_file[key]['price']):
#                         print(f"Вот это да {key} по цене {data['c']}!")
#                         break
#
#                 elif key =='ETH/USDT' and loaded_json_file[key]['trigger'] == 'less_eq':
#                     if float(data['c']) <= float(loaded_json_file[key]['price']):
#                         print(f"Вот это да {key} по цене {data['c']}!")
#                         break
#
#
#
# async def steck():
#     tasks = []
#     for socket in sockets:
#             tasks.append(main(socket))
#     await asyncio.gather(*tasks)
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(steck())
#     loop.close()
import requests

url = 'wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker'

connect = requests.get(url)
print(connect.status_code)