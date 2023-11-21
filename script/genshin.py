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


if __name__ == '__main__':
    res = search_status_artifact("元素熟知")
    print(res)
