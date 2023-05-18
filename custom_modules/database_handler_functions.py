import os

import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

#engines and permissions
CONNECTION_STRING = os.environ['CONNECTION_STRING']
engine = create_engine(CONNECTION_STRING, isolation_level="AUTOCOMMIT")

#variables


# Gets all characters and their stat block
def character_list_handler(server_id):
  sql = text("SELECT * FROM characters WHERE server_id = :server_id")
  with engine.connect() as conn:
    result = conn.execute(sql, {"server_id": str(server_id)})
    rows = result.fetchall()

  df = pd.DataFrame(rows, columns=result.keys())
  return df


# Gets single character stat block
def character_sheet_handler(name, server_id):
  sql = text(
    "SELECT first_name, last_name, skin, hot, cold, volatile, dark, level FROM characters WHERE first_name = :name AND server_id = :server_id"
  )
  try:
    with engine.connect() as conn:
      df = conn.execute(sql, {
        "name": name,
        "server_id": str(server_id)
      }).fetchall()

    if not df:
      return None

    return pd.DataFrame(df,
                        columns=[
                          "first_name", "last_name", "skin", "hot", "cold",
                          "volatile", "dark", "level"
                        ])

  except NoResultFound:
    return None


# Add new character
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
  except IntegrityError as e:
    print(
      f"Error: character not created due to an integrity error.\n{e}\n{character}\n{sql}"
    )
  except DataError as e:
    print(
      f"Error: character not created due to a data error.\n{e}\n{character}\n{sql}"
    )
  except SQLAlchemyError as e:
    print(f"Error: character not created.\n{e}\n{character}\n{sql}")
  return False


# Delete character and their associated conditions
def delete_character_handler(name, server_id):
  try:
    with engine.connect() as conn:
      # Find the character's ID
      sql_select = text(
        "SELECT id FROM characters WHERE server_id = :server_id AND first_name = :name"
      )
      result_select = conn.execute(sql_select, {
        "name": name,
        "server_id": str(server_id)
      })
      character_id = result_select.fetchone()
      if character_id is None:
        return False

      # Checks to see if the character has any conditions
      sql_conditions_check = text(
        '''SELECT id FROM conditions WHERE id = :character_id''')
      result_conditions = conn.execute(sql_conditions_check,
                                       {"character_id": character_id[0]})
      conditions_exist = result_conditions.fetchone() is not None

      # Delete the character and their associated conditions (if conditions exist)
      if conditions_exist:
        sql_delete_conditions = text(
          '''DELETE FROM conditions WHERE id = :character_id; \
                    DELETE FROM characters WHERE id = :character_id;''')
        result_delete = conn.execute(sql_delete_conditions,
                                     {"character_id": character_id[0]})

      # (if conditions don't exist)
      else:
        sql_delete_no_conditions = text(
          '''DELETE FROM characters WHERE id = :character_id''')
        result_delete = conn.execute(sql_delete_no_conditions,
                                     {"character_id": character_id[0]})

      if result_delete.rowcount > 0:
        return True
      else:
        return False
  except SQLAlchemyError:
    print("Error: character not deleted ", sql_delete_conditions,
          sql_delete_no_conditions, sql_select, name, server_id, character_id,
          character_id[0])
    return False


# add condition
def add_condition_handler(name, server_id, condition):
  try:
    # get character id
    with engine.connect() as conn:
      result = conn.execute(
        text(
          "SELECT id FROM characters WHERE first_name = :name AND server_id = :server_id"
        ), {
          "name": name,
          "server_id": str(server_id)
        })
      character_id = result.scalar()

    # insert condition
    with engine.connect() as conn:
      conn.execute(
        text(
          "INSERT INTO conditions (id, condition) VALUES (:character_id, :condition)"
        ), {
          "character_id": character_id,
          "condition": condition.capitalize()
        })
    return True
  except SQLAlchemyError:
    print(
      f'''Error: Condition not added. Here's what the database_functions module tried to push to the database:\n \n \n name = {name} \n character_id = {character_id} \n id = {id} \n server_id = {server_id} \n condition = {condition}'''
    )
    return False


#NPC ADD CONDITIONS TODO: I started this functionality then stopped for time. Include this functionality in a later patch. For now, only player characters can have conditions. Also, take the advice you were given. Give npcs their own conditions table. Otherwise you have no way of ensuring that a character id won't be the same as an npc id.
def add_npc_condition(name, condition, server_id):
  try:
    # Get NPC ID
    with engine.connect() as conn:
      result = conn.execute(
        text(
          "SELECT id FROM npcs WHERE first_name = :name AND server_id = :server_id"
        ), {
          "name": name,
          "server_id": str(server_id)
        })
      npc_id = result.scalar()

    # Insert condition
    with engine.connect() as conn:
      conn.execute(
        text(
          "INSERT INTO conditions (npc_id, condition) VALUES (:npc_id, :condition)"
        ), {
          "npc_id": npc_id,
          "condition": condition.capitalize()
        })
    return True
  except SQLAlchemyError:
    print(
      f'''Error: Condition not added. Here's what the database_functions module tried to push to the database:\n \n \n name = {name} \n npc_id = {npc_id} \n server_id = {server_id} \n condition = {condition}'''
    )
    return False


#GET CONDITIONS
def get_conditions_handler(name, server_id):
  with engine.connect() as conn:
    result = conn.execute(
      text(
        "SELECT characters.id, first_name, last_name FROM characters "
        "JOIN conditions "
        "ON characters.id = conditions.id "
        "WHERE characters.first_name = :name AND characters.server_id = :server_id "
      ), {
        "name": name,
        "server_id": server_id
      })
    rows = result.fetchall()
    if rows:
      conditions_arr = []
      for row in rows:
        id, first_name, last_name = row
        if id not in conditions_arr:
          conditions_arr.append(id)
      # extract conditions
      conditions = []
      for condition_id in conditions_arr:
        sql = text("SELECT condition FROM conditions WHERE id = :id")
        with engine.connect() as conn:
          result = conn.execute(sql, {"id": condition_id})
          for row in result:
            conditions.append(row[0])
      return (first_name, last_name, conditions, True)
    else:
      return (None, None, None, False)


#DELETE CONDITIONS
def delete_condition_handler(name, condition, server_id):
  try:
    with engine.connect() as conn:
      #find character's ID
      sql_select = text(
        "SELECT id FROM characters WHERE server_id = :server_id AND first_name = :name"
      )
      result_select = conn.execute(sql_select, {
        "name": name,
        "server_id": str(server_id)
      })
      character_id = result_select.fetchone()
      if character_id is None:
        return False

      #delete condition
      sql_delete = text(
        "DELETE FROM conditions WHERE id = :id AND condition = :condition")
      result_delete = conn.execute(sql_delete, {
        "id": character_id[0],
        "condition": condition
      })

      if result_delete.rowcount > 0:
        return True
      else:
        return False
  except SQLAlchemyError:
    print("Error: condition not deleted")


#ADD NPCS
def new_npc_handler(first_name, last_name, server_id):
  sql = '''
  INSERT INTO npcs (first_name, last_name, server_id)
  VALUES (:first_name, :last_name, :server_id)'''

  try:
    with engine.connect() as conn:
      conn.execute(text(sql), {
        "first_name": first_name,
        "last_name": last_name,
        "server_id": server_id
      })
    return True
  except SQLAlchemyError:
    print(
      f"ERROR: npc not added. Here's what SQLAlchemy sent to the database:\n \n {first_name} \n {last_name} \n {server_id}"
    )


# DELETE NPCS
def delete_npc_handler(first_name, last_name, server_id):
  sql = '''
  DELETE FROM npcs
  WHERE first_name = :first_name AND last_name = :last_name AND server_id = :server_id
  '''
  try:
    with engine.connect() as conn:
      conn.execute(text(sql), {
        "first_name": first_name,
        "last_name": last_name,
        "server_id": server_id
      })
    return True
  except SQLAlchemyError:
    raise Exception(
      f'''Error in backend. Here's what it tried to pass to the database: \n {sql} \n {first_name} \n {last_name} \n {server_id}'''
    )
    return False
  except DataError:
    raise Exception()
  except IntegrityError:
    raise Exception()


#ADD STRINGS TODO: add string functionality. It should be very similar to conditions.
# def add_string_handler(giver_name, taker_name, string_description)
