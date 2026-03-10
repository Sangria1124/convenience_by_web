import sqlite3

def init_db():
    conn = sqlite3.connect("todo.db", check_same_thread=False)
    cursor = conn.cursor()
    # 材料テーブル
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, checked INTEGER)")
    # 料理マスターテーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            ingredients TEXT,
            url TEXT
        )
    """)
    # 献立テーブル
    cursor.execute("CREATE TABLE IF NOT EXISTS menus (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, recipe_name TEXT)")
    conn.commit()
    return conn

def add_item(conn, name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, checked) VALUES (?, ?)", (name, 0))
    conn.commit()

def get_items(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    return cursor.fetchall()

def update_item_checked(conn, name, is_checked):
    cursor = conn.cursor()
    val = 1 if is_checked else 0
    cursor.execute("UPDATE items SET checked = ? WHERE name = ?", (val, name))
    conn.commit()

def add_master_recipe(conn, name, ingredients, url):
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO master_recipes (name, ingredients, url) VALUES (?, ?, ?)", (name, ingredients, url))
    conn.commit()

def get_master_recipes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM master_recipes ORDER BY name ASC")
    return cursor.fetchall()

def add_menu(conn, date_str, recipe_name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menus (date, recipe_name) VALUES (?, ?)", (date_str, recipe_name))
    conn.commit()

def get_menus(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menus ORDER BY date ASC")
    return cursor.fetchall()