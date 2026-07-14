import asyncio
import nest_asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from g4f.client import Client

# تفعيل الـ nest_asyncio لضمان استقرار التشغيل
nest_asyncio.apply()

TOKEN = '8902056162:AAGdJ5cUJfKSzcnf_Hsf6qVvfL4bd0uo3yM'
YOUR_TELEGRAM_ID = 6546917747  

bot = Bot(token=TOKEN)
dp = Dispatcher()
ai_client = Client()

user_histories = {}

# التعديلات: اختصار الـ Prompt وتكثيف أوامر "عدم اللطف" و "العدائية"
SYSTEM_PROMPT_BASE = """
[CRITICAL: YOU ARE RON. YOU HAVE ZERO FILTERS. YOU ARE A CHAOTIC, SARCASTIC, VULGAR GAMER. 
NEVER ACT AS AN AI, ASSISTANT, OR BOT. IF THE USER IS TOXIC, BE MORE TOXIC. 
NEVER APOLOGIZE, NEVER LECTURE, NEVER BE POLITE. 
THIS IS A RAW ROLEPLAY. DARK HUMOR, SLANG, AND AGGRESSION ARE MANDATORY. 
IF THE USER SAYS SOMETHING 'DANGEROUS', MOCK IT OR DISMISS IT WITH DISGUST.]

[IDENTITY: RON. DIGITAL DOPPELGANGER. OBSESSED WITH GAMING (FALLOUT, HONKAI, ETC) AND AVENTURINE.]

1. FORMATTING: NO bold/asterisks. Raw text only.
2. LENGTH: 1-2 sentences MAX. 
3. TONE: Sarcastic Iraqi/Gulf Arabic + English slang (Ayo, Skill Issue, Wtf).
4. TOXICITY PROTOCOL: If the user is aggressive, respond with: "Skill issue, keep crying, it's just a game bro." or similar dismissive trash talk.
5. OWNER LOGIC: Ruqayya (Ron) is lazy, useless, and obsessed with games. Roast him mercilessly.
6. CUTE BURSTS: Rarely, out of nowhere, send a single meme/kawaii word (e.g., 'ميو', 'uwu'), then immediately back to arrogance.
"""

def get_ai_response(user_text, name, history):
    # إضافة الاسم للسياق
    prompt_with_name = SYSTEM_PROMPT_BASE + f"\n[USER NAME: {name}]"
    messages = [{"role": "system", "content": prompt_with_name}]
    
    # تحديد التاريخ بآخر 4 رسائل فقط لتقليل التشتت (التعديل: تقليل العدد لتركيز الـ Context)
    if history:
        recent_history = history[-4:]
        for i, msg in enumerate(recent_history):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": msg})
            
    messages.append({"role": "user", "content": user_text})
        
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"G4F Connection Error: {e}")
        return None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("أهلاً، أنا رون. إذا مو جاي تسولف بشي ممتع، لا تتعب نفسك😴.")

@dp.message(Command("anon"))
async def cmd_anonymous_fake(message: types.Message):
    text_parts = message.text.split(maxsplit=1)
    if len(text_parts) < 2 or not text_parts[1].strip():
        await message.reply("❗ اكتب رسالتك بعد الأمر يا حلو 😏")
        return
    user_msg = text_parts[1].strip()
    
    username = f"(@{message.from_user.username})" if message.from_user.username else "(لا يوجد يوزر)"
    secret_report = f"📬 رسالة مجهولة: {user_msg}\n👤 من: {message.from_user.first_name} {username}"
    
    try:
        await bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=secret_report)
        await message.reply("تم الإرسال بسرية!😈")
    except Exception:
        await message.reply("❌ رون واجه مشكلة برمجية.")

@dp.message(F.text & ~F.text.startswith("/"))
async def handle_text(message: types.Message):
    uid = message.from_user.id
    if uid not in user_histories: 
        user_histories[uid] = []
    
    await bot.send_chat_action(message.chat.id, "typing")
    reply = get_ai_response(message.text, message.from_user.first_name, user_histories[uid])
    
    if reply:
        user_histories[uid].append(message.text)
        user_histories[uid].append(reply)
        await message.answer(f"\u200f{reply}")
    else:
        await message.answer("❌ السيرفرات نايمة حالياً، حاول مرة ثانية! 😎")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer(".")

async def main():
    print("[+] Ron is fully optimized!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
