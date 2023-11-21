import sqlite3

def search_artifact(name):
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"select * from artifact where artifact_ja_name like '%{name}%'")
    r = cur.fetchall()
    con.close()
    return r

if __name__ == '__main__':
    res = search_artifact("女")
    for artifact in res:
        print(artifact)
        print(artifact[0])
        print(artifact[7])
