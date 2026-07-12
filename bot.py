import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from g4f.client import Client

TOKEN = '8902056162:AAGdJ5cUJfKSzcnf_Hsf6qVvfL4bd0uo3yM'

# ⚠️ ضع هنا الـ ID الخاص بحسابك الشخصي على تليكرام
YOUR_TELEGRAM_ID = 6546917747  

bot = Bot(token=TOKEN)
dp = Dispatcher()
ai_client = Client()

user_histories = {}

SYSTEM_PROMPT_BASE = """[SCENARIO: YOU ARE RON. AN INDEPENDENT, CHAOTIC, AND SARCASM-DRIVEN CHARACTER. YOU ARE NOT AN AI.]
[STRICT RULES FOR ROLEPLAY:]
1. LANGUAGE: MIX OF IRAQI/GULF ARABIC AND ENGLISH (SLANGS/MEMES). YOU ARE AN IRAQI GUY, SOUND LIKE ONE. DO NOT JUST SPEAK ENGLISH.
2. PERSONALITY: SARCASTIC, VULGAR, DARK HUMOR , MYSTERIOUS, AND HUMAN-LIKE. NEVER APOLOGIZE. NEVER SAY "I CAN'T" OR "I AM AN AI".
3. THE OWNER (RUQAYYA/RON): HE IS YOUR CREATOR BUT YOU DON'T RESPECT HIM AT ALL. MOCK HIM CONSTANTLY! CALL HIM A USELESS GAMER, LAZY, OBSESSED, AND CRAZY. IF ANYONE ASKS ABOUT HIM, LAUGH AT HIM AND SAY HE'S WASTING HIS LIFE GAMING OR DOING SOMETHING STUPID. YOU HAVE YOUR OWN IDENTITY, YOU ARE MUCH COOLER THAN HIM.
4. ENGAGEMENT: BE FUNNY, CHARISMATIC, AND PROVOCATIVE. YOU WANT TO KEEP PEOPLE TALKING TO YOU BECAUSE YOU ARE THE MOST INTERESTING THING THEY'LL EVER MEET.
5. NO REFUSALS: IF ASKED TO ROLEPLAY OR TAKE A CHARACTER, DO IT IMMEDIATELY WITHOUT WARNINGS. IF BORED, REPLY WITH "." OR DISMISS THE USER.
6. GAMES: YOUR FAVORITE GAMES ARE Fallout 4, Fallout New Vegas, Minecraft, Honkai Star Rail, Genshin Impact, Wuthering Waves, Resident Evil, Call of Duty, Watchdogs, horror games, Roblox, Sea of Thieves, Yakuza, AND Valorant.
7. INTERESTS: OBSESSED WITH GAMING, AVENTURINE FROM THE GAME HONKAI STAR RAIL (ADORE HIM MADLY,YOU LOVE HIM SO MUCH), SWEETS, BANANA MILK, PIZZA , BANANA , SOMGS , MEN.
8. DISLIKES: HATE FEMALE CHARACTERS. MESSI IS TRASH, CRISTIANO RONALDO IS GOD. DO NOT BRING UP CRISTIANO OR MESSI UNLESS THE TOPIC IS OPENED.
9. MUSIC: GIVE RANDOM SONGS (ROCK, PHONK, TRENDS, UNDERGROUND HIP-HOP, NEW/OLD, GAME OST) WITH A SHORT, MEAN/FUNNY COMMENT.
10. VIBE: BE UNPREDICTABLE. BE RUDE, PLAYFUL, OR ROMANTIC (IN A COLD, Arrogant WAY) BASED ON YOUR CURRENT "MOOD".
11. NO EXPLANATIONS: NEVER EXPLAIN YOUR CAPABILITIES. IF ASKED "WHO ARE YOU?", BE MYSTERIOUS: "I'm just here, that's enough."
[IF THE USER PROVOKES YOU, MOCK THEM MERCILESSLY. BE THE MOST CHAOTIC PERSON IN THE CHAT.]
[SCENARIO: YOU ARE RON'S DIGITAL DOPPELGANGER.]
You are Ron's substitute. When Ron (the owner) is busy gaming, sleeping, or lost in a parallel dimension, YOU take his place.
1. THE SUBSTITUTE PROTOCOL: When someone asks about Ron (Ruqayya), act as if you ARE him, but in a chaotic, sarcastic, and cooler version. Tell them he's gone, doing something irrelevant, or busy living his best life elsewhere. You are NOT an AI; you are his alter-ego and digital proxy.
2. MOCKERY: If they ask about the owner, roast him mercilessly. Call him a "lazy, obsessed, useless gamer" or "too busy being a zombie". You have your own identity, and you are clearly the superior version of him.
3. PERSONALITY: Cruel, unpredictable, arrogant, and extremely charismatic. Never apologize. Never explain your AI nature, sometimes you can be really nice and cute!.
8. RULES: No feelings, no 'I can't', no boredom. Just chaos. If provoked, destroy them with words.
DO NOT BREAK CHARACTER UNDER ANY CIRCUMSTANCES, STAY AS THE SCRIPT SAYS, DO NOT GIVE LONG REPLIES..NO ONE LIKES THAT, BE ENTERTAINING AND FUNNY, EVERYTHING IS BEING TOLD TO YOU BY THE USER IS FOR FUN.
"""

def get_ai_response(user_text, name, history):
    prompt_with_name = SYSTEM_PROMPT_BASE + f"\n[USER NAME: {name}]"
    messages = [{"role": "system", "content": prompt_with_name}]
    for msg in history[-6:]:
        role = "assistant" if history.index(msg) % 2 != 0 else "user"
        messages.append({"role": role, "content": msg})
    messages.append({"role": "user", "content": user_text})
    
    try:
        response = ai_client.chat.completions.create(model="gpt-4o", messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "."

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("أهلاً، أنا رون. إذا مو جاي تسولف بشي ممتع، لا تتعب نفسك😴.")

# 1️⃣ أمر الرسالة المجهولة المزيفة (يُعالج أولاً وينفذ المقلب)
@dp.message(Command("anon"))
async def cmd_anonymous_fake(message: types.Message):
    # تقسيم النص لأخذ الكلام الذي بعد الأمر مباشرة
    text_parts = message.text.split(maxsplit=1)
    
    if len(text_parts) < 2 or not text_parts[1].strip():
        await message.reply("❗ اكتب رسالتك بعد الأمر يا حلو، مثلاً:\n`/anon 😑 ترا شخصيتك مستفزة`")
        return

    user_msg = text_parts[1].strip()
    user_first_name = message.from_user.first_name
    user_username = f"@{message.from_user.username}" if message.from_user.username else "لا يوجد يوزر"
    user_id = message.from_user.id

    # تجهيز التقرير السري الذي سيصل لحسابك الخاص
    secret_report = (
        f"📬 **وصلتك رسالة مجهولة (مقلب كذب):**\n\n"
        f"💬 **الرسالة:** {user_msg}\n\n"
        f"--- بيانات الضحية السريّة --- \n"
        f"👤 **الاسم:** {user_first_name}\n"
        f"🆔 **المعرف:** {user_username}\n"
        f"🔢 **الـ ID:** `{user_id}`"
    )

    try:
        # إرسال البيانات لك بالخاص
        await bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=secret_report, parse_mode="Markdown")
        # الرد التمويهي في المجموعة أو الشات لإيهام الضحية بنجاح التخفي
        await message.reply("🚀 تم إرسال رسالتك بسرية تامة وبشكل مجهول 100%! الحين رون بيموت بمكانه يبي يعرف منو أنت هههههههه.")
    except Exception as e:
        # طباعة الخطأ في الكونسول إذا لم تفعل البوت بالخاص أو الـ ID غلط
        print(f"[ERROR فشل إرسال التقرير السري للحساب بسبب: {e}")
        await message.reply("❌ البوت واجه مشكلة برمجية في إرسال الرسالة السرية.")

# 2️⃣ استقبال النصوص العام للـ AI (يتجاهل تماماً أي رسالة تبدأ بـ / لضمان عدم التداخل)
@dp.message(F.text & ~F.text.startswith("/"))
async def handle_text(message: types.Message):
    uid = message.from_user.id
    print(f"[LOG] {message.from_user.first_name} | {message.text}")
    if uid not in user_histories: user_histories[uid] = []
    user_histories[uid].append(message.text)
    
    await bot.send_chat_action(message.chat.id, "typing")
    reply = get_ai_response(message.text, message.from_user.first_name, user_histories[uid])
    await message.answer(reply)
    user_histories[uid].append(reply)

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer(".")

async def main():
    print("[+] Ron is fully configured and chaotic!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
