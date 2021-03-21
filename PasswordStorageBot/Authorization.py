import mysql.connector 
from mysql.connector import errorcode
import os
import AppExceptions
import db
import random

class Authorization(object):
    """sign up, sign in, sign out
    """
#---------------------SIGN UP----------------------
    @staticmethod
    def UserIsAuth(id):
        try:
            response = db.checkSession(id)
        except Exception as e:
            print(e)
            raise AppExceptions.Cant_Check_If_Task_Is_Comlete("AppExceptions.CantCheckIfSessionIsOpen")
        if (response == 1):
            return True
        else:
            return False


    @staticmethod
    def signup(id):

        token = random.randint(0, 9999)
        try: 
            db.createUserTable(id)
            db.registerUser(id, token)
        except Exception as e:
            print(token)
            print(e)
            raise AppExceptions.UserAlreadyExist("AppExceptions.UserAlreadyExist")
        

#--------------------SIGN IN-----------------------

    @staticmethod
    def signin(id, user_token):
         new_token = random.randint(0, 9999)
         try:
             old_token = db.getToken(id)
         except Exception as e:
             print(e)
             raise AppExceptions.CantGetToken("AppExceptions.CantGetToken")
         if (user_token == old_token):
            try:
                db.setToken(id, new_token)
            except Exception as e:
                print(e)
                raise AppExceptions.CantInsertNewToken("AppExceptions.CantInsertNewToken")

            try:
                db.openSession(id)
            except Exception as e:
                print(e)
                raise AppExceptions.CantOpenSession("AppExceptions.CantOpenSession")
            return True
         else:
            return False


#--------------------SIGN OUT-----------------------
    @staticmethod
    def signout(id):
        try:
             response = db.checkSession(id)
        except Exception as e:
            print(e)
            raise AppExceptions.Cant_Check_If_Task_Is_Comlete("AppExceptions.CantCheckIfSessionIsOpen")
        print(response)
        if (response == 1):
            try:
                db.closeSession(id)
            except Exception as e:
                print(e)
                raise AppExceptions.CantCloseSession("AppExceptions.CantCloseSession")
            try:
                token = db.getToken(id)
            except Exception as e:
                print(e)
                raise AppExceptions.CanGetToken("AppExceptions.CanGetToken")
            return token
        else:
            raise AppExceptions.NotAuthorized("AppExceptions.NotAuthorized")