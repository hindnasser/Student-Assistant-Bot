import telebot
import dotenv, os
import requests

dotenv.load_dotenv()

bot_token = os.getenv("TOKEN")
bot = telebot.TeleBot(bot_token)

tasks = []

@bot.message_handler(commands=['start','about'])
def welcome_message (message):
    bot.send_message(message.chat.id,
        "Hi there! I’m your Student Assistant Bot.\n"
        "Here’s what I can do:\n\n"
        "- /addtask <task> - To add Task to your To Do list\n"
        "- /viewtasks - To display your To Do list\n"
        "- /marktask <task number> - To mark a task as complete in your To Do list\n"
        "- /removetask <task number> - To remove a task from your To Do list\n"
        "- /cleartasks - To clear all the tasks from your To Do list\n"
        "- /gpa <current GPA> <current credits> <course credits> <course mark> - Calculate your GPA\n"
        "- /quote - Get a motivational quote\n\n"
        "Let’s get started!")

@bot.message_handler(commands= ['addtask'])
def add_task(message):
    #task = message.text.replace('/addtask', '').strip()
    task = message.text.strip().split(" ",1)
    if len(task) < 2  :
        bot.reply_to(message,"Please write a task after the command. Example:\n`/addtask Study for exam`")
        return
    task = task[1]
    tasks.append(task)
    bot.send_message(message.chat.id, f"Task [{task}] is added to your To-Do list")

@bot.message_handler(commands= ['viewtasks'])
def view_tasks(message):
    if not tasks:
        bot.send_message(message.chat.id,"Wohoo!! Your To-do list is empty!" )
        return
    tasks_formatted = ""
    for i in range(len(tasks)):
        tasks_formatted += f"{i+1}. {tasks[i]}\n"
    bot.send_message(message.chat.id, f"Your Tasks are:\n{tasks_formatted}")

@bot.message_handler(commands=['marktask'])
def mark_task(message):
    if not tasks:
        bot.reply_to(message, "You have no tasks to mark as complete.")
        return
    message_content = message.text.split(" ",1)
    if  len(message_content) < 2:
        bot.reply_to(message, f"Please write a task number between 1 and {len(tasks)} after the command. Example:\n`/marktask 1`")
        return
    task_number = message_content[1]
    if not task_number.isnumeric():
        bot.reply_to(message, f"Please write a task number between 1 and {len(tasks)} after the command. Example:\n`/marktask 1`")
        return
    task_number = int(task_number)
    if task_number>len(tasks) or task_number < 1:
        bot.reply_to(message, f"Please write a task number between 1 and {len(tasks)} after the command. Example:\n`/marktask 1`")
        return
    temp = tasks[task_number-1]
    tasks[task_number-1] += " ✅."
    bot.send_message(message.chat.id, f"Task [{temp}] is marked as Done✅")
  
@bot.message_handler(commands=['removetask'])
def remove_task(message):
    if len(tasks) == 0:
        bot.reply_to(message, "You have no tasks to remove.")
        return
    message_content = message.text.split(" ",1)
    if  len(message_content) < 2:
        bot.reply_to(message, f"Please write a task number between 1 and {len(tasks)} after the command. Example:\n`/removetask 1`")
        return
    task_number = message_content[1]
    if not task_number.isnumeric():
        bot.reply_to(message, f"Please write a task number between 1 and {len(tasks)} after the command. Example:\n`/removetask 1`")
        return
    task_number = int(task_number)
    if task_number>len(tasks) or task_number < 1:
        bot.reply_to(message, f"Please write a task number between 1 and {len(tasks)} after the command. Example:\n`/removetask 1`")
        return
    temp = tasks[task_number-1]
    tasks.remove(temp)
    bot.send_message(message.chat.id, f"Task [{temp}] is removed from your To-Do list")  

@bot.message_handler(commands=['cleartasks'])
def clear_tasks(message):
    tasks.clear()
    bot.send_message(message.chat.id, f"Your To-Do list is cleared")

@bot.message_handler(commands=['gpa'])
def gpa (message):
    message_content = message.text.split(" ")
    if len(message_content) < 5:
        bot.reply_to(message, f"Please write the current GPA, current credits, course credits, course mark after the command. Example:\n`/gpa 87 30 3 89`")
        return
    gpa = float(message_content[1])
    credits = float(message_content[2])
    course_cred = float(message_content[3])
    course_mark = float(message_content[4])
    result = ((gpa*credits) + (course_cred*course_mark))/ (course_cred + credits)
    bot.send_message(message.chat.id,f"Your GPA is {round(result,2)}")

@bot.message_handler(commands=['quote'])
def get_qoute(message):
    response = requests.get("https://zenquotes.io/api/random")
    data = response.json()
    qoute = data[0]['q']
    bot.send_message(message.chat.id,f"Your Qoute of the Day:\n\"{qoute}\"")

bot.polling()