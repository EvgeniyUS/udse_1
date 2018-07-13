Установить модули: psycopg2


2.1.6 Справочники:
	2.1.6.1 Сведения о договорах (контрактах)	[класс Contract]
	2.1.6.2 Сведения о заказах			[класс Order]
	2.1.6.3 Справочник о контрагентах		[класс Parther]
Файлы - хранилище документов с тегами			[класс File]
Справки - сохранённые запросы				[класс Inquiry]
Шаблоны изделий						[класс Template]
2.1.1 Типы изделий серийной продукции в эксплуатации	[класс Product]
	2.1.1.1 Типы серийной продукции
	2.1.1.2 Типы ПКИ для серийной продукции
	2.1.1.3 Типы ПС(ПК)

2.1.2 Сведения об экземплярах серийной продукции	[класс Release]
	2.1.2.1 Сведения об экземплярах продукции
	2.1.2.2 Сведения об экземплярах ПКИ
	2.1.2.3 сведения об экземплярах ПС(ПК)
2.1.3 Сведения об инцидентах (обслуживание)		[класс Service]
2.1.4 Сведения об входном контроле			[класс Verify]
2.1.5 Сведения об объектах эксплуатации			[класс Location]
Состав - следующий уровень вложенности			[класс Consist]





#ДОБАВЛЕНИЕ ЭЛЕМЕНТА ЗАДАННОГО ТИПА С АВТОМАТИЧЕСКИМ ПОЛУЧЕНИЕМ ID, ЕСЛИ НЕ УКАЗАН КОНКРЕТНЫЙ.
addData(dataType, dataID, data, auth)
	АТРИБУТЫ:
	dataType - тип элемента [str]
	dataID	- ID элемента [int/str]
	data - данные элемента [dict/list]  {подготовленные json.dumps()}
	auth - информация для авторизации [???]
	ВОЗВРАЩАЕТ:
	при пустом('') dataID, если тип позволяет, - автоинкриментный ID добавленного элемента [int]
	ОШИБКИ:
	Exception.faultString - текст ошибки {для протокола XML-RPC} [str]

#ПОЛУЧЕНИЕ ЭЛЕМЕНТА ЗАДАННОГО ТИПА ПО ID, СПИСКУ ID ИЛИ ФИЛЬТРУ.
#ФИЛЬТР ПРЕДСТАВЛЯЕТ ИЗ СЕБЯ ОДНОУРОВНЕВЫЙ СЛОВАРЬ. ВОЗВРАЩАЮТСЯ ЭЛЕМЕНТЫ, ИМЕЮЩИЕ ТАКИЕ КЛЮЧИ СО ЗНАЧЕНИЯМИ.
getData(dataType, dataFilter, auth)
	АТРИБУТЫ:
	dataType - тип элемента [str]
	dataFilter - ID, список ID или словарь для поиска по данным о элементов [int/str/list/dict]
	auth - информация для авторизации [???]
	ВОЗВРАЩАЕТ {json.dumps()}:
	при dataFilter, [dict] - список списков [ID, data] найденых записей [list]
	при dataFilter, [dict/list пустой] - список списков [ID, data] всех записей [list]
	при dataFilter, [list/int/str] - список списков [ID, data] запрошенных записей [list]
	ОШИБКИ:
	Exception.faultString - текст ошибки {для протокола XML-RPC} [str]

#ЗАМЕНА ЭЛЕМЕНТА ЗАДАННОГО ТИПА С УКАЗАННЫМ ID.
setData(dataType, dataID, data, auth)
	АТРИБУТЫ:
	dataType - тип элемента [str]
	dataID	- ID элемента [int/str]
	data - данные элемента [dict/list]  {подготовленные json.dumps()}
	auth - информация для авторизации [???]
	ВОЗВРАЩАЕТ:
	кол-во изменений >0 (int)
	ОШИБКИ:
	Exception.faultString - текст ошибки {для протокола XML-RPC} [str]

#УДАЛЕНИЕ ЭЛЕМЕНТОВ ЗАДАННОГО ТИПА С УКАЗАННЫМИ ID.
delData(dataType, dataIDs, auth)
	АТРИБУТЫ:
	dataType - тип элемента [str]
	dataIDs - ID удаляемых элементов [int/str/list]
	auth - информация для авторизации [???]
	ВОЗВРАЩАЕТ:
	кол-во удалений >0 (int)
	ОШИБКИ:
	Exception.faultString - текст ошибки {для протокола XML-RPC} [str]


#ДОБАВЛЕНИЕ ФАЙЛА И ДОПОЛНИТЕЛЬНОЙ ИНФОРМАЦИИ О НЁМ.
addFile(dataType, dataID, fileInfo, fileData, auth)
	АТРИБУТЫ:
	dataType - тип объекта, с которым связан файл [str]
	dataID - ID объекта, с которым связан файл [int или str]
	fileInfo - дополнительная информация о файле [dict] {подготовленный json.dumps()}
		добавляемые сервером поля:
		- size - размер в байтах [int];
		- md5 - хэш-сумма MD5 [str];
		- added - время добавления вида 2017-10-25 12:03:46.168766+03:00 [str].
		рекомендуемые пользовательские поля:
		- name - имя файла с расширением [str];
		- modified - время изменения {os.stat(<ИМЯ ФАЙЛА>).st_mtime} [float];
		- secret - уровень секретности [int];
		- permissions - права доступа к файлу [???].
	fileData - содержимое файла в виде xmlrpclib.Binary(<ДАННЫЕ ФАЙЛА>) [instance]
	auth - информация для авторизации [???]
	ВОЗВРАЩАЕТ:
	автоинкриментный ID добавленного файла [int]
	ОШИБКИ:
	Exception.faultString - текст ошибки {для протокола XML-RPC} [str]
	
#ИНФОРМАЦИЯ О ФАЙЛАХ ПО ID, СПИСКУ ID ИЛИ ФИЛЬТРУ.
#ФИЛЬТР ПРЕДСТАВЛЯЕТ ИЗ СЕБЯ ОДНОУРОВНЕВЫЙ СЛОВАРЬ. ВОЗВРАЩАЮТСЯ ЭЛЕМЕНТЫ, ИМЕЮЩИЕ ТАКИЕ КЛЮЧИ СО ЗНАЧЕНИЯМИ.
infFile(fileFilter, auth)
	АТРИБУТЫ:
	fileFilter - ID, список ID или словарь для поиска по информации о файлах
	auth - информация для авторизации [???]
	ВОЗВРАЩАЕТ:
	при fileFilter [dict] - список списков [ID, fileInfo] найденых файлов [list]
	при fileFilter [dict/list пустой] - список списков [ID, fileInfo] всех файлов [list]
	при fileFilter [list, int, str] - список списков [ID, fileInfo] запрошенных файлов [dict]
		fileInfo [dict]:
		  dataType - тип объекта, с которым связан файл [str];
		  dataID - ID объекта, с которым связан файл [int или str];
		  size - размер в байтах [int];
		  md5 - хэш-сумма MD5 [str];
		  added - время добавления вида 2017-10-25 12:03:46.168766+03:00 [str];
		  другие пользовательские поля.
	ОШИБКИ:
	Exception.faultString - текст ошибки {для протокола XML-RPC} [str]

#ЗАПРС ФАЙЛА.
getFile(fileID, auth)
	АТРИБУТЫ:
	fileID - ID, запрашиваемого файла [int/str]
	auth - информация для авторизации [???]
	ВОЗВРАЩАЕТ:
	содержимое файла в виде xmlrpclib.Binary()
	ОШИБКИ:
	Exception.faultString - текст ошибки {для протокола XML-RPC} [str]

#УДАЛЕНИЕ ФАЙЛОВ.
delFile(fileIDs, auth)
	АТРИБУТЫ:
	fileIDs - ID, удаляемых файлов [int/str/list]
	auth - информация для авторизации [???]
	ВОЗВРАЩАЕТ:
	количество удалённых элементов >0 [int]
	ОШИБКИ:
	Exception.faultString - текст ошибки {для протокола XML-RPC} [str]

setPrivacy(dataType, dataID, privacyLevel, auth)

getPrivacy(dataType, dataID, auth)

addUser(login, auth)
-> id

getUser(userID/{userLogin}, auth)

setUser(userID, auth)

delUser(userIDs, auth)

addGroup(groupID, userIDs/groupIDs, auth)

getGroup(groupID, auth)

setGroup(groupID, userIDs/groupIDs, auth)

delGroup(groupIDs, auth)

grantAccess(dataType, dataID, read/write, groupIDs/userIDs, auth)

infAccess(dataType, dataID, read/write, groupIDs/userIDs, auth)

denieAccess(dataType, dataID, read/write, groupIDs/userIDs, auth)

