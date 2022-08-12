import ampalibe
from ampalibe import Payload
from tononkira import Tononkira 
from ampalibe import Model, Messenger
from conf import Configuration as config
from ampalibe.ui import QuickReply, Element, Button

query = Model()
chat = Messenger()
tononkira = Tononkira()

def divide(text):
    if len(text) >= 2000:
        for i in range(1999, 0, -1):
            if text[i] == '\n':
                return [text[:i], text[i:]]
    return [text]


@ampalibe.command('/')
def main(sender_id, cmd, **extends):
    chat.send_message(sender_id, "Tongasoa")

    quick_rep = [
        QuickReply(title='🎵 Lohateny', payload=Payload('/search', by='lohateny')),
        QuickReply(title='👨 Mpihira', payload=Payload('/search', by='mpihira')),
        QuickReply(title='🎼 Tononkira', payload=Payload('/search', by='tononkira'))
    ]
    chat.send_quick_reply(sender_id, quick_rep, "Te hikaroka amnin'ny ...")


@ampalibe.command('/search')
def search(sender_id, by, **extends):
    query.set_action(sender_id, '/get')
    query.set_temp(sender_id, 'type', by)
    chat.send_message(sender_id, "Soraty ny teny misy anatin'ny " + by)


@ampalibe.action('/get')
def get(sender_id, cmd, **extends):
    query.set_action(sender_id, None)
    by = query.get_temp(sender_id, 'type')

    if by == 'lohateny':
        res = tononkira.search_by(title=cmd)
    elif by == 'mpihira':
        res = tononkira.search_by(artist=cmd)
    else:
        res = tononkira.search_by(lyrics=cmd)
    
    if not res:
        return chat.send_message(sender_id, "Tsisy vokany ny fikarohana")
    
    elements = [
        Element(
            title=r['title'],
            subtitle=r['artist'],
            image_url=config.APP_URL+'/asset/musical-note.png',
            buttons=[
                 Button(
                    type="postback",
                    title="Jerena",
                    payload=Payload("/fetch", url=r['url']),
                )
            ]
        ) for r in res
    ]
    chat.send_template(sender_id, elements, next='Manaraka')


@ampalibe.command('/fetch')
def fetch(sender_id, url, **ext):
    print(url)
    res = tononkira.fetch(url)
    for text in divide(res):
        chat.send_message(sender_id, text)
