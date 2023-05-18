import os

import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


#TODO: technically they should only be adding a level 1 character. Make the default level 1.
def new_character_handler(character):
  sql = '''
                INSERT INTO characters (first_name, last_name, skin, level, hot, cold, volatile, dark, id, server_id)
                VALUES (:first_name, :last_name, :skin, :level, :hot, :cold, :volatile, :dark, DEFAULT, :server_id)
            '''
  try:
    with engine.connect() as conn:
      conn.execute(text(sql), character)
      print(sql)
    return True
  except SQLAlchemyError:
    print("Error: character not created.")
    return False
