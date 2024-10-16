def insertsql1(entity, cur):
    cur.execute('INSERT INTO users(surname, name,secondname, idtelegram,startdate,mentor) VALUES(?,?,?,?,?,?)', entity)


def insertsql2(entity, cur):
    cur.execute('INSERT INTO users(surname, name,secondname, idtelegram,startdate) VALUES(?,?,?,?,?)', entity)


def selectsql7(cur):
    cur.execute(
        "SELECT idtelegram,startdate FROM users WHERE julianday('now') - julianday(startdate) >= 7 and julianday('now') - julianday(startdate) < 8")
    return cur.fetchall()


def selectsql30(cur):
    cur.execute(
        "SELECT idtelegram,startdate FROM users WHERE julianday('now') - julianday(startdate) >= 30 and julianday('now') - julianday(startdate) < 31")
    return cur.fetchall()


def selectsql92(cur):
    cur.execute(
        "SELECT idtelegram,startdate FROM users WHERE julianday('now') - julianday(startdate) >= 92 and julianday('now') - julianday(startdate) < 93")
    return cur.fetchall()


def show_sql(bot, user_id, cur):
    cur.execute('select surname,name, idtelegram,startdate from users')
    i = 1
    for surname, name, user, date in cur.fetchall():
        bot.send_message(user_id, f"{i}) {surname} {name} - {user} - {date}")
        i += 1


def delete_user(userid, cur):
    cur.execute(f"delete from users where idtelegram = {userid}")

#
# def updatesql(entity, cur):
#     cur.execute('update users set surname = ?, name= ?,secondname= ?,startdate= ?,mentor= ? ', entity)
