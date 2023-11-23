import sqlite3

def search_name_artifact(name):
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"select * from artifact where artifact_ja_name like '%{name}%'")
    r = cur.fetchall()
    con.close()
    return r

def search_status_artifact(detail):
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"select * from artifact where ja_artifact_4_detail like '%{detail}%'")
    r = cur.fetchall()
    con.close()
    return r

def search_name_character(name):
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"select * from character where chara_ja_name like '%{name}%'")
    r = cur.fetchall()
    con.close()
    return r

def search_birthday_character(birthday):
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"select * from character where birthday like '%{birthday}%'")
    r = cur.fetchall()
    con.close()
    return r

def search_place_name(place_id):
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"select place_ja_name from place where place_id = {place_id}")
    r = cur.fetchall()
    con.close()
    return r

def search_element_name(element_id):
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"select element_ja_name from element where element_id= {element_id}")
    r = cur.fetchall()
    con.close()
    return r

if __name__ == '__main__':
    res = search_birthday_character("09")
    print(res)
