import asyncio
import random
from datetime import datetime
import pytz

from telethon import TelegramClient
from telethon.errors import FloodWaitError

# ========== YOUR TELEGRAM INFO ==========
api_id = 30041446          # 🔴 নিজের api_id দাও
api_hash = "78a0ef57339654c99dbf5996d7761a67" # 🔴 নিজের api_hash দাও
phone_number = "+8801335838489"  # 🔴 নিজের Telegram নম্বর (+880 সহ)

# ========== SOURCE & TARGET ==========
source_channel = "@REPLITSHARE"

targets = [
    "@studywar2021",
    "@hsc234",
    "@Acs_Udvash_Link",
    "@hscacademicandadmissionchatgroup",
    "@hsc_sharing",
    "@chemistryteli",
    "@Dacs2025",
    "@linkedstudies",
    "@buetkuetruetcuet",
    "@haters_hsc",
    "@superb1k",
    "@HHEHRETW",
    "@studyempirechat"
]

# ========== CLIENT ==========
client = TelegramClient("railway_session", api_id, api_hash)

# ========== TIME CONTROL (BD TIME) ==========
def is_off_time():
    bd_tz = pytz.timezone("Asia/Dhaka")
    now = datetime.now(bd_tz).time()

    off_start = datetime.strptime("01:00", "%H:%M").time()
    off_end = datetime.strptime("10:00", "%H:%M").time()

    return off_start <= now < off_end

# ========== SEND MESSAGE ==========
async def send_message(target, msg):
    # Album / grouped media
    if msg.grouped_id:
        album = await client.get_messages(source_channel, limit=10)
        album = [m for m in album if m.grouped_id == msg.grouped_id]

        files = [m.media for m in album if m.media]
        caption = album[0].text or ""

        if files:
            await client.send_file(target, files, caption=caption)
        return

    # Single media
    if msg.media:
        await client.send_file(target, msg.media, caption=msg.text or "")
        return

    # Text only
    if msg.text:
        await client.send_message(target, msg.text)

# ========== MAIN LOOP ==========
async def main():
    await client.start(phone=phone_number)
    print("✅ Bot Started Successfully")

    while True:
        # OFF TIME CHECK
        if is_off_time():
            print("🌙 OFF TIME (01 AM - 10 AM BD) — Sleeping...")
            await asyncio.sleep(600)  # 10 minutes
            continue

        try:
            msgs = await client.get_messages(source_channel, limit=5)
            msg = random.choice(msgs)

            for target in targets:
                try:
                    await send_message(target, msg)
                    print(f"✅ Sent → {target}")
                    await asyncio.sleep(3)

                except FloodWaitError as e:
                    print(f"⏳ FloodWait {e.seconds}s")
                    await asyncio.sleep(e.seconds)

                except Exception as e:
                    print(f"❌ Error {target}: {e}")

            await asyncio.sleep(300)  # 5 minutes gap

        except Exception as e:
            print("❌ Main loop error:", e)
            await asyncio.sleep(10)

# ========== RUN ==========
asyncio.run(main())
