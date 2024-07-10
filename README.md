# DialPad POC


## Prerequisites

Ensure you have Python and `virtualenv` installed on your Ubuntu system.

### create virtual env 
python -m venv <env_name>

### activate virtual env
source venv/bin/activate

### Move to Project root directory and start python development server
python manage.py runserver

### base-url - localhost:8000

### signup
![image](https://github.com/bhakarerushi/dialpad-django_poc/assets/65430906/694d2b15-1751-439a-bb2f-e68239df6e2c)

### login
![image](https://github.com/bhakarerushi/dialpad-django_poc/assets/65430906/7158db81-a10e-43f9-8722-6197371d7ea5)

### Use this for following requests

headers - {
            "Authorization : Bearer <access_token>
          }

### list users 
![image](https://github.com/bhakarerushi/dialpad-django_poc/assets/65430906/3aa4dc7c-1227-4af5-be5b-3fa4d35d5202)

### Retrieve user
![image](https://github.com/bhakarerushi/dialpad-django_poc/assets/65430906/38a968c8-8bed-40ea-986f-9e810753d9c0)

### update user
![image](https://github.com/bhakarerushi/dialpad-django_poc/assets/65430906/8d8b188a-0a7d-4a42-b1ab-448eb2d090dd)

### delete user
![image](https://github.com/bhakarerushi/dialpad-django_poc/assets/65430906/0af1ab72-5fba-4d43-9697-ac82b0aefea5)

### If access_token is expired, use below Api,
![image](https://github.com/bhakarerushi/dialpad-django_poc/assets/65430906/96cfd6a9-0244-477a-856b-7543f109d838)











