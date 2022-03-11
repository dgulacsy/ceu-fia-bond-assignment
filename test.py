import os
from dotenv import load_dotenv

load_dotenv('./venv/.env')
print(os.environ.get('SQLALCHEMY_DATABASE_URI'))