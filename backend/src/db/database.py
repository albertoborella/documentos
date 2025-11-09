from fastapi import Depends
from sqlmodel import SQLModel, Field, Session, create_engine
from typing import Annotated

# Creo la base de datos
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Creo el motor de la base de datos
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Con la siguiente funcion creo la db y tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Creo la session
def get_session():
    with Session(engine) as session:
        yield session 

sessionDep = Annotated[Session, Depends(get_session)]


