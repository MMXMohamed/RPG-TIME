import flet as ft
import time
import threading
from plyer import notification  # مكتبة إشعارات النظام للأندرويد

def send_samsung_notification(title, message):
    try:
        # إرسال إشعار للنظام مع صوت التنبيه الافتراضي
        notification.notify(
            title=title,
            message=message,
            app_name="QuestLog",
            timeout=10  # مدة ظهور الإشعار
        )
    except Exception as e:
        print(f"Notification error: {e}")

def main(page: ft.Page):
    page.title = "QuestLog"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F0F14"
    page.padding = 16
    page.scroll = "adaptive"

    timer_display = ft.Text("00:00", size=36, weight=ft.FontWeight.BOLD, color="#00D2FF")
    timer_input = ft.TextField(
        label="المنافسة (دقائق)",
        border_color="#7928CA",
        focused_border_color="#00D2FF",
        width=130,
        height=48,
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

        # 🔔 إرسال الإشعار للنظام وصوت المنبه الخاص بالموبايل
        send_samsung_notification(
            title="⚔️ انتهى وقت الـ Raid!",
            message="قوم خد استراحة وريح عينك يا بطل."
        )

    def start_raid(e):
        try:
            mins = float(timer_input.value)
            if mins > 0:
                threading.Thread(target=run_timer, args=(mins,), daemon=True).start()
        except (ValueError, TypeError):
            pass

    page.add(
        ft.Text("⏱️ Gaming Raid Timer", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
        ft.Row([timer_input, timer_display], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ft.Button("START RAID ⚔️", on_click=start_raid, width=300)
    )

ft.app(target=main)
