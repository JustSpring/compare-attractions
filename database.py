import sqlite3
CREATE_ATTRACTION_TABLE4= "CREATE TABLE IF NOT EXISTS id_name (id INTERGER, name TEXT);"
CREATE_ATTRACTION_TABLE3= "CREATE TABLE IF NOT EXISTS final_data (id INTERGER, company TEXT,name TEXT, price INTERGER, discount INTEGER, plus_one INTEGER, points INTEGER,city TEXT, link TEXT);"
CREATE_ATTRACTION_TABLE2= "CREATE TABLE IF NOT EXISTS data3 (id INTERGER, link TEXT,name TEXT);"
CREATE_ATTRACTION_TABLE= "CREATE TABLE IF NOT EXISTS attractions (id INTERGER, company TEXT,name TEXT, price INTERGER, discount INTEGER, plus_one INTEGER, points INTEGER,city TEXT, link TEXT);"
INSERT_ATTRACTION= "INSERT INTO attractions(id,company,name,price,discount,plus_one,points,city,link) VALUES (?,?,?,?,?,?,?,?,?);"
INSERT_ATTRACTION2= "INSERT INTO data3(id,link,name) VALUES (?,?,?);"
INSERT_ATTRACTION3= "INSERT INTO final_data(id,company,name,price,discount,plus_one,points,city,link) VALUES (?,?,?,?,?,?,?,?,?);"
INSERT_ATTRACTION4= "INSERT INTO id_name(id,name) VALUES (?,?);"
GET_ALL_ATTRACTION= "SELECT * FROM attractions;"
GET_ALL_ATTRACTION_BY_NAME= "SELECT # FROM attractions WHERE link=?;"
def connect():
    return sqlite3.connect("data.db")
def connect2():
    return sqlite3.connect("data3.db")
def connect3():
    return sqlite3.connect("final_data.db")
def connect4():
    return sqlite3.connect("id_name.db")
def create_tables(connection):
    with connection:
        connection.execute(CREATE_ATTRACTION_TABLE)
def create_tables2(connection):
    with connection:
        connection.execute(CREATE_ATTRACTION_TABLE2)
def create_tables3(connection):
    with connection:
        connection.execute(CREATE_ATTRACTION_TABLE3)
def create_tables4(connection):
    with connection:
        connection.execute(CREATE_ATTRACTION_TABLE4)
def add_attraction(connection,id,company,name,price,discount,plus_one,points,city,link):
    with connection:
        connection.execute(INSERT_ATTRACTION, (id,company,name,price,discount,plus_one,points,city,link))
def add_attraction2(connection,id,link,name):
    with connection:
        connection.execute(INSERT_ATTRACTION2, (id,link,name))
def add_attraction3(connection,id,company,name,price,discount,plus_one,points,city,link):
    with connection:
        connection.execute(INSERT_ATTRACTION3, (id,company,name,price,discount,plus_one,points,city,link))
def add_attraction4(connection,id,name):
    with connection:
        connection.execute(INSERT_ATTRACTION4, (id,name))
def get_all_attraction(connection):
    with connection:
        return connection.execute(GET_ALL_ATTRACTION).fetchall()
def get_attraction_by_link(connection,name):
    with connection:
        return connection.execute(f"SELECT * FROM attractions WHERE link='{name}'")
        #return connection.execute(GET_ALL_ATTRACTION_BY_NAME, (name,)).fetchall()
def get_name_and_id_by_link(connection,name):
    with connection:
        return connection.execute(f"SELECT * FROM data3 WHERE link='{name}'")
def delete(connection,link):
     with connection:
         connection.execute(f"DELETE FROM data3 WHERE link = '{link}';")
