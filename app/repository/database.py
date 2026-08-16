from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL =  ("postgresql+psycopg://postgres:password@localhost:5432/FinTracker")

engine = create_engine(
    DATABASE_URL
)

#для каждого запроса свое соединение с бд
# (engine - точка входа,
# connection - конкретное соединение для взаимодействия,
# session - пользователь соединения

#autoflush - хз потом узнаю, вообще для не-auto запросов в БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
