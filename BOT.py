import requests as r
import random

print("I'm ON!")

messages = ['hello', 'lmao', 'sub2pew']
PEW_LIST = ['subs', 'pew', 'pewds', 'pewdiepie', 'sub2pewds', 'sub']

url = 'https://api.telegram.org/bot697406604:AAH-1LwBWuUJ6STTtHif1de7xyXuc45TQdk/'


def get_(offset=None, timeout=30):
    method = 'getUpdates'
    params = {'timeout': timeout, 'offset': offset}
    resp = r.get(url + method, params)
    result = resp.json()
    return result


def send_(chat_id, text):
    method = 'sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    resp = r.post(url + method, params)
    return resp


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


def difference():
    P = sub_count('p')
    T = sub_count('t')
    p = P[1]
    t = T[1]

    if p >= t:
        leader = 'PewDiePie'
        loser = 'T-series'
        diff = p - t
        emoji = u'\U00002705'*3
    elif t > p:
        leader = 'T-series'
        loser = 'PewDiePie'
        diff = t - p
        emoji = u'\U0001F6A8'*3

    num = '{:,d}'.format(int(diff))

    result = (
            'PewDiePie has {} subscribers.'.format(P[0]) + '\n' +
            'T-series has {} subscribers.'.format(T[0]) + '\n' +
            '{} is ahead of {} for {} subscribers!{}'.format(leader, loser, num, emoji)
    )

    return result


def main():

    new_offset = None

    while True:
        update = get_(new_offset)
        try:
            update['result'][0]['message']
        except IndexError:
            print('no data')
            continue
        update_plus = update['result'][0]

        update_id = update_plus['update_id']
        chat_text = update_plus['message']['text']
        chat_id = update_plus['message']['chat']['id']
        name = update_plus['message']['chat']['first_name']

        if chat_text.lower() in PEW_LIST:
            text = difference()
            send_(chat_id, text)

        else:
            i = random.randint(0, len(messages)-1)
            text = messages[i]
            send_(chat_id, '{} this text for you, {}! '.format(text, name) + u'\U0000270C')

        new_offset = update_id +1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
