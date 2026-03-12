import gspread
import json


import gspread

def init_db():
    # エラーメッセージの提案通り、引数名を 'credentials_filename' にします。
    # これで、gspread は AppData のデフォルトパスではなく、
    # 匠さんのプロジェクトフォルダにあるファイルを直接見に行くようになります。
    gc = gspread.oauth(
        credentials_filename="client_secret.json",
        authorized_user_filename="authorized_user.json"
    )
    
    # スプレッドシート名
    sheet = gc.open("献立管理DB")
    return sheet
# --- 材料（items）操作 ---
def add_item(sheet, name):
    ws = sheet.worksheet("items")
    # A列に名前、B列にチェック状態(0 or 1)
    ws.append_row([name, 0])

def get_items(sheet):
    ws = sheet.worksheet("items")
    data = ws.get_all_values()
    
    results = []
    for i, row in enumerate(data):
        # 1行目（見出し）を飛ばす
        if i == 0: continue
        
        name = row[0]
        # B列(row[1])に何か書いてあれば True、空なら False
        is_checked = True if len(row) > 1 and row[1] == "TRUE" else False
        
        results.append([i, name, is_checked])
    return results

def update_item_checked(sheet, name, is_checked):
    ws = sheet.worksheet("items")
    # 名前が一致するセルを探す
    cell = ws.find(name)
    if cell:
        val = 1 if is_checked else 0
        # 見つかった行の2列目（B列）を更新
        ws.update_cell(cell.row, 2, val)

# --- 料理マスター（master_recipes）操作 ---
def add_master_recipe(sheet, name, ingredients, url):
    ws = sheet.worksheet("master_recipes")
    cell = ws.find(name)
    if cell:
        # すでに存在する場合はその行を更新
        ws.update(f"A{cell.row}:C{cell.row}", [[name, ingredients, url]])
    else:
        # 新規追加
        ws.append_row([name, ingredients, url])

# database.py の get_master_recipes を修正
def get_master_recipes(sheet):
    ws = sheet.worksheet("master_recipes")
    data = ws.get_all_values()
    
    results = []
    for i, row in enumerate(data):
        # 1行目が見出し（料理名など）の場合は飛ばす
        if i == 0 and len(row) > 0 and row[0] == "料理名":
            continue
            
        # 列が足りない場合に備えてデフォルト値で埋める
        name = row[0] if len(row) > 0 else ""
        ingredients = row[1] if len(row) > 1 else ""
        url = row[2] if len(row) > 2 else ""
        
        if name: # 名前がある場合のみリストに追加
            results.append([i, name, ingredients, url])
            
    return results
# --- 献立（menus）操作 ---
def add_menu(sheet, date_str, recipe_name):
    ws = sheet.worksheet("menus")
    ws.append_row([date_str, recipe_name])

def get_menus(sheet):
    ws = sheet.worksheet("menus")
    data = ws.get_all_values()
    # (id, date, recipe_name)
    return [[i, row[0], row[1]] for i, row in enumerate(data)]