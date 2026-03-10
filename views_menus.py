import flet as ft
from database import get_master_recipes, add_menu, add_item
import datetime
import re

def menu_view(conn, on_task_added):
    selected_date = datetime.date.today()
    
    dropdowns_list = []
    dropdowns_container = ft.Column(spacing=10)

    def get_recipe_options():
        recipes = get_master_recipes(conn)
        return [ft.dropdown.Option(r[1]) for r in recipes]

    def add_dropdown_field(e=None):
        new_dd = ft.Dropdown(
            label=f"料理 {len(dropdowns_list) + 1}",
            options=get_recipe_options(),
            expand=True,
            on_change=on_dropdown_change
        )
        dropdowns_list.append(new_dd)
        dropdowns_container.controls.append(new_dd)
        
        # --- 修正ポイント：pageがある場合（画面表示後）のみupdateする ---
        if dropdowns_container.page:
            dropdowns_container.update()

    def on_dropdown_change(e):
        if all(dd.value is not None for dd in dropdowns_list):
            add_dropdown_field()

    def handle_date_change(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value.date()
            date_button.text = f"日付: {selected_date.strftime('%Y-%m-%d')}"
            date_button.update()

    date_picker = ft.DatePicker(on_change=handle_date_change)

    date_button = ft.ElevatedButton(
        f"日付: {selected_date.strftime('%Y-%m-%d')}",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: date_button.page.open(date_picker)
    )

    def add_clicked(e):
        date_str = selected_date.strftime('%Y-%m-%d')
        recipes_master = get_master_recipes(conn)
        added_any = False

        for dd in dropdowns_list:
            recipe_name = dd.value
            if not recipe_name: continue
            
            add_menu(conn, date_str, recipe_name)
            
            target = next((r for r in recipes_master if r[1] == recipe_name), None)
            if target and target[2]:
                items = re.split(r'[,\n、\s]+', target[2])
                for item in items:
                    if item.strip():
                        add_item(conn, item.strip())
            added_any = True

        if added_any:
            on_task_added()
            dropdowns_list.clear()
            dropdowns_container.controls.clear()
            add_dropdown_field()
            # SnackBarの新しい表示方法（e.page.show_snack_bar）
            e.page.show_snack_bar(ft.SnackBar(ft.Text("全ての料理を予約し、材料を追加しました！")))
        else:
            e.page.show_snack_bar(ft.SnackBar(ft.Text("料理を選択してください")))

    # 初期化時に1つ作成（この時点ではupdateは呼ばれない）
    add_dropdown_field()

    content = ft.Column([
        ft.Text("未来の献立を予約する", size=20, weight=ft.FontWeight.BOLD),
        date_button,
        ft.Text("作る料理をすべて選択してください：", size=14, color=ft.colors.OUTLINE),
        dropdowns_container,
        ft.ElevatedButton("この内容で一括予約", icon=ft.Icons.DONE_ALL, on_click=add_clicked),
    ], spacing=15, scroll=ft.ScrollMode.AUTO)
    
    def refresh_recipes():
        options = get_recipe_options()
        for dd in dropdowns_list:
            dd.options = options
        # --- ここも修正：画面表示後のみupdate ---
        if dropdowns_container.page:
            dropdowns_container.update()

    content.refresh_recipes = refresh_recipes
    return content