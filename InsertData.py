import mysql.connector
from mysql.connector import Error    
import csv

country = ['Argentina','Australia','Belgium','Brazil','Cameroon','Canada','Costa Rica','Croatia','Denmark','Ecuador','England','France','Germany','Ghana','IR Iran','Japan','Korea Republic','Mexico','Morocco','Netherlands','Poland','Portugal','Qatar','Saudi Arabia','Senegal','Serbia','Spain','Switzerland','Tunisia','Uruguay','USA','Wales']

country_code = ['ARG', 'AUS', 'BEL', 'BRA', 'CMR', 'CAN', 'CRC', 'CRO', 'DEN', 'ECU', 'ENG', 'FRA', 'GER', 'GHA', 'IRN', 'JPN', 'KOR', 'MEX', 'MAR', 'NED', 'POL', 'POR', 'QAT', 'KSA', 'SEN', 'SRB', 'ESP', 'SUI', 'TUN', 'URU', 'USA', 'WAL']

def insertCountry(cursor):
  record = []
  for co in country:
    filename = './data/Country/' + co + '/team.csv' 
    with open(filename, 'r', encoding='utf-8') as f:
      for items in csv.reader(f):
        record.append((items[1], items[0]))
  query = 'INSERT INTO Country(country_code, country_name) values (%s, %s);'  
  cursor.executemany(query, record) 

def insertTeam(cursor):
  record = []
  for co in country:
    filename = './data/Country/' + co + '/team.csv' 
    with open(filename, 'r', encoding='utf-8') as f:
      for items in csv.reader(f):
        record.append((items[2],items[1],0,0,0,0,0,0,0,0))
  query = 'INSERT INTO Team values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
  cursor.executemany(query,record)

def insertPosition(cursor):
  record = [('GK','Goalkeeper'),('DF','Defender'),('MF','Midfielder'),('FW','Forward')]
  query = 'INSERT INTO Position values (%s, %s);'
  cursor.executemany(query, record)

def convertDate(s): #DOB format in player.csv: DD-MM-YYYY, MySQL format : YYYY-MM-DD
  d, m, y = s.split('-')
  return "-".join((y, m, d))

def insertPlayer(cursor): #insert player csv into player Table
  record = []
  for idx in range(len(country)): #country: list of 32 countries name
    team_id = idx + 1    # team_id increases from 1
    filename = './data/Country' + country[idx] + '/player.csv'
    with open(filename, 'r', encoding='utf-8') as f:
      for items in csv.reader(f): #Excluding the row representing column information
        if items[0].startswith('\ufeff') : continue 
        record.append((team_id,*items[0 : 6],convertDate(items[6]),*items[7 :]))
  query = 'INSERT INTO Player values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
  cursor.executemany(query,record)

def insertCoach(cursor):
  record = []
  for idx in range(len(country)):
    team_id = idx + 1
    filename = './data/Country' + country[idx] + '/coach.csv'
    with open(filename, 'r', encoding='utf-8') as f:
      for items in csv.reader(f):
        if items[0].startswith('\ufeff') : continue
        record.append((team_id, *items))
  query = 'INSERT INTO Coach values (NULL,%s,%s,%s,%s,%s,%s);'
  cursor.executemany(query,record)

def insertReferee(cursor):
  record = []
  filename = './data/referee.csv'
  with open(filename, encoding='utf-8') as f:
    for items in csv.reader(f):
      record.append(tuple(items))
  query = 'INSERT INTO Referee values (NULL,%s);'
  cursor.executemany(query,record)
  
def insertAsstRef(cursor):
  record = []
  filename = './data/assistant_referee.csv'
  with open(filename, encoding='utf-8') as f:
    for items in csv.reader(f):
      record.append(tuple(items))
  query = 'INSERT INTO asst_ref values (NULL,%s);'
  cursor.executemany(query,record)

def insertStadium(cursor):
  record = []
  filename = './data/stadium.csv'
  with open(filename, encoding='utf-8') as f:
    for items in csv.reader(f):
      record.append(tuple(items))
  query = 'INSERT INTO Stadium values (NULL,%s,%s,%s);'
  cursor.executemany(query,record)

def insertData(cursor):
  insertCountry(cursor)
  insertTeam(cursor)
  insertPosition(cursor)
  insertPlayer(cursor)
  insertCoach(cursor)
  insertReferee(cursor)
  insertAsstRef(cursor)
  insertStadium(cursor)

  
if __name__ == "__main__":
  try :
    connection = mysql.connector.connect( host = 'localhost', database = 'mydata', user = 'root', password = 'mydideockd1!')
    if connection.is_connected() :
        cursor = connection.cursor()
        insertData(cursor)
        connection.commit()
  except Error as e :
      print('Error : ', e)        
  finally :                      
      cursor.close()
      connection.close()
      print('CLose MySQL Connection') 