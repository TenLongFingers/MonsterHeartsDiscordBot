import os

import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError, ProgrammingError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

#engines and permissions
CONNECTION_STRING = os.environ['CONNECTION_STRING']
engine = create_engine(CONNECTION_STRING, isolation_level="AUTOCOMMIT")


#GET STATS
def get_character_stat_handler(server_id, name, stat):
  sql = text(
    f'''SELECT {stat} FROM characters WHERE server_id = :server_id AND first_name = :name'''
  )
  with engine.connect() as conn:
    # try:
    result = conn.execute(sql, {"server_id": str(server_id), "name": name})
  #TODO: add error handling so this return message is sent as a discord message
  # except ProgrammingError:
  #   #stat doesn't exist in the game
  #   return f"{stat} isn't a stat in Monsterhearts"
  row = result.fetchone()

  if row is None:
    return None

  return row[0]
