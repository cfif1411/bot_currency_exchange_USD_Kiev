import requests
from bs4 import BeautifulSoup as BS
import telebot

bot = telebot.TeleBot('5549293536:AAFGeLKzICrYmyxDt74vXXjzJzoDBqmf23s')
url = 'https://minfin.com.ua/ua/currency/auction/exchanger/usd/sell/kiev/'

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Bot currency exchange ready on Work.")



@bot.message_handler()
def send_exchange(message):
    if message.text == 'exchange':
        bot.send_message(message.chat.id, parse_site_rate())
    else:
        bot.send_message(message.chat.id, 'Not today, man.')

def parse_site_rate():
    response = requests.get(url=url)

    soup = BS(response.text, 'html.parser')

    info_rate = soup.find_all('div', class_='card-note-wrapper')
    i = 0
    for item in info_rate:
        if i < 5:
            rate_usd = item.find('div', class_='Typography cardHeadlineL align').text
            address = item.find('span', class_='text-address').text



            print(f'Курс:{rate_usd}, за адресою: {address}')
        else:
            break
        i+=1
        return f'Курс:{rate_usd}, за адресою: {address}'


if __name__ == '__main__':
    bot.polling(none_stop=True)






