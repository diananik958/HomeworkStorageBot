import mysql.connector 
from mysql.connector import errorcode
import AppExceptions
import db

class Storage(object):

    @staticmethod
    def IsComplete(id, task_id):
        try:
            response = db.checkIsComlete(id, task_id)
            if (response == 0):
                return True # if not completed
            else:
                return False # if is completed
        except Exception as e:
            print(e)
            raise AppExceptions.Cant_Check_If_Task_Is_Comlete("AppExceptions.Cant_Check_If_Task_Is_Comlete")

    @staticmethod
    def AddTable(id):
        try: 
            db.createUserTable(id)
        except Exception as e:
            print(e)
            raise AppExceptions.Table_Already_Exist("AppExceptions.UserAlreadyExist")

    # Adds subject to the table
    @staticmethod
    def AddSub(id, subject):
        try:
            addSubject = db.addSubject(id, subject)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Add_Subject("AppExceptions.Cant_Add_Subject")

    # Set deadline to the task by id
    @staticmethod
    def SetDeadline(id, task_id, deadline):
        try:
            print(task_id)
            print(deadline)
            setDeadline = db.setDeadline(id, task_id, deadline)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Set_Deadline("AppExceptions.Cant_Set_Deadline")

    # Prints uncompleted tasks and ids for this subject
    @staticmethod
    def ShowSub(id, subject_name):
        try:
            showSubject = db.getSubject(id, subject_name)
            return(showSubject)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Get_Subject("AppExceptions.Cant_Get_Subject")

    # Print list of all subjects
    @staticmethod
    def ShowSubNames(id):
        try:
            showNames = db.getSubjectList(id)
            return(showNames)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Get_Subject_Names("AppExceptions.Cant_Get_Subject_Names")

 # Prints all uncompleted and completed tasks and irs ids for this subject
    @staticmethod
    def ShowAllTasks(id, subject_name):
        try:
            showAllTasks = db.getAll(id, subject_name)
            return(showAllTasks)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Get_Subject("AppExceptions.Cant_Get_Subject")

    # Shows tasks by period
    @staticmethod
    def GetByPeriod(id, date1, date2):
        try:
            showByPeriod = db.getInPeriod(id, date1, date2)
            return(showByPeriod)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Get_Subject("AppExceptions.Cant_Get_Subject")

    # Shows tasks for last week
    @staticmethod
    def GetLastWeek(id):
        try:
            showLastWeek = db.getLastWeek(id)
            return(showLastWeek)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Get_Subject("AppExceptions.Cant_Get_Subject Last Week")

    # Shows tasks for last month
    @staticmethod
    def GetLastMonth(id):
        try:
            showLastMonth = db.getLastMonth(id)
            return(showLastMonth)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Get_Subject("AppExceptions.Cant_Get_Subject Last Month")

    # Shows tasks before deadline
    @staticmethod
    def GetForDeadline(id, deadline):
        try:
            showForDeadline = db.getUntillDeadline(id, deadline)
            return(showForDeadline)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Get_Subject("AppExceptions.Cant_Get_Subject Deadline")

    # Deletes tasks from the subject by date 
    @staticmethod
    def DeleteByID(id, task_ID):
        try:
            if (db.checkID(id, task_ID)):
                deleteByTaskID = db.deleteSubjectbyID(id, task_ID)
            else:
                raise AppExceptions.Incorrect_Task_Id("AppExceptions.Incorrect_Task_Id")
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Delete_Subject_by_ID("AppExceptions.Cant_Delete_Subject_by_Date")

    # Deletes subject and date and tasks in this
    @staticmethod
    def DeleteService(id, subject_name):
        try:
            deleteSubject = db.deleteSubject(id, subject_name)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Delete_Subject("AppExceptions.Cant_Delete_Subject")

    # Sets Task is complete
    @staticmethod
    def TaskIsComplete(id, task_id):
        try:
            setComplete = db.subjectComplete(id, task_id)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Set_Complete("AppExceptions.Cant_Set_Complete")

    # Deletes all data including the table
    @staticmethod
    def DeleteAll(id):
        try:
            deleteAll = db.deleteAll(id)
        except Exception as error:
            print(error)
            raise AppExceptions.Cant_Delete_All_Data("AppExceptions.CantDeleteAllData")