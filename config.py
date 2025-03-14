import os

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@db:3306/mydatabase")
