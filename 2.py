import requests

f = open('out.json', 'w')

r = requests.get('https://api.telegram.org/bot717856084:AAE1F0ZN5nrEfdsNO8GBcUI4PyTnqSxa5Ig/getUpdates')
r = r.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]


print(r)
print(str(r))

try:
    f.write(r)
except:
    print("I can't")
f.close()

print('////////////////////')
print('\n')
print(last_update(r)['message']['chat']['username'])
