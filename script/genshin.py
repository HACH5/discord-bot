import sqlite3

def element_color(element_name):
    match element_name:
        case '炎':
            return '#ff0000'
        case '水':
            return '#0000ff'
        case '氷':
            return '#a0d8ef'
        case '雷':
            return '#800080'
        case '風':
            return '#bee0c2'
        case '草':
            return '#008000'
        case '岩':
            return '#ffa500'

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

def search_artifact_id(artifact_name):
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"select artifact_id from artifact where artifact_ja_name like '%{artifact_name}%'")
    r = cur.fetchall()
    con.close()
    return r

def search_chara_artifact_name(name):
    n = search_name_character(name)
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"""select chara_ja_name, rarity, element_ja_name, type_ja_name, artifact_ja_name, ja_best_main_sand_status, ja_best_main_goblet_status, ja_best_main_crown_status, 
                from artifact_character natural join character_type natural join character 
                natural join artifact natural join element
                where chara_id = {n[0][0]}""")
    r = cur.fetchall()
    con.close()
    return r

def search_chara_artifact_artifact(artifact):
    id = search_artifact_id(artifact)
    con = sqlite3.connect("database/genshin.db")
    cur = con.cursor()
    cur.execute(f"""select chara_ja_name, rarity, element_ja_name, type_ja_name, artifact_ja_name, ja_best_main_sand_status, ja_best_main_goblet_status, ja_best_main_crown_status
                from artifact_character natural join character_type natural join character 
                natural join artifact natural join element
                where artifact_id = {id[0][0]}""")
    r = cur.fetchall()
    con.close()
    return r

if __name__ == '__main__':
    res = search_chara_artifact_artifact("林")
    print(res)
