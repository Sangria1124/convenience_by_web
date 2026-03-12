import flet as ft
from database import get_master_recipes, add_menu, add_item
import datetime
import re

class MenuComponent(ft.Column):
    def __init__(self, conn, on_task_added):
        super().__init__(spacing=15, scroll=ft.ScrollMode.AUTO)
        self.conn = conn
        self.on_task_added = on_task_added
        self.selected_date = datetime.date.today()
        self.dropdowns_list = []
        
        # パーツ準備
        self.dropdowns_container = ft.Column(spacing=10)
        self.date_picker = ft.DatePicker(on_change=self.handle_date_change)
        
        self.date_button = ft.ElevatedButton(
            f"日付: {self.selected_date.strftime('%Y-%m-%d')}",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda _: self.page.open(self.date_picker)
        )

        # 画面の組み立て
        self.controls = [
            ft.Text("未来の献立を予約する", size=20, weight="bold"),
            self.date_button,
            self.date_picker,
            ft.Text("作る料理を選択してください：", size=14, color="outline"),
            self.dropdowns_container,
            # ★自動ではなく、このボタンで確実に増やす！
            ft.TextButton("＋ 別の料理を追加", icon=ft.Icons.ADD, on_click=lambda _: self.add_dropdown_field()),
            ft.Divider(),
            ft.ElevatedButton("この内容で一括予約", icon=ft.Icons.DONE_ALL, on_click=self.add_clicked, width=200),
        ]

    def did_mount(self):
        if not self.dropdowns_list:
            self.add_dropdown_field()

    def get_recipe_options(self):
        recipes = get_master_recipes(self.conn)
        return [ft.dropdown.Option(r[1]) for r in recipes]

    def add_dropdown_field(self):
        new_dd = ft.Dropdown(
            label=f"料理 {len(self.dropdowns_list) + 1}",
            options=self.get_recipe_options(),
            expand=True,
        )
        self.dropdowns_list.append(new_dd)
        self.dropdowns_container.controls.append(new_dd)
        
        # ページ全体の更新を試みる
        if self.page:
            self.page.update()
        else:
            self.update()

    def handle_date_change(self, e):
        if e.control.value:
            self.selected_date = e.control.value.date()
            self.date_button.text = f"日付: {self.selected_date.strftime('%Y-%m-%d')}"
            self.page.update()

    def add_clicked(self, e):
        date_str = self.selected_date.strftime('%Y-%m-%d')
        recipes_master = get_master_recipes(self.conn)
        added_any = False

        for dd in self.dropdowns_list:
            if not dd.value: continue
            add_menu(self.conn, date_str, dd.value)
            target = next((r for r in recipes_master if r[1] == dd.value), None)
            if target and target[2]:
                items = re.split(r'[,\n、\s]+', target[2])
                for item in items:
                    if item.strip(): add_item(self.conn, item.strip())
            added_any = True

        if added_any:
            self.on_task_added()
            self.dropdowns_list.clear()
            self.dropdowns_container.controls.clear()
            self.add_dropdown_field()
            self.page.overlay.append(ft.SnackBar(ft.Text("予約完了！"), open=True))
        self.page.update()

    def refresh_data(self):
        options = self.get_recipe_options()
        for dd in self.dropdowns_list:
            dd.options = options
        try:
            self.update()
        except:
            pass

def menu_view(conn, on_task_added):
    return MenuComponent(conn, on_task_added)