from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<postgresserver>/<database_name>

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        print("yebo")
        yield db
    finally:
        db.close()

# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi',
#                             user='petermutisya', password='', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('database connection was successful')
# except Exception as err:
#     print("connecting to database failed")
#     print(err)
