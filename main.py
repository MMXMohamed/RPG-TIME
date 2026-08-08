import flet as ft
import time
import threading

def main(page: ft.Page):
    # ------------------- إعدادات الصفحة والشاشة -------------------
    page.title = "AFK Life - Gamer Time Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0E0E12"  # خلفية داكنة جداً للألعاب
    page.padding = 20
    page.scroll = "adaptive"

    # ------------------- متغيرات الـ Gamification -------------------
    user_data = {
        "level": 1,
        "xp": 0,
        "xp_needed": 100
    }

    # ------------------- مكونات الهيدر والشعار (AFK Logo) -------------------
    logo_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("AFK", font_family="monospace", size=22, weight=ft.FontWeight.BOLD, color="#00D2FF"),
                    padding=10,
                    border_radius=12,
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                        colors=["#7928CA", "#00D2FF"],
                    )
                ),
                ft.Column(
                    controls=[
                        ft.Text("AFK LIFE", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ft.Text("Level Up Your Real Life", size=12, color="#8E8E93"),
                    ],
                    spacing=2
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=15,
        border_radius=15,
        bgcolor="#16161E",
    )

    # ------------------- كارت الـ Avatar والـ XP -------------------
    level_text = ft.Text(f"Level {user_data['level']}", size=16, weight=ft.FontWeight.BOLD, color="#00D2FF")
    xp_text = ft.Text(f"XP: {user_data['xp']}/{user_data['xp_needed']}", size=12, color="#A0A0A0")
    
    xp_progress_bar = ft.ProgressBar(
        value=0,
        color="#7928CA",
        bgcolor="#232331",
        height=10,
    )

    profile_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row([ft.Text("🛡️", size=16), level_text]),
                        xp_text
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(height=5),
                xp_progress_bar
            ]
        ),
        padding=15,
        border_radius=15,
        bgcolor="#16161E",
    )

    def update_xp(amount):
        user_data["xp"] += amount
        if user_data["xp"] >= user_data["xp_needed"]:
            user_data["level"] += 1
            user_data["xp"] -= user_data["xp_needed"]
            user_data["xp_needed"] = int(user_data["xp_needed"] * 1.5)
            
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"🎉 LEVEL UP! وصلت للمستوى {user_data['level']}"),
                bgcolor="#7928CA"
            )
            page.snack_bar.open = True

        level_text.value = f"Level {user_data['level']}"
        xp_text.value = f"XP: {user_data['xp']}/{user_data['xp_needed']}"
        xp_progress_bar.value = user_data["xp"] / user_data["xp_needed"]
        page.update()

    # ------------------- قسم الـ Raid Timer -------------------
    timer_display = ft.Text("00:00", size=32, weight=ft.FontWeight.BOLD, color="#FFFFFF")
    timer_input = ft.TextField(
        label="وقت اللعب (بالدقائق)", 
        border_color="#7928CA", 
        focused_border_color="#00D2FF",
        width=200,
        text_size=14,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    def run_timer(minutes):
        total_seconds = int(minutes * 60)
        remaining = total_seconds

        while remaining > 0:
            mins, secs = divmod(remaining, 60)
            timer_display.value = f"{mins:02d}:{secs:02d}"
            page.update()
            time.sleep(1)
            remaining -= 1

        timer_display.value = "00:00"
        page.snack_bar = ft.SnackBar(
            content=ft.Text("⚔️ Raid Time is Over! قوم خد استراحة وخف عينك يا بطل."),
            bgcolor="#00D2FF"
        )
        page.snack_bar.open = True
        page.update()

    def start_raid_click(e):
        try:
            mins = float(timer_input.value)
            if mins > 0:
                threading.Thread(target=run_timer, args=(mins,), daemon=True).start()
        except (ValueError, TypeError):
            pass

    raid_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("⏱️ Gaming Raid Timer", size=16, weight=ft.FontWeight.BOLD, color="#00D2FF"),
                ft.Row([timer_input, timer_display], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=5),
                ft.Button(
                    content=ft.Text("START RAID ⚔️", weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    style=ft.ButtonStyle(
                        bgcolor={"": "#7928CA"},
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    width=400,
                    on_click=start_raid_click
                )
            ]
        ),
        padding=15,
        border_radius=15,
        bgcolor="#16161E",
    )

    # ------------------- قسم الـ Daily Quests -------------------
    quests_list = [
        {"title": "📖 ذاكر / اشتغل لمدة 60 دقيقة", "xp": 50},
        {"title": "🏋️ تمرينة الجيم اليومية", "xp": 40},
        {"title": "💧 شرب 3 لتر مية", "xp": 20},
        {"title": "😴 نوم بدري قبل 12", "xp": 30},
    ]

    quest_controls = []
    for q in quests_list:
        def make_check_handler(quest_data):
            def on_change(e):
                if e.control.value:
                    update_xp(quest_data["xp"])
                    e.control.disabled = True
                    page.update()
            return on_change

        cb = ft.Checkbox(
            label=f"{q['title']} (+{q['xp']} XP)",
            value=False,
            check_color="#00D2FF",
            active_color="#7928CA",
            on_change=make_check_handler(q)
        )
        quest_controls.append(cb)

    quests_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("📜 Daily Quests", size=16, weight=ft.FontWeight.BOLD, color="#00D2FF"),
                *quest_controls
            ]
        ),
        padding=15,
        border_radius=15,
        bgcolor="#16161E",
    )

    # ------------------- إضافة العناصر للصفحة -------------------
    page.add(
        logo_card,
        profile_card,
        raid_card,
        quests_card
    )

ft.app(target=main)
