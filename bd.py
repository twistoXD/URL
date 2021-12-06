import sqlite3



def db_create():
    try:
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT));""")
        con.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links(
            id INTEGER,
            user_id INTEGER,
            link TEXT NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT),
            FOREIGN KEY(user_id) REFERENCES users(id));""")
        con.commit()
    except sqlite3.Error:
        print("Ошибка создания бд")
    finally:
        con.close()


def db_loginId(login):
    try:
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        user = cursor.execute("""SELECT login FROM users WHERE login = ?""",(login,)).fetchone()
        if not user:
            print("Вы можете зарегистрироваться")
            return 0
        else:
            print("Такой логин уже существует")
            return 1
    except sqlite3.Error:
        print("Ошибка в авторизации")
    finally:
        con.close()




def db_reg_user(login, password):
    try:
        print("Регистрация")
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute("""INSERT INTO users (login, password) VALUES(?, ?)""",(login, password,))
        con.commit()
        print("Вы успешно зарегистрировались")
    except sqlite3.Error:
        print("Ошибка регистрации")
        print(login)
    finally:
        con.close()



def db_auth(login, password):
    try:
        print("Авторизация")
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        user = cursor.execute("""SELECT * FROM users WHERE login = ? AND password = ?""",(login, password,)).fetchall()
        if len(user) == 0:
            print("Неверный логин или пароль")
            return 0
        else:
            print(user)
            return 1
    except sqlite3.Error:
        print("Ошибка авторизации")
    finally:
        con.close()


def getUserByLogin(login):
    try:
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        res = cursor.execute("""SELECT * FROM users WHERE login = ? LIMIT 1""",(login,)).fetchone()
        if not res:
            print('Такого пользователя не существует')
            return False   
        return res
    except sqlite3.Error as e:
        print('Ошибка получения данных из БД - getUserByLogin - ' + str(e))
    return False


def getUser(user_id):
    try:
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        res = cursor.execute("""SELECT * FROM users WHERE id = ? LIMIT 1""",(user_id,)).fetchone()
        if not res:
            print('Такого пользователя не существует')
            return False   
        return res
    except sqlite3.Error as e:
        print('Ошибка получения данных из БД - getUser - ' + str(e))
    return False





def db_getLinkPublic():
    try:
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        links = cursor.execute("""SELECT * FROM links""").fetchall()
        con.commit()
        print(links)
        return links
    except sqlite3.Error:
        print("Ошибка вывода ссылки")
    finally:
        con.close()

