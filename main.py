from telethon.sync import TelegramClient, events



api_id = "2421227"
api_hash = "5cfbdb99e4477b828bf06a9cd1efeead"
bot_token = '7890508770:AAHYtfKBjOxIWQ08m6onH6MZRu6gxKbZMwc'

client = TelegramClient("wmt", api_id=api_id, api_hash=api_hash).start(bot_token=bot_token)


@client.on(events.NewMessage(pattern='/start'))
async def handler(event):
   await event.reply('Hey!')

client.run_until_disconnected()