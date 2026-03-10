import flet as ft
from database import add_master_recipe

def recipe_registration_view(conn):
    name_input = ft.TextField(label="料理名", prefix_icon=ft.Icons.RESTAURANT)
    ingredients_input = ft.TextField(label="必要材料 (カンマ区切り)", multiline=True, hint_text="例: 肉, 玉ねぎ, 人参")
    url_input = ft.TextField(label="レシピURL", icon=ft.Icons.LINK)


    def save_clicked(e):
            if not name_input.value:
                e.page.show_snack_bar(ft.SnackBar(ft.Text("料理名を入力してください")))
                return
            
            # データベースに保存
            add_master_recipe(
                conn, 
                name_input.value, 
                ingredients_input.value, 
                url_input.value
            )
            
            # --- ここからが修正ポイント：入力欄を空にする ---
            name_input.value = ""
            ingredients_input.value = ""
            url_input.value = ""
            
            # 画面を更新して、空になったことを反映させる
            name_input.update()
            ingredients_input.update()
            url_input.update()
            # ----------------------------------------------
            
            e.page.show_snack_bar(ft.SnackBar(ft.Text("料理マスターに登録しました！")))


    return ft.Column([
        ft.Text("料理マスター登録", size=25, weight="bold"),
        name_input, ingredients_input, url_input,
        ft.ElevatedButton("保存", icon=ft.Icons.SAVE, on_click=save_clicked)
    ], scroll=ft.ScrollMode.AUTO, spacing=15)