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
    tasks = Tasks.select().where(Tasks.user == sender.id)

    response_text = "\n\n"
    for task in tasks:
        response_text += (
            f"TaskID=({task.id}) TaskStatus=({task.is_done}) => {task.title}\n\n"
        )

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


@client.on(events.NewMessage(pattern="/update"))
async def update_task(event):
    sender = await event.get_sender()
    raw_text = event.raw_text

    result = raw_text.split("\n")
    task_id = int(result.pop(0).split(" ")[1])

    title = result.pop(0)
    date = datetime.strptime(result.pop(-1), "%Y:%m:%d %H:%M")
    description = "\n".join(result)

    task = Tasks.get(Tasks.user == sender.id, Tasks.id == task_id)
    task.title = title
    task.description = description
    task.datetime = date
    # task.is_done #TODO: Change is done to True if update date was bigger than current date


    task.save()

    await event.reply(f"Task {task_id} Updated.")


@client.on(events.NewMessage(pattern="/done"))
async def is_done(event):
    sender = await event.get_sender()
    task_id = int(event.raw_text.split(" ")[1])

    task = Tasks.get(Tasks.user == sender.id, Tasks.id == task_id)
    task.is_done = not task.is_done
    task.save()

    await event.reply(f"Status of the Task {task.title} changed to {task.is_done}.")


client.run_until_disconnected()
