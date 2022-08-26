import requests
from bs4 import BeautifulSoup as BS
import telebot
from lxml import etree
from telebot import types

bot = telebot.TeleBot('5549293536:AAFGeLKzICrYmyxDt74vXXjzJzoDBqmf23s')
url_exc = 'https://minfin.com.ua/ua/currency/auction/exchanger/usd/sell/kiev/'
url_bank = 'https://minfin.com.ua/ua/company/privatbank/currency/'


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Bot currency exchange ready on Work.")



@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кращий курс в обмінниках")
    item2 = types.KeyboardButton('Курс в банку')

    markup.add(item1)
    markup.add(item2)

    bot.send_message(message.chat.id, 'Виберіть що потрібно ', reply_markup=markup)


@bot.message_handler()
def send_exchange(message):
    if message.text == 'Кращий курс в обмінниках':
        bot.send_message(message.chat.id, parse_site_rate())
    elif message.text == 'Курс в банку':
        bot.send_message(message.chat.id, parse_site_bank())
    else:
        bot.send_message(message.chat.id, 'Not today, man.')


def parse_site_rate():
    response = requests.get(url=url_exc)

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
        i += 1
        return f'Курс:{rate_usd}, за адресою: {address}'

def parse_site_bank():
    response = requests.get(url=url_bank)

    soup = BS(response.text, 'html.parser')

    dom = etree.HTML(str(soup))
    my_list = dom.xpath('/html/body/main/div/div/div[1]/div/div/div/div/div[2]/div[3]/table[3]/tbody/tr[1]/td[3]')[0].text.strip()
    print(f'Курс в ПриватБанк {my_list} USD.')
    return f'Курс в ПриватБанк {my_list} USD.'


if __name__ == '__main__':
    bot.polling(none_stop=True)
