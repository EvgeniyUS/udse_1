# -*- coding: utf-8 -*-

import json
from ldap import LDAP
from settings import dbName, dbUser, dbHost, dbPort, dbPassword
from psycopg2 import connect as connectPSQL, Binary as binaryPSQL

def dbConnect(dbName=dbName, dbUser=dbUser, dbHost=dbHost, dbPort=dbPort, dbPassword=dbPassword):
    try:
        result = connectPSQL('dbname={} user={} host={} port={} password={}'.format(
            dbName,
            dbUser,
            dbHost,
            dbPort,
            dbPassword))
    except Exception as error:
        print str(error).decode('utf8')
        raise Exception('База данных недоступна!')
    return result

def dbBinary(fileData):
    fileData = binaryPSQL(fileData.data)
    return fileData

def loadVar(var):
    try:
        if isinstance(var, unicode) or isinstance(var, str):
            var = json.loads(var)
    except Exception:
        pass
    finally:
        if not isinstance(var, list) and not isinstance(var, dict):
            var = [var]
    if isinstance(var, dict):
        result = {}
        for key in var:
            if (isinstance(var[key], unicode) or isinstance(var[key], str)) and var[key].isdigit():
                result[key] = int(var[key])
            elif isinstance(var[key], unicode):
                result[key] = var[key].encode('utf8')
            else:
                result[key] = var[key]
    else:
        result = []
        for entry in var:
            if (isinstance(entry, unicode) or isinstance(entry, str)) and entry.isdigit():
                result.append(int(entry))
            elif isinstance(entry, unicode):
                result.append(entry.encode('utf8'))
            else:
                result.append(entry)
        if len(result) == 1:
            result = result[0]
    return result

# Проверяем, что пользователь есть в системе 
def chkUser(auth):
    query = "SELECT id,data->>'privacy' FROM \"user\" WHERE "
    if (len(auth) == 2) and auth[1]:
        query += "(data ->> 'login')='{}' AND (data ->> 'domain')=''".decode('utf8').format(auth[0])
    elif (len(auth) == 3) and auth[2]:
        query += "(data ->> 'login')='{}' AND (data ->> 'domain')='{}'".decode('utf8').format(auth[0], auth[2])
    else:
        raise Exception('Неправильный запрос авторизации: {}!'.format(auth))
    connection = None
    try:
        connection = dbConnect()
        cursor = connection.cursor()
        cursor.execute(query)
        fetch = cursor.fetchone()
        if not fetch:
            raise Exception('Пользователь не найден!')
        else:
            result = fetch[0], int(fetch[1]), []
        query = "SELECT id FROM \"group\" WHERE (data -> 'members') @> '{}'".decode('utf8').format(result[0])
        cursor.execute(query)
        fetch = cursor.fetchall()
        for entry in fetch:
            result[2].append(entry[0])
    except Exception as error:
        if query:
            print query.decode('utf8')
        raise
    finally:
        if connection:
            connection.close()
    return result

# Аутентифицируем пользователя 
def chkAuth(auth):
    result = chkUser(auth)
    if len(auth) == 3:
        ad = LDAP(auth[0], auth[1], auth[2])
        try:
            ad.connect().unbind()
            #result = True
        except Exception as error:
            result = None
            print str(error).decode('cp1251')
    else:
        query = "SELECT data->>'pwdHash' FROM \"user\" WHERE data ->> 'login'='{}' AND data ->> 'domain'=''".decode('utf8').format(auth[0])
        connection = None
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            cursor.execute(query)
            fetch = cursor.fetchone()
            if not fetch or (fetch[0] != auth[1]):
                result = None
        except Exception as error:
            if query:
                print query.decode('utf8')
            raise
        finally:
            if connection:
                connection.close()
    if not result:
        raise Exception('Ошибка аутентификации!')
    return result

# Проверяем права и уровень доступа пользователя
def getAccess(auth, dataType=None, dataID = None, write = False):

    # todo Безопасность файлов привязать к объектам

    try:
        userID, userPrivacy, userGroups = chkAuth(auth)
        if not dataType:
            result = True
        else:
            query = "SELECT id,security FROM \"group\" WHERE id='{}'".format(dataType)
            connection = dbConnect()
            cursor = connection.cursor()
            try:
                cursor.execute(query)
                fetch = cursor.fetchone()
            except Exception as error:
                fetch = None
                print str(error).decode('utf8')
            if not fetch:
                raise Exception('Группа "{}" не существует!'.format(dataType))
            if not fetch[1]:
                raise Exception('Информация о безопасности у группы "{}" отсутствует!'.format(dataType))
            if isinstance(fetch[1], str):
                security=json.loads(fetch[1])
            else:
                security = fetch[1]
            if dataID:
                query = "SELECT id,security FROM \"{}\" WHERE id='{}'".format(dataType, dataID)
                try:
                    cursor.execute(query)
                    fetch = cursor.fetchone()
                except Exception as error:
                    fetch = None
                    print str(error).decode('utf8')
                if not fetch:
                    raise Exception('Элемента "{}" типа "{}" не существует!'.format(dataID, dataType))
                if not fetch[1]:
                    raise Exception('Информация о безопасности у элемента "{}" типа "{}" отсутствует!'.format(dataID, dataType))
                if isinstance(fetch[1], str):
                    fetch=json.loads(fetch[1])
                else:
                    fetch = fetch[1]
                security['write'].extend(fetch['write'])
                security['read'].extend(fetch['read'])
                security['privacy'] = fetch['privacy']
            userGroups.append(userID)
            if (userPrivacy < security['privacy']):
                if dataID:
                    raise Exception('Недостаточный уровень доступа к "{}[{}]"!'.format(dataType, dataID))
                else:
                    raise Exception('Недостаточный уровень доступа к "{}"!'.format(dataType))
            elif write and (set(userGroups) & set(security['write'])):
                result = userID
            elif not write and (set(userGroups) & set(security['read'])):
                result = userID
            else:
                if dataID and write:
                    raise Exception('Отсутствует право на запись в "{}[{}]"!'.format(dataType, dataID))
                elif dataID:
                    raise Exception('Отсутствует право на чтение из "{}[{}]"!'.format(dataType, dataID))
                elif write:
                    raise Exception('Отсутствует право на запись в "{}"!'.format(dataType))
                else:
                    raise Exception('Отсутствует право на чтение из "{}"!'.format(dataType))
    except Exception as error:
        if auth:
            print str(auth).decode('utf8')
        print str(error).decode('utf8')
        raise
    return result

###def addLog(auth, dataType, dataID, write, result)