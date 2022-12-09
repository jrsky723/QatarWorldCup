import mysql.connector
from mysql.connector import Error   
from vo import *

class Dao:
  def __init__(self):
    self.conn = None
  
  def connect(self):
    self.conn = mysql.connector.connect( host = 'localhost', database = 'mydata', user = 'root', password = 'mydideockd1!')

  def disconn(self):
    self.conn.close()

  def insert_by_id(self, a):
    try:
      self.connect()
      table = type(a).__name__
      values = 'NULL,' + ','.join(f"'{str(x)}'" for x in vars(a).values())
      cursor = self.conn.cursor()
      sql = f'insert into `{table}` values ({values});'
      cursor.execute(sql)
      self.conn.commit()
    except Error as e:
      print(e)
    finally:
      self.disconn()
    
  def insert_no_id(self, a):
    try:
      self.connect()
      table = type(a).__name__
      values = ','.join(f"'{str(x)}'" for x in vars(a).values())
      cursor = self.conn.cursor()
      sql = f'insert into `{table}` values ({values});'
      cursor.execute(sql)
      self.conn.commit()
    except Error as e:
      print(e)
    finally:
      self.disconn()

  def select_by_val(self, table:str, wheres:dict = None):
    try:
      self.connect()
      cursor = self.conn.cursor()
      if wheres == None:
        sql = f'SELECT * from `{table}`;'
      else:
        cond = ' and '.join(f'`{column}` = {val}' for column, val in wheres.items())
        sql = f'select * from `{table}` where {cond};'
      cursor.execute(sql)
      return cursor.fetchall()
    except Exception as e:
      print(e)
    finally:
      self.disconn()

  def delete_by_Val(self, table:str, wheres:dict = None):
    try:
      self.connect()
      cursor = self.conn.cursor()
      if wheres == None:
        sql = f'TRUNCATE TABLE `{table}`'
      else:
        cond = ' and '.join(f'`{column}` = {val}' for column, val in wheres.items())
        sql = f'DELETE * from `{table}` where {cond};'
      cursor.execute(sql)
      self.conn.comit()
    except Exception as e:
      print(e)
    finally:
      self.disconn()

  def update_by_val(self,table:str, sets:dict = None, wheres:dict = None):
    try:
      self.connect()
      cursor = self.conn.cursor()
      if sets == None: return
      else :
        set_cond = ' , '.join(f'`{column}` = {val}' for column, val in sets.items())
        if wheres == None:
          sql = f'UPDATE `{table}` SET {set_cond};'
        else:
          where_cond = ' and '.join(f'`{column}` = {val}' for column, val in wheres.items())
          sql = f'UPDATE `{table}` SET {set_cond} WHERE {where_cond};'
      cursor.execute(sql)
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.disconn()

  def get_count(self, table:str, wheres:dict = None):
    try:
      self.connect()
      cursor = self.conn.cursor()
      if wheres == None:
        sql = f'SELECT count(*) from `{table}`;'
      else:
        cond = ' and '.join(f'`{column}` = {val}' for column, val in wheres.items())
        sql = f'select count(*) from `{table}` where {cond};'
      cursor.execute(sql)
      return cursor.fetchone()[0]
    except Exception as e:
      print(e)
    finally:
      self.disconn()

  def team_id_by_country(self,country_name:str):
    try:
      self.connect()
      cursor = self.conn.cursor()
      sql = f"SELECT team_id from Team WHERE country_code = (SELECT country_code from `Country` where country_name = '{country_name}');"
      cursor.execute(sql)
      return cursor.fetchone()[0]
    except Exception as e:
      print(e)
    finally:
      self.disconn()

if __name__ == '__main__':
  dao = Dao()
  print(dao.get_count('Match'))