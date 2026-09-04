from django import template
import base64
from django.conf import settings

SECRET_KEY = 'uT84_gKcXyWqz5tMlp34jM2aT0zrOnh6rQz3oVrI4YI'

register = template.Library()

@register.filter(name='url_file')
def url(url):
	if url == 'url':
		file_url = settings.URL_FILE
	return file_url


@register.filter(name='encrypt')
def encode_id(id):
    id_str = str(id)
    data = f'{id_str}{SECRET_KEY}'
    encoded = base64.urlsafe_b64encode(data.encode()).decode()
    return encoded


@register.filter(name='decrypt')
def decode_id(encoded_id):
    try:
        decoded_bytes = base64.urlsafe_b64decode(encoded_id.encode())
        decoded_str = decoded_bytes.decode()
        id_str = decoded_str.replace(SECRET_KEY, '')
        return int(id_str)
    except Exception as e:
        print(f"Decoding error: {e}")
        raise ValueError("Invalid encoded ID")


@register.filter(name='getMonthNumber')
def getMonthNumber(month):
	if month == "January":
		month = "1"
	elif month == "February":
		month = "2"
	elif month == "March":
		month = "3"
	elif month == "April":
		month = "4"
	elif month == "May":
		month = "5"
	elif month == "June":
		month = "6"
	elif month == "July":
		month = "7"
	elif month == "August":
		month = "8"
	elif month == "September":
		month = "9"
	elif month == "October":
		month = "10"
	elif month == "November":
		month = "11"
	elif month == "December":
		month = "12"
	return month


@register.filter(name='getStatusName')
def getStatusName(status):
	if status == 1:
		name = "new"
	if status == 2:
		name = "clarification"
	if status == 3:
		name = "budgeting"
	if status == 4:
		name = "budgeted"
	if status == 5:
		name = "approval"
	if status == 6:
		name = "revision"
	if status == 7:
		name = "approved"
	if status == 8:
		name = "planning"
	if status == 9:
		name = "implementation"
	if status == 10:
		name = "acceptance tests"
	if status == 11:
		name = "available for production"
	if status == 12:
		name = "production installation"
	if status == 13:
		name = "closed"
	if status == 14:
		name = "abandoned"
	if status == 15:
		name = "canceled"
	if status == 16:
		name = "rejected"
	if status == 17:
		name = "suspended"
	if status == 18:
		name = "analysis"
	return name

