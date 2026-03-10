import flet as ft
from database import init_db, add_item, get_items, update_item_checked
from views_menus import menu_view
from views_calendar import calendar_view
from views_recipes import recipe_registration_view

def main(page: ft.Page):
    conn = init_db()
    page.title = "献立管理アプリ"
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- 1. 各画面の器（コンテナ）を先に作る ---
    display_area = ft.Column() # ← これを一番上に持ってくる

    # --- 2. 次に共通の「動き」を定義する ---
    
    def on_check(e):
        e.control.label_style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH) if e.control.value else None
        update_item_checked(conn, e.control.label, e.control.value)
        page.update()

    def refresh_items():
        # display_area が作られた後なので、もう NameError は出ません
        display_area.controls.clear()
        items = get_items(conn)
        for item in items:
            cb = ft.Checkbox(
                label=item[1], 
                on_change=on_check, 
                value=bool(item[2])
            )
            if cb.value:
                cb.label_style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
            display_area.controls.append(cb)
        
        if display_area.page:
            display_area.update()

    # --- 3. 他の画面の定義 ---
    
    menu_container = ft.Column(controls=[menu_view(conn, refresh_items)], visible=False)
    calendar_container = ft.Column(controls=[calendar_view(conn)], visible=False)
    recipe_container = ft.Column(controls=[recipe_registration_view(conn)], visible=False)

    # --- 4. ナビゲーション切り替え ---
    def on_nav_change(e):
        index = e.control.selected_index
        display_area.visible = (index == 0)
        menu_container.visible = (index == 1)
        recipe_container.visible = (index == 2)
        calendar_container.visible = (index == 3)
        page.floating_action_button.visible = (index == 0)

        if index == 3:
            if hasattr(calendar_container.controls[0], "load_data"):
                calendar_container.controls[0].load_data()
        
        if index == 1:
             if hasattr(menu_container.controls[0], "refresh_recipes"):
                menu_container.controls[0].refresh_recipes()
        page.update()

    # --- 5. 追加ダイアログ ---
    new_task = ft.TextField(hint_text="何を買いますか？")

    def add_clicked(e):
        if new_task.value == "": return
        add_item(conn, new_task.value)
        refresh_items()
        new_task.value = ""
        page.close(dialog)
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("材料の追加"),
        content=new_task,
        actions=[ft.TextButton("追加", on_click=add_clicked)],
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=lambda _: page.open(dialog),
    )

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART, label="材料"),
            ft.NavigationBarDestination(icon=ft.Icons.RESTAURANT, label="献立予約"),
            ft.NavigationBarDestination(icon=ft.Icons.MENU_BOOK, label="料理登録"),
            ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH, label="週間履歴"),
        ],
        on_change=on_nav_change,
    )

    # 全てのコンテナをページに追加
    page.add(display_area, menu_container, recipe_container, calendar_container)
    refresh_items()
    page.update()

if __name__ == "__main__":
    ft.app(main)