from telethon import TelegramClient
import pandas as pd
import details as ds
import os

# Login details #
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


def inputChannelName():
    while True:
        try:
            channelName = input("Please enter a Telegram channel name:\n")
            print(f'You entered "{channelName}"')
            answer = input('Is this correct? (y/n)')
            if answer == 'y':
                print('Scraping forwards from', channelName, 'This may take a while...')
                return channelName
        except():
            continue


print('Welcome to channel forward scraper.\n'
      'This tool will scrape a Telegram channel for all forwarded messages and '
      'their original sources.')

channel_name = inputChannelName()


async def main():
    lines = []
    async for message in client.iter_messages(channel_name):

        if message.forward is not None:
            try:
                from_id = message.forward.original_fwd.from_id
                if from_id is not None:
                    ent = await client.get_entity(from_id)
                    date = str(message.date.year) + "/" + str(message.date.month) + "/" + str(message.date.day)
                    time = str(message.date.hour) + ":" + str(message.date.minute)
                    # print(ent.title,">>>",channel_name)
                    df = pd.DataFrame(lines, columns=['To', 'From', 'date', 'time'])

                    name_clean = channel_name
                    alphanumeric = ""

                    for character in name_clean:
                        if character.isalnum():
                            alphanumeric += character

                    directory = './data/edgelists/'
                    try:
                        os.makedirs(directory)
                    except FileExistsError:
                        pass

                    file = './data/edgelists/' + alphanumeric + '_edgelist.csv'

                    with open(file, 'w+') as f:
                        df.to_csv(f)

                    lines.append([channel_name, ent.title, date, time])

            except():
                # print("An exception occurred: Could be private, now deleted, or a group.")
                pass


with client:
    client.loop.run_until_complete(main())


print('Forwards scraped successfully.')


next1 = input('Do you also want to scrape forwards from the discovered channels? (y/n)')
if next1 == 'y':
    # channel_name = inputChannelName()
    print('Scraping forwards from channels discovered in', channel_name, '...')


    async def new_main():
        name_clean = channel_name
        alphanumeric = ""

        for character in name_clean:
            if character.isalnum():
                alphanumeric += character
        df = pd.read_csv('./data/edgelists/' + alphanumeric + '_edgelist.csv')
        df = df.From.unique()
        lines = []

        for i in df:
            async for message in client.iter_messages(i):
                if message.forward is not None:
                    try:
                        from_id = message.forward.original_fwd.from_id
                        if from_id is not None:
                            ent = await client.get_entity(from_id)
                            date = str(message.date.year) + "/" + str(message.date.month) + "/" + str(message.date.day)
                            time = str(message.date.hour) + ":" + str(message.date.minute)
                            # print(ent.title,">>>", i)

                            df = pd.DataFrame(lines, columns=['To', 'From', 'date', 'time'])

                            name_clean = channel_name
                            alphanumeric = ""

                            for character in name_clean:
                                if character.isalnum():
                                    alphanumeric += character

                            directory = './data/edgelists/'
                            try:
                                os.makedirs(directory)
                            except FileExistsError:
                                pass

                            file1 = './data/edgelists/' + alphanumeric + '_net.csv'

                            with open(file1, 'w+') as f:
                                df.to_csv(f)

                            lines.append([i, ent.title, date, time])
                    except():
                        print("An exception occurred: Could be private, now deleted, or a group.")
                        pass

            print("Scrape complete for:", i, )
        df.to_json('./data/edgelists/' + alphanumeric + '_archive.json',
                   orient='split', compression='infer', index=True)


    with client:
        client.loop.run_until_complete(new_main())
    print('Forwards scraped successfully.')
else:
    pass

again = input('Do you want to scrape more chats? (y/n)')
if again == 'y':
    print('Restarting...')
    exec(open("forwards.py").read())
else:
    pass

launcher = input('Do you want to return to the launcher? (y/n)')
if launcher == 'y':
    print('Restarting...')
    exec(open("telepathy.py").read())
else:
    print('Thank you for using Telepathy.')
