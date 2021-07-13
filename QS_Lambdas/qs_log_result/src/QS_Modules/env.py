import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_PWD = os.getenv("MYSQL_PWD")
MYSQL_ACCOUNT = os.getenv("MYSQL_ACCOUNT")
MYSQL_ROUTE = os.getenv("MYSQL_ROUTE")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

MONGO_HOST_EC2 = os.getenv("MONGO_HOST_EC2")
MONGO_PORT_EC2 = int(os.getenv("MONGO_PORT_EC2"))
MONGO_ADMIN_USERNAME_EC2 = os.getenv("MONGO_ADMIN_USERNAME_EC2")
MONGO_ADMIN_PASSWORD_EC2 = os.getenv("MONGO_ADMIN_PASSWORD_EC2")

MONGO_EC2_URI = f"mongodb://{MONGO_ADMIN_USERNAME_EC2}:{MONGO_ADMIN_PASSWORD_EC2}@{MONGO_HOST_EC2 }"
DRIVER_PATH = os.getenv('DRIVER_PATH')

ERROR_EMAIL = os.getenv('ERROR_EMAIL')
ERROR_PWD = os.getenv('ERROR_PWD')
MY_GMAIL = os.getenv('MY_GMAIL')