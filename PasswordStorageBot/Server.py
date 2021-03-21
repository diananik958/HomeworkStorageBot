import logging
import AppExceptions
import db
from Storage import Storage 
from Authorization import Authorization
from aiogram import Bot, Dispatcher, executor, types
from aiogram import types
import Subject
import Date
from datetime import datetime

# token from BotFather
API_TOKEN = ''

# Initialize database
HOST = 'localhost'
USER = 'root'
PASSWORD = 'sasha'
DATABASE = 'testhw'
db.initdb(HOST, USER, PASSWORD, DATABASE) 

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot) 


# START---------------------------------------------------------------------------------------------

@dp.message_handler(commands=['start', 'START'])
async def send_welcome(message: types.Message):
    try: 
        Storage.AddTable(message.from_user.id)
        await message.answer("Hello!\nI am a homework storage bot.\nTo begin type /help")
    except AppExceptions.Table_Already_Exist as error:
        print(error)
        await message.answer("Looks like you already have a table.\nType /help to see the list of all commands and their description.")
    except Exception as e:
        print(e)
        print("Unexpected error!")
        
# HELP---------------------------------------------------------------------------------------------

@dp.message_handler(commands=['help', 'HELP'])
async def helpMSG(message: types.Message):
    text = ("/help - для просмотра всех команд и что они делают\n/add 'предмет' 'задание' - для добавления определенного предмета и задания к нему\n/show 'предмет' - для просмотра невыполненных заданий по предмету\n/showall 'предмет' - для просмотра всех заданий по предмету как выполненных, так и не выполненных\n/subjects - для просмотра списка предметов архива\n/done 'ID' - для смены статуса задания с невыполненного на выполненное (ID задания можно узнать при выполнение команды /show)\n/delete 'ID' - для удаления определенного задание для предмета (ID задания можно узнать при выполнение команды /show)\n/drop 'предмет' - для удаления предмета и всех заданий к нему\n/restore - для полного удаления вашего хранилище, для того чтобы снова начать пользоваться нашим хранилищем, наберите команду /start\n/deadline 'ID' 'YYYY-MM-DD' - для добавления дедлайна для задания по его id (пример даты: 2020-12-20)\n/period 'YYYY-MM-DD' 'YYYY-MM-DD' - для просмотра заданий за определенный период (пример даты: 2020-12-20)\n/lastweek - для просмотра заданий за прошлую неделю\n/lastmonth - для просмотра заданий за прошлый месяц\n/showdl 'YYYY-MM-DD' - для просмотра заданий которые нужно сделать до этого дедлайна")
    await message.answer(text)

# ADDS SUBJECT---------------------------------------------------------------------------------------------

@dp.message_handler(commands=['add', 'ADD'])
async def addData(message: types.Message):
    data = message.text[5:].split(' ')
    task = ""
    for word in data:
        if word != data[0]:
            task += word + " "
    if not data or not task:
        await message.answer("Incorrect input for /add command, use /help")
    else:
        subject = Subject.Subject(data[0], None, task, None)
        try:
            Storage.AddSub(message.from_user.id, subject)
            await message.answer("your task was inserted\n\n" + task + "\nfor subject: " + data[0])
        except AppExceptions.Not_Enough_Data as error:
            print(error)
            print("Incorrect input for /add command, use /help")
        except Exception as e:
            print(e)
            print("Error can not insert your data")

# SETS DEADLINE FOR TASK BY ID----------------------------------------------------------------------------------
@dp.message_handler(commands=['deadline', 'DEADLINE'])
async def addDeadline(message: types.Message):
    data = message.text[10:].split(' ')
    print(data)
    if len(data) != 2:
        await message.answer("Incorrect input for /deadline command, use /help")
    else:
        try:
            Storage.SetDeadline(message.from_user.id, data[0], data[1])
            await message.answer("Deadline: " + str(data[1]) + " was set to the task with id: " + str(data[0]))
        except AppExceptions.Cant_Set_Deadline as error:
            print(error)
            await message.answer("Cant set a deadline")
        except Exception as e:
            print(e)
            print("Error can not set deadline")

# SHOWS TASKS AND ITS IDS FOR SUBJECT---------------------------------------------------------------------------

@dp.message_handler(commands=['show', 'SHOW'])
async def showData(message: types.Message):
    subject_name = message.text[6:].split(' ')
    if len(subject_name) != 1:
        await message.answer("Incorrect input for /show command, use /help")
    else:
        try:
            data = Storage.ShowSub(message.from_user.id, subject_name)
            parsedData = 'Subject: ' + data[0].name + "\n\n"
            for text in data:
                parsedData += "(ID: " + str(text.ID) + ") task: " + str(text.task) + "\ncreated on: " + str(text.date_cr) + "\ndeadline is " + str(text.deadline) + "\n\n"
            await message.answer(parsedData)
        except Exception as e:
            print(e)
            print("Error can not get tasks for this subject")
  
# SHOWS ALL COMPLETED AND NOT COMPLETED TASKS AND ITS IDS FOR SUBJECT---------------------------------------------------------------------------

@dp.message_handler(commands=['showall', 'SHOWALL'])
async def showAllData(message: types.Message):
    subject_name = message.text[9:].split(' ')
    if len(subject_name) != 1:
        await message.answer("Incorrect input for /showall command, use /help")
    else:
        try:
            data = Storage.ShowAllTasks(message.from_user.id, subject_name)
            parsedData = 'Subject: ' + data[0].name + "\n\n"
            for text in data:
                parsedData += "(ID: " + str(text.ID) + ") task: " + str(text.task) + "\ncreated on: " + str(text.date_cr) + "\n"
                if (str(text.iscomp) == '0'):
                    parsedData += "is not completed\n" + "deadline is " + str(text.deadline) + "\n\n"
                elif (str(text.iscomp) == '1'):
                    parsedData += "was completed on: " + str(text.date_comp) + "\ndeadline was " + str(text.deadline) + "\n\n"
                else:
                    print("Couldn't get info if task is completed or not")
            await message.answer(parsedData)
        except Exception as e:
            print(e)
            print("Error can not get all tasks for this subject")

# SHOWS TASK ON LAST WEEK------------------------------------------------------------------------------------------
@dp.message_handler(commands=['lastweek', 'LASTWEEK'])
async def showLastWeek(message: types.Message):
    try:
        data = Storage.GetLastWeek(message.from_user.id)
        parsedData = ""
        for text in data:
            parsedData += "Subject: " + str(text.name) + "\n(ID: " + str(text.ID) + ") task: " + str(text.task) + "\nadded on date: " + str(text.date_cr) + "\n"
            if (str(text.iscomp) == '0'):
                parsedData += "is not completed\n\n"
            elif (str(text.iscomp) == '1'):
                parsedData += "was completed on " + str(text.date_comp) + "\n\n"
            else:
                print("Couldn't get info if task is completed or not")
        await message.answer(parsedData)
    except Exception as e:
        print(e)
        await message.answer("Error can get tasks for last week")

# SHOWS TASK ON LAST MONTHS----------------------------------------------------------------------------------------
@dp.message_handler(commands=['lastmonth', 'LASTMONTH'])
async def showLastMonth(message: types.Message):
    try:
        data = Storage.GetLastMonth(message.from_user.id)
        parsedData = ""
        for text in data:
            parsedData += "Subject: " + str(text.name) + "\n(ID: " + str(text.ID) + ") task: " + str(text.task) + "\nadded on date: " + str(text.date_cr) + "\n"
            if (str(text.iscomp) == '0'):
                parsedData += "is not completed\n\n"
            elif (str(text.iscomp) == '1'):
                parsedData += "was completed on " + str(text.date_comp) + "\n\n"
            else:
                print("Couldn't get info if task is completed or not")
        await message.answer(parsedData)
    except Exception as e:
        print(e)
        await message.answer("Error can get tasks for last month")

# SHOWS TASK FOR DEADLINE------------------------------------------------------------------------------------------
@dp.message_handler(commands=['showdl', 'SHOWDL'])
async def showForDeadline(message: types.Message):
    deadline = message.text[8:].split(' ')
    parsed = deadline[0].split('-')
    print(parsed)
    if len(deadline) != 1:
        await message.answer("Incorrect input for /showdl command, use /help") 
    elif len(parsed) != 3:
        await message.answer("You've entered more date than needed") 
    elif len(parsed[0]) != 4:
        await message.answer("Incorrect year format")
    elif len(paresed[1]) != 2 and int(parsed[1]) > 12:
        await message.answer("Incorrect month format")
    elif len(parsed[2]) != 2 and int(parsed[2]) > 31:
        await message.answer("Incorrect day format")
    else:
        try:
            id_date_valid = datetime.strptime(deadline[0], '%Y-%m-%d').date()
            data = Storage.GetForDeadline(message.from_user.id, deadline)
            parsedData = "Tasks to do before " + str(deadline[0]) + "\n\n"
            for text in data:
                parsedData += "Subject: " + str(text.name) + "\n(ID: " + str(text.ID) + ") task: " + str(text.task) + "\ncreated on: " + str(text.date_cr) + "\ndeadline is " + str(text.deadline) + "\n\n"
            await message.answer(parsedData)
        except Exception as e:
            print(e)
            await message.answer("Incorrect day format")

# SHOWS ALL SUBJECTS-----------------------------------------------------------------------------------------------

@dp.message_handler(commands=['subjects', 'sub', 'SUBJECTS'])  
async def showSub(message: types.Message):
    try:
        subject = Storage.ShowSubNames(message.from_user.id)
        parsedData = 'List of subjects:\n\n'
        for name in subject:
            parsedData += name[0] + "\n"
        await message.answer(parsedData)
    except Exception as e:
        print(e)
        print("Error can not get the list of subjects")

# SETS TASK COMPLETED--------------------------------------------------------------------------------------------
@dp.message_handler(commands=['done', 'DONE'])  
async def isComplete(message: types.Message):
    data = message.text[6:].split(' ')
    if len(data) != 1:
        await message.answer("Incorrect input for /done command, use /help")
    else:
        try:
            if (Storage.IsComplete(message.from_user.id, data)):
                Storage.TaskIsComplete(message.from_user.id, data)
                await message.answer("task with id: " + data[0] + " marked as completed")
            else: 
                await message.answer("Check if id you entered is correct")
        except Exception as e:
            print(e)
            await message.answer("Check if id you entered is correct")

# SHOWS TASK IN PERIOD-----------------------------------------------------------------------------

@dp.message_handler(commands=['period', 'PERIOD'])  
async def showInPeriod(message: types.Message):
    data = message.text[8:].split(' ') # /period 2020-10-02 2020-11-14
    if len(data) != 2:
        await message.answer("Incorrect input for /period command, use /help")
    else:
        try:
            response = Storage.GetByPeriod(message.from_user.id, data[0], data[1])
            parsedData = ""
            for text in response:
                parsedData += "Subject: " + str(text.name) + "\n(ID: " + str(text.ID) + ") task: " + str(text.task) + "\nadded on date: " + str(text.date_cr) + "\n"
                if (str(text.iscomp) == '0'):
                    parsedData += "is not completed\n\n"
                elif (str(text.iscomp) == '1'):
                    parsedData += "was completed on " + str(text.date_comp) + "\n\n"
                else:
                    print("Couldn't get info if task is completed or not")
            await message.answer(parsedData)
        except Exception as e:
            print(e)
            await message.answer("Error can get tasks for this period")
        


# DELETS TASK BY ID FOR SUBJECT--------------------------------------------------------------------

@dp.message_handler(commands=['delete', 'DELETE'])  
async def delTask(message: types.Message):
    data = message.text[8:].split(' ')
    if len(data) != 1:
        await message.answer("Incorrect input for /delete command, use /help")
    else:
        try:
            Storage.DeleteByID(message.from_user.id, data)
            await message.answer("Task with id: " + data[0] + " was deleted successfully!")
        except AppExceptions.Incorrect_Task_Id as error:
                print(error)
                await message.answer("You've entered incorrect task id")
        except Exception as e:
            print(e)
            print("Can't delete task with this id")

# DELETES SUBJECT AND ALL TASK AND DATES IN IT---------------------------------------------------------------------------------------------

@dp.message_handler(commands=['drop', 'DROP'])  
async def delSub(message: types.Message):
    subject_name = message.text[6:].split(' ')
    if len(subject_name) != 1:
        await message.answer("Incorrect input for /drop command, use /help")
    else:
        try:
            Storage.DeleteService(message.from_user.id, subject_name)
            await message.answer("All tasks from " + subject_name[0] + " were deleted successfully!")
        except Exception as e:
            print(e)
            print("Can't delete subject with this name")


# DELETES ALL DATA INCLUDING TABLE---------------------------------------------------------------------------------------------
@dp.message_handler(commands=['restore', 'RESTORE'])  
async def resetTable(message: types.Message):
    try:
        Storage.DeleteAll(message.from_user.id)
        await message.answer("Your storage was deleted!")
    except Exception as e:
        print(e)
        print("Can't delete your storage")

# FOR INCORRECT COMMANDS---------------------------------------------------------------------------------------------
@dp.message_handler()
async def unknown(message: types.Message):
    await message.answer("Hmmm...\nI don't understand what you want\nUse help to see the list of commands")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
