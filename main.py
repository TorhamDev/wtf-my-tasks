from telethon.sync import TelegramClient, events
from tools import get_starter_text
from database import User
from datetime import datetime

api_id = "2421227"
api_hash = "5cfbdb99e4477b828bf06a9cd1efeead"
bot_token = "7890508770:AAHYtfKBjOxIWQ08m6onH6MZRu6gxKbZMwc"

client = TelegramClient("wmt", api_id=api_id, api_hash=api_hash).start(
    bot_token=bot_token
)


@client.on(events.NewMessage(pattern="/start"))
async def handler(event):
    sender = await event.get_sender()
    user_id = sender.id
    user_first_name = sender.first_name
    User.get_or_create(name=user_first_name, user_id=user_id)
    await event.reply(get_starter_text(user_first_name))


@client.on(events.NewMessage(pattern="/add"))
async def add_task(event):
    text = event.raw_text
    result = text.split("\n")
    title = result.pop(0).replace("/add", "")
    date = datetime.strptime(result.pop(-1), "%Y:%m:%d %H:%M")
    description = "\n".join(result)

    await event.reply(f"title: {title}\n date: {date}\n desc: {description}")


client.run_until_disconnected()

# next video 
# save task to dabase
# add get task command