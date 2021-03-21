import mysql.connector 
from mysql.connector import errorcode
import hashlib
from hashlib import sha256
import Subject
import Date
import AppExceptions
import datetime
from datetime import datetime, date, time

DB = mysql.connector.connect(host = 'localhost',
                                     user = 'root',
                                     password = 'sasha',
                                     database = 'testhw')

def initdb(host, user, password, database):
    DB = mysql.connector.connect(host = host,
                                     user = user,
                                     password = password,
                                     database = database)

def checkIsNoTable(id):
        cursor = DB.cursor()
        check = "describe user" + str(id)
        cursor.execute(check)
        tables = cursor.fetchall()
        if (tables == None):
            return True
        else:
            return False
        

def createUserTable(id):
        cursor = DB.cursor()
        createTable = "create table user" + str(id) + " (subject varchar(50), ID int(50) auto_increment, task varchar(1000), date_created date, is_complete tinyint(1), date_completed date, deadline date, PRIMARY KEY(ID))"
        cursor.execute(createTable)
        DB.commit()
        cursor.close()


def addSubject(id, subject):
        cursor = DB.cursor()
        datecreated = datetime.strftime(datetime.now(), "%Y.%m.%d")
        insert = "insert into user" + str(id) + " (subject, task, date_created, is_complete) values (%s, %s, %s, %s)"
        val = (subject.name, subject.task, datecreated, 0)
        cursor.execute(insert, val)
        DB.commit()
        cursor.close()

def checkID(id, task_id):
        cursor = DB.cursor()
        allIDs = "select ID from user" + str(id)
        cursor.execute(allIDs)
        listID = cursor.fetchall()
        ids = list(sum(listID, ()))
        exist = False
        for numb in ids:
            print(str(numb) + " = " + str(task_id[0]))
            if int(task_id[0]) == int(numb):
                print("task id is correct")
                exist = True
        return exist

#def getID(id, subject_name):
        #cursor = DB.cursor()
        #query = "select ID from user" + str(id) + " where subject = '" + str(subject_name[0]) + "'"
        #cursor.execute(query)
        #task_ID = cursor.fetchone()
        #cursor.close()
        #return task_ID[0]

def getSubject(id, subject_name):
        cursor = DB.cursor()
        forSubject = "select * from user" + str(id) + " where subject = '" + str(subject_name[0]) + "' and is_complete = '0'"
        cursor.execute(forSubject)
        all = cursor.fetchall()
        response = []
        
        for subject in all:
            response.append(Date.Date(subject[0], subject[1], subject[2], subject[3], subject[4], None, subject[6])) 
        cursor.close()
        return response

def getAll(id, subject_name):
        cursor = DB.cursor()
        forSubject = "select * from user" + str(id) + " where subject = '" + str(subject_name[0]) + "'"
        cursor.execute(forSubject)
        all = cursor.fetchall()
        response = []
        
        for subject in all:
            response.append(Date.Date(subject[0], subject[1], subject[2], subject[3], subject[4], subject[5], subject[6]))
        cursor.close()
        return response

def getLastWeek(id):
        cursor = DB.cursor()
        lastweek = "select * from user" + str(id) + " where date_created between CURDATE()-INTERVAL 1 WEEK and CURDATE()"
        cursor.execute(lastweek)
        all = cursor.fetchall()
        response = []
        for data in all:
            response.append(Date.Date(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        cursor.close()
        print(response)
        return response

def getLastMonth(id):
        cursor = DB.cursor()
        lastmonth = "select * from user" + str(id) + " where date_created between CURDATE()-INTERVAL 30 DAY and CURDATE()"
        cursor.execute(lastmonth)
        all = cursor.fetchall()
        response = []
        for data in all:
            response.append(Date.Date(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        cursor.close()
        print(response)
        return response

def getUntillDeadline(id, deadline):
        cursor = DB.cursor()
        print(deadline[0])
        tasks = "select * from user" + str(id) + " where deadline <= '" + str(deadline[0]) + "' AND is_complete = '0'"
        cursor.execute(tasks)
        all = cursor.fetchall()
        response = []
        for data in all:
            response.append(Date.Date(data[0], data[1], data[2], data[3], None, None, data[6]))
        cursor.close()
        print(response)
        return response

def getSubjectList(id):
        cursor = DB.cursor()
        show = "select subject from user" + str(id)
        cursor.execute(show)
        response = set(cursor.fetchall())
        cursor.close()
        return response

def checkIsComlete(id, task_id):
        cursor = DB.cursor()
        query = "select is_complete from user" + str(id) + " where ID = '" + task_id[0] + "'"
        cursor.execute(query)
        task_is_comlete = cursor.fetchone()
        cursor.close()
        return task_is_comlete[0]

def getInPeriod(id, date1, date2):
        cursor = DB.cursor()
        period = "select * from user" + str(id) + "  where date_created >= '" + str(date1) + "' AND date_created <= '" + str(date2) + "'"
        cursor.execute(period)
        all = set(cursor.fetchall())
        response = []
        for data in all:
            response.append(Date.Date(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        cursor.close()
        return response

def setDeadline(id, task_id, date):
        cursor = DB.cursor()
        print(date)
        print(task_id)
        set = "update user" + str(id) + " set deadline = '" + str(date) + "' where ID = '" + str(task_id[0]) + "'"
        cursor.execute(set)
        DB.commit()
        cursor.close()

def subjectComplete(id, task_id):
        cursor = DB.cursor()
        datefinished = datetime.strftime(datetime.now(), "%Y.%m.%d")
        complete = "update user" + str(id) + " set is_complete = '1', date_completed = '" + datefinished + "' where ID = '" + task_id[0] + "'"
        cursor.execute(complete)
        DB.commit()
        cursor.close()

def deleteSubjectbyID(id, task_id):
        cursor = DB.cursor()
        delete = "delete from user" + str(id) + " where ID = '" + task_id[0] + "'"
        cursor.execute(delete)
        DB.commit()
        cursor.close()

def deleteSubject(id, subject_name):
        cursor = DB.cursor()
        drop = "delete from user" + str(id) + " where subject = '" + str(subject_name[0]) + "'"
        cursor.execute(drop)
        DB.commit()
        cursor.close()

def deleteAll(id):
        cursor = DB.cursor()
        dropTable = "drop table user" + str(id)
        cursor.execute(dropTable)
        cursor.close()


