import flet as ft
import time
import threading

# استدعاء الإشعارات بشكل آمن لعدم ضرب أخطاء
try:
    from plyer import notification
except ImportError:
    notification = None

def send_samsung_notification(title, message):
    if notification:
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="QuestLog",
                timeout=10
            )
        except Exception:
            pass

def main(page: ft.Page):
    # ------------------- إعدادات الشاشة والموبايل -------------------
    page.title = "QuestLog"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F0F14"
    page.padding = 16
    page.scroll = "adaptive"

    # ------------------- بيانات المستخدم -------------------
    user_data = {"level": 1, "xp": 0, "xp_needed": 100}

    # ------------------- 1. Header & Level Card -------------------
    level_text = ft.Text(f"Level {user_data['level']}", size=15, weight=ft.FontWeight.BOLD, color="#00D2FF")
    xp_text = ft.Text(f"{user_data['xp']}/{user_data['xp_needed']} XP", size=12, color="#8E8E93")
    xp_progress = ft.ProgressBar(value=0, color="#7928CA", bgcolor="#232331", height=8)

    header_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text("QL", weight=ft.FontWeight.BOLD, color="#FFFFFF", size=14),
                                    bgcolor="#7928CA",
                                    padding=8,
                                    border_radius=8
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("QuestLog", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                        ft.Text("Level Up Your Day", size=11, color="#8E8E93")
                                    ],
                                    spacing=0
                                )
                            ],
                            spacing=10
                        ),
                        ft.Column(
                            controls=[level_text, xp_text],
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            spacing=0
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(height=4),
                xp_progress
            ],
            spacing=8
        ),
        padding=14,
        border_radius=14,
        bgcolor="#181820"
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
        xp_text.value = f"{user_data['xp']}/{user_data['xp_needed']} XP"
        xp_progress.value = user_data["xp"] / user_data["xp_needed"]
        page.update()

    # ------------------- 2. Gaming Raid Timer -------------------
    timer_display = ft.Text("00:00", size=36, weight=ft.FontWeight.BOLD, color="#00D2FF")
    
    # تحسين حقل الإدخال ليظهر الكلام بوضوح
    timer_input = ft.TextField(
        label="المنافسة (دقائق)",
        border_color="#7928CA",
        focused_border_color="#00D2FF",
        width=150,
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
        page.update()

        # إرسال إشعار سامسونج والصوت المدمج بالنظام 🔔
        send_samsung_notification(
            title="⚔️ انتهى وقت الـ Raid!",
            message="قوم خد استراحة وريح عينك يا بطل."
        )

        page.snack_bar = ft.SnackBar(
            content=ft.Text("⚔️ انتهى الوقت! قوم خذ استراحة وريح عينك."),
            bgcolor="#00D2FF"
        )
        page.snack_bar.open = True
        page.update()

    def start_raid(e):
        try:
            mins = float(timer_input.value)
            if mins > 0:
                threading.Thread(target=run_timer, args=(mins,), daemon=True).start()
        except (ValueError, TypeError):
            pass

    raid_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("⏱️ Gaming Raid Timer", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ft.Row(
                    controls=[timer_input, timer_display],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Container(height=5),
                ft.Button(
                    content=ft.Text("START RAID ⚔️", weight=ft.FontWeight.BOLD, color="#FFFFFF", size=14),
                    style=ft.ButtonStyle(
                        bgcolor={"": "#7928CA"},
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    width=400,
                    height=45,
                    on_click=start_raid
                )
            ],
            spacing=10
        ),
        padding=14,
        border_radius=14,
        bgcolor="#181820"
    )

    # ------------------- 3. Daily Quests -------------------
    quests = [
        {"title": "📖 مذاكرة / عمل (60 دقيقة)", "xp": 50},
        {"title": "🏋️ تمرينة الجيم", "xp": 40},
        {"title": "💧 شرب 3 لتر مية", "xp": 20},
        {"title": "😴 نوم مبكر قبل 12", "xp": 30},
    ]

    quest_controls = []
    for q in quests:
        def make_handler(quest_data):
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
            on_change=make_handler(q)
        )
        quest_controls.append(cb)

    quests_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("📜 Daily Quests", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                *quest_controls
            ],
            spacing=6
        ),
        padding=14,
        border_radius=14,
        bgcolor="#181820"
    )

    # ------------------- إضافة كل الكروت للواجهة -------------------
    page.add(
        header_card,
        raid_card,
        quests_card
    )

ft.app(target=main)
