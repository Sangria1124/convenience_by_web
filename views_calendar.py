import flet as ft
from database import get_menus
import datetime

def calendar_view(conn):
    week_row = ft.Row(spacing=10, scroll=ft.ScrollMode.AUTO)

    def load_week():
        week_row.controls.clear()
        menus = {m[1]: m[2] for m in get_menus(conn)}
        monday = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        
        for i in range(7):
            day = monday + datetime.timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            recipe = menus.get(day_str, "")
            
            week_row.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(day.strftime('%a'), size=12),
                        ft.Text(day.strftime('%d'), size=18, weight="bold"),
                        ft.Text(recipe[:3] + ".." if len(recipe) > 3 else recipe, size=10)
                    ], horizontal_alignment="center"),
                    width=70, height=90, bgcolor=ft.colors.SURFACE_VARIANT, border_radius=10
                )
            )
        if week_row.page: week_row.update()

    content = ft.Column([ft.Text("週間カレンダー", size=25, weight="bold"), week_row])
    content.load_data = load_week
    load_week()
    return content