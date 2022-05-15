import asyncio
import json
import websockets
import telebot

"""
* Получать цены с binance (по rest или ws), в синхронном или асинхронном режиме (выбор обосновать)
* Сравнивать их с ценами из конфига (будет в файле формата json)
* Если цена соответствует условию из конфига, слать нотификацию в тг
* По возможности покрыть код тестами
"""
# Настроим бота и выцепим chat id
token = '5141312344:AAGEN-QQjtsdxsFShNGoTnTs9_2WbNQPaow'
bot = telebot.TeleBot(token)
id = None


@bot.message_handler(commands=['Start', 'Hello', 'start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я тут тестовое задание прохожу")
    global id
    id = message.chat.id


##Берем информацию из конфига
with open("config.json", "r") as read_file:
    loaded_json_file = json.load(read_file)

val = [x.replace('/', '') for x in dict(loaded_json_file).keys()]
vals = [x.lower() for x in val]
## Работать будем через ws, тк слишком много информации придется обрабатывать (тратим очень много времени с
# использованием requests (это будет не оптимально, тк цена валюты очень быстро меняется))
# тк у нас есть 4 разных валютных пары будем решать эту задачу асинхронно
sockets = []
for i in vals:
    sockets.append(f'wss://stream.binance.com:9443/stream?streams={i}@miniTicker')


# В этой функции реализуем логику, которая отбирает, пары соглано конфигу
def tick_find(name, price):
    for key in loaded_json_file.keys():
        if name == key.replace('/', ''):
            if loaded_json_file[key]['trigger'] == 'more':
                if float(price) > float(loaded_json_file[key]['price']):
                    return (f'Вот Это да ! {name} по цене {price}')
            if loaded_json_file[key]['trigger'] == 'less':
                if float(price) < float(loaded_json_file[key]['price']):
                    return (f'Вот Это да ! {name} по цене {price}')
            if loaded_json_file[key]['trigger'] == 'more_eq':
                if float(price) >= float(loaded_json_file[key]['price']):
                    return (f'Вот Это да ! {name} по цене {price}')
            if loaded_json_file[key]['trigger'] == 'less_eq':
                if float(price) <= float(loaded_json_file[key]['price']):
                    return (f'Вот Это да ! {name} по цене {price}')


async def main(socket):
    async with websockets.connect(socket) as client:
        while True:
            data = json.loads(await client.recv())['data']
            x = tick_find(name=data['s'], price=data['c'])
            if x:
                print(x)
                bot.send_message(chat_id=id, text=x)
                await asyncio.sleep(1800
                    )  # Чтобы бот не довел нас до инсульта своими оповещениями, настроим отправку каждые 30 мин


async def steck():
    tasks = []
    for socket in sockets:
        tasks.append(main(socket))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(steck())
    loop.close()
