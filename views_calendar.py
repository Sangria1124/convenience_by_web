import flet as ft
from database import get_menus
import datetime

def calendar_view(conn):
    # スクロール可能な行を作成
    week_row = ft.Row(spacing=10, scroll=ft.ScrollMode.AUTO)

    def load_week():
        week_row.controls.clear()
        # get_menus は [id, date, recipe_name] を返すので
        # 日付(m[1])をキー、料理名(m[2])を値にした辞書を作る
        menus = {m[1]: m[2] for m in get_menus(conn)}
        
        # 今週の月曜日を計算
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        
        for i in range(7):
            day = monday + datetime.timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            recipe = menus.get(day_str, "")
            
            week_row.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(day.strftime('%a'), size=12),
                        ft.Text(day.strftime('%d'), size=18, weight="bold"),
                        # 料理名が長い場合は省略表示
                        ft.Text(recipe[:3] + ".." if len(recipe) > 3 else recipe, size=10)
                    ], horizontal_alignment="center", spacing=2),
                    width=70, 
                    height=90, 
                    bgcolor="surfacevariant", # 小文字の文字列指定で安全に
                    border_radius=10,
                    padding=5
                )
            )
        
        # --- 修正ポイント：try-exceptでガード ---
        try:
            if week_row.page:
                week_row.update()
        except Exception:
            # ページに追加される前のupdate呼び出しは無視する
            pass

    content = ft.Column([
        ft.Text("週間カレンダー", size=25, weight="bold"), 
        week_row
    ])

    # --- 修正ポイント：AttributeError対策 ---
    # 直接 content.load_data とせず、Flet推奨の data 属性に保存する
    content.data = load_week
    
    # 最初の組み立て（ここでは update() は走らないようにガード済み）
    load_week()
    
    return content