import requests as r
import random

token_bot = '697406604:AAH-1LwBWuUJ6STTtHif1de7xyXuc45TQdk/'
PEW_LIST = ['subs', 'pew', 'pewds', 'pewdiepie', 'sub2pewds', 'sub']
PHRASES = ['Hey!', 'LMAO']


class Bot:

    def __init__(self, token):
        self.token = token
        self.url = 'https://api.telegram.org/bot' + self.token

    def get_(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {timeout, offset}
        resp = r.get(self.url + method, params)
        return resp.json()

    def send_(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        resp = r.post(self.url + method, params)
        return resp



def fill_user_dict():
    global user_dict
    user_dict = {}
    with open('userFile.txt', 'r', encoding='utf-8') as user_file:
        for i in user_file:
            name = ''
            i = i.replace('\n', '')
            i = i.split()
            i.reverse()
            chat_id = i[0]
            i.reverse()
            i[-2] = i[-2][:-1]
            i = i[:-1]
            for j in i:
                name += j
            user_dict[chat_id] = name


def remember_(name, chat_id):
    if not (chat_id in user_dict):
        user_dict[chat_id] = name


def ssp_game(choice):
    global ssp_variants_list
    ssp_variants_list = ['stone', 'scissors', 'paper']
    choice = choice.lower()
    random_index = random.randint(0, 2)
    choice_random = ssp_variants_list[random_index]
    index_user = ssp_variants_list.index(choice)
    index_random = ssp_variants_list.index(choice_random)

    if index_random == index_user:
        winner = "no one, it's dare!"

    else:
        if index_user - index_random == 1:
            winner = 'Bot'
        elif index_user - index_random == -1:
            winner = 'you'

        if index_user - index_random == 2:
            winner = 'you'
        elif index_user - index_random == -2:
            winner = 'Bot'

    res = ("Yore choice is {}\n"
           "Bot choice is {}\n"
           "And wins... {}").format(choice, choice_random, winner)

    return res


def difference():

    def sub_count(who):
        part = 'statistics'
        key = 'AIzaSyCPI840NhCNzFvywCwW6plTaHaMxxPHDUk'

        if who == 'p':
            id = 'UC-lHJZR3Gqxm24_Vd_AJ5Yw'
            # PewDiePie
        elif who == 't':
            id = 'UCq-Fj5jknLsUf-MWSy4_brA'
            # T-series

        params = {'part': part, 'id': id, 'key': key}
        resp = r.get('https://www.googleapis.com/youtube/v3/channels', params)
        count = resp.json()["items"][0]["statistics"]["subscriberCount"]

        num = '{:,d}'.format(int(count))

        return [num, int(count)]


    P = sub_count('p')
    T = sub_count('t')
    p = P[1]
    t = T[1]

    if p >= t:
        leader = 'PewDiePie'
        loser = 'T-series'
        diff = p - t
        emoji = u'\U00002705' * 3
    elif t > p:
        leader = 'T-series'
        loser = 'PewDiePie'
        diff = t - p
        emoji = u'\U0001F6A8' * 3

    num = '{:,d}'.format(int(diff))

    result = (
            'PewDiePie has {} subscribers.'.format(P[0]) + '\n' +
            'T-series has {} subscribers.'.format(T[0]) + '\n' +
            '{} is ahead of {} for {} subscribers!{}'.format(leader, loser, num, emoji)
    )

    return result


def add_to_phrases(text):
    global PHRASES
    if text not in PHRASES:
        PHRASES.append(text)


def save_user_dict():
    with open('test.txt', 'w') as f:
        f.write('')

    values = list(user_dict.values())
    keys = list(user_dict.keys())

    for i in range(len(user_dict)):
        user_name = values[i]
        user_chat_id = keys[i]
        res = '{}: {}\n'.format(user_name, user_chat_id)
        with open('test.txt', 'a', encoding='utf-8') as f:
            f.write(res)


bot = Bot(token_bot)


def main():
    new_offset = None

    while True:
        updates = bot.get_(new_offset)
        updates_plus = updates['result'][0]
        try:
            updates_plus['message']
        except IndexError:
            print('no data')
            continue

        update_id = updates_plus['update_id']
        chat_id = update_plus['message']['chat']['id']
        name = update_plus['message']['chat']['first_name']
        try:
            chat_text = update_plus['message']['text']
        except KeyError:
            chat_text = ''

        if chat_text in PEW_LIST:
            text = difference()
            bot.send_(chat_id, text)

        elif chat_text in ssp_variants_list or chat_text == 'ssp':
            text = ssp_game(chat_text)
            bot.send_(chat_id, text)

        else:
            text = '{}, как тебе такое, {}?'.format(random.choice(PHRASES), name)
            bot.send_(chat_id, text)

        remember_(name, chat_id)
        add_to_phrases(chat_text)

        new_offset = update_id +1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        save_user_dict()
        exit()
