# from telethon.sync import TelegramClient
# from telethon import TelegramClient

print('Welcome to Telepathy')
print('Please select a function:')

li = ['Batch chat archiver', 'Scrape group members', 'Scrape forwarded messages in a chat']


def display(line):
    for idx, tables in enumerate(line):
        print("%s. %s" % (idx+1, tables))


def get_list(line):
    choose = int(input("\nPick a number:"))-1
    if choose < 0 or choose > (len(line) - 1):
        print('Invalid Choice')
        return ''
    return line[choose]


display(li)
choice = (get_list(li))

print('Loading', choice, '...')

if choice == 'Batch chat archiver':
    print('Launching batch chat archiver')
    exec(open("archiver.py").read())
elif choice == 'Scrape group members':
    print('Launching group member scraper...')
    exec(open("members.py").read())
elif choice == 'Scrape forwarded messages in a chat':
    print('Launching channel forward scraper...')
    exec(open("forwards.py").read())
