import base64
import hashlib
# 43 character
SECRET_KEY = 'uT84_gKcXyWqz5tMlp34jM2aT0zrOnh6rQz3oVrI4YI'

def encode_id(id):
    id_str = str(id)
    data = f'{id_str}{SECRET_KEY}'
    encoded = base64.urlsafe_b64encode(data.encode()).decode()
    return encoded

def decode_id(encoded_id):
    try:
        decoded_bytes = base64.urlsafe_b64decode(encoded_id.encode())
        decoded_str = decoded_bytes.decode()
        id_str = decoded_str.replace(SECRET_KEY, '')
        return int(id_str)
    except Exception as e:
        print(f"Decoding error: {e}")
        raise ValueError("Invalid encoded ID")

def getlastid(table_name):
	result = table_name.objects.last()
	if result:
		lastid = result.id
		newid = lastid + 1
	else:
		lastid = 0
		newid = 1
	return lastid, newid
	
def getnewid(table_name):
	result = table_name.objects.last()
	if result:
		newid = result.id + 1
		hashid = hashlib.md5(str(newid).encode())
	else:
		newid = 1
		hashid = hashlib.md5(str(newid).encode())
	return newid, hashid.hexdigest()

def getjustnewid(table_name):
	result = table_name.objects.last()
	if result:
		newid = result.id + 1
	else:
		newid = 1
	return newid

def split_string(string):
	string2 = string.split()
	return string2[0].lower()

def getMonthName(num):
	if num == 1:
		month = "Janeiru"
	if num == 2:
		month  = "Fevereiru"
	if num == 3:
		month  = "Marsu"
	if num == 4:
		month  = "Abril"
	if num == 5:
		month  = "Maio"
	if num == 6:
		month  = "Junho"
	if num == 7:
		month  = "Julho"
	if num == 8:
		month  = "Agosto"
	if num == 9:
		month  = "Setembru"
	if num == 10:
		month  = "Outubro"
	if num == 11:
		month  = "Novembro"
	if num == 12:
		month  = "Dezembro"
	return month

def getStatusId(status):
	if status == "new":
		estatus = 1
	if status == "clarification":
		estatus = 2
	if status == "budgeting":
		estatus = 3
	if status == "budgeted":
		estatus = 4
	if status == "approval":
		estatus = 5
	if status == "revision":
		estatus = 6
	if status == "approved":
		estatus = 7
	if status == "planning":
		estatus = 8
	if status == "implementation":
		estatus = 9
	if status == "acceptance tests":
		estatus = 10
	if status == "available for production":
		estatus = 11
	if status == "production installation":
		estatus = 12
	if status == "closed":
		estatus = 13
	if status == "abandoned":
		estatus = 14
	if status == "canceled":
		estatus = 15
	if status == "rejected":
		estatus = 16
	if status == "suspended":
		estatus = 17
	if status == "analysis":
		estatus = 18
	return estatus

def getStatusName(status):
	if status == 1:
		estatus = "new"
	if status == 2:
		estatus = "clarification"
	if status == 3:
		estatus = "budgeting"
	if status == 4:
		estatus = "budgeted"
	if status == 5:
		estatus = "approval"
	if status == 6:
		estatus = "revision"
	if status == 7:
		estatus = "approved"
	if status == 8:
		estatus = "planning"
	if status == 9:
		estatus = "implementation"
	if status == 10:
		estatus = "acceptance tests"
	if status == 11:
		estatus = "available for production"
	if status == 12:
		estatus = "production installation"
	if status == 13:
		estatus = "closed"
	if status == 14:
		estatus = "abandoned"
	if status == 15:
		estatus = "canceled"
	if status == 16:
		estatus = "rejected"
	if status == 17:
		estatus  = "suspended"
	if status == 18:
		estatus = "analysis"
	return estatus