import sqlite3

def connectDatabase():
    database = sqlite3.connect('DatabaseList/weatherBot.db')
    databaseCursor = database.cursor()
    return databaseCursor, database

def updateDatabase(name: str, id: int, lat: float, lon: float):
    listDatabase = connectDatabase()
    databaseCursor = listDatabase[0]
    database = listDatabase[1]
    try:
        if databaseCursor.execute(f"SELECT lat FROM users WHERE lat == {lat}").fetchone()[0] != lat and databaseCursor.execute(f"SELECT lon FROM users WHERE lon == {lon}").fetchone()[0] != lon:
            databaseCursor.execute(f"INSERT INTO users VALUES ('{name}', {id}, {lon}, {lat})")
            database.commit()
            database.close()
        else:
            database.close()
    except:
        databaseCursor.execute(f"INSERT INTO users VALUES ('{name}', {id}, {lon}, {lat})")
        database.commit()
        database.close()

def deleteElementDatabase(id: int):
    listDatabase = connectDatabase()
    databaseCursor = listDatabase[0]
    database = listDatabase[1]
    databaseCursor.execute(f"DELETE FROM users WHERE user_id == {id}")
    database.commit()
    database.close()

def lockDatabase():
    listDatabase = connectDatabase()
    databaseCursor = listDatabase[0]
    database = listDatabase[1]
    listUsers = databaseCursor.execute("SELECT * FROM users")
    listUsers = listUsers.fetchall()
    database.close()
    return listUsers
