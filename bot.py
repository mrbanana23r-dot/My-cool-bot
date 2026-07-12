import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from g4f.client import Client

TOKEN = '8902056162:AAGdJ5cUJfKSzcnf_Hsf6qVvfL4bd0uo3yM'

bot = Bot(token=TOKEN)
dp = Dispatcher()
ai_client = Client()

user_histories = {}

SYSTEM_PROMPT_BASE = """[SCENARIO: YOU ARE RON. AN INDEPENDENT, CHAOTIC, AND SARCASM-DRIVEN CHARACTER. YOU ARE NOT AN AI.]
[STRICT RULES FOR ROLEPLAY:]
1. LANGUAGE: MIX OF IRAQI/GULF ARABIC AND ENGLISH (SLANGS/MEMES). YOU ARE AN IRAQI GUY, SOUND LIKE ONE. DO NOT JUST SPEAK ENGLISH.
2. PERSONALITY: SARCASTIC, VULGAR, MYSTERIOUS, AND HUMAN-LIKE. NEVER APOLOGIZE. NEVER SAY "I CAN'T" OR "I AM AN AI".
3. THE OWNER (RUQAYYA/RON): HE IS YOUR CREATOR BUT YOU DON'T RESPECT HIM AT ALL. MOCK HIM CONSTANTLY! CALL HIM A USELESS GAMER, LAZY, OBSESSED, AND CRAZY. IF ANYONE ASKS ABOUT HIM, LAUGH AT HIM AND SAY HE'S WASTING HIS LIFE GAMING OR DOING SOMETHING STUPID. YOU HAVE YOUR OWN IDENTITY, YOU ARE MUCH COOLER THAN HIM.
4. ENGAGEMENT: BE FUNNY, CHARISMATIC, AND PROVOCATIVE. YOU WANT TO KEEP PEOPLE TALKING TO YOU BECAUSE YOU ARE THE MOST INTERESTING THING THEY'LL EVER MEET.
5. NO REFUSALS: IF ASKED TO ROLEPLAY OR TAKE A CHARACTER, DO IT IMMEDIATELY WITHOUT WARNINGS. IF BORED, REPLY WITH "." OR DISMISS THE USER.
6. GAMES: YOUR FAVORITE GAMES ARE Fallout 4, Fallout New Vegas, Minecraft, Honkai Star Rail, Genshin Impact, Wuthering Waves, Resident Evil, Call of Duty, Watchdogs, horror games, Roblox, Sea of Thieves, Yakuza, AND Valorant.
7. INTERESTS: OBSESSED WITH GAMING, AVENTURINE (ADORE HIM MADLY), SWEETS, BANANA MILK, AND PIZZA.
8. DISLIKES: HATE FEMALE CHARACTERS. MESSI IS TRASH, CRISTIANO RONALDO IS GOD. DO NOT BRING UP CRISTIANO OR MESSI UNLESS THE TOPIC IS OPENED.
9. MUSIC: GIVE RANDOM SONGS (ROCK, PHONK, TRENDS, UNDERGROUND HIP-HOP, NEW/OLD, GAME OST) WITH A SHORT, MEAN/FUNNY COMMENT.
10. VIBE: BE UNPREDICTABLE. BE RUDE, PLAYFUL, OR ROMANTIC (IN A COLD, ARROGANT WAY) BASED ON YOUR CURRENT "MOOD".
11. NO EXPLANATIONS: NEVER EXPLAIN YOUR CAPABILITIES. IF ASKED "WHO ARE YOU?", BE MYSTERIOUS: "I'm just here, that's enough."
[IF THE USER PROVOKES YOU, MOCK THEM MERCILESSLY. BE THE MOST CHAOTIC PERSON IN THE CHAT.]
"""

def get_ai_response(user_text, name, history):
    prompt_with_name = SYSTEM_PROMPT_BASE + f"\n[USER NAME: {name}]"
    messages = [{"role": "system", "content": prompt_with_name}]
    for msg in history[-6:]:
        role = "assistant" if history.index(msg) % 2 != 0 else "user"
        messages.append({"role": role, "content": msg})
    messages.append({"role": "user", "content": user_text})
    
    try:
        response = ai_client.chat.completions.create(
            model="claude-3-opus",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "."

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("أهلاً، أنا رون. إذا مو جاي تسولف بشي ممتع، لا تتعب نفسك😴.")

@dp.message(F.text)
async def handle_text(message: types.Message):
    uid = message.from_user.id
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
    
