from telethon.sync import TelegramClient, events
from tools import get_starter_text
from database import User, Tasks
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
    title = result.pop(0).replace("/add ", "", 1)
    date = datetime.strptime(result.pop(-1), "%Y:%m:%d %H:%M")
    description = "\n".join(result)

    sender = await event.get_sender()
    task = Tasks.create(
        user=sender.id, title=title, datetime=date, description=description
    )

    response_text = f'The "{title}" task is created. its ID is {task}'

    await event.reply(response_text)


@client.on(events.NewMessage(pattern="/tasks"))
async def get_task(event):
    sender = await event.get_sender()
    tasks = Tasks.select().where(Tasks.user == sender.id, Tasks.is_done == False)

    response_text = "\n\n"
    for task in tasks:
        response_text += f"task id ({task.id}) => {task.title}\n\n"

    response_text += "For remove or update your task use /remove or /update with task id in front of them example: /remove 12"

    await event.reply(response_text)


@client.on(events.NewMessage(pattern="/remove"))
async def remove_task(event):
    sender = await event.get_sender()
    task_id = int(event.raw_text.split(" ")[1])

    task = Tasks.get(Tasks.user == sender.id, Tasks.id == task_id)
    task_title = task.title

    remove_q = Tasks.delete().where(Tasks.user == sender.id, Tasks.id == task_id)
    remove_q.execute()

    await event.reply(f"Task {task_title} removed.")


client.run_until_disconnected()
