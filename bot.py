import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from g4f.client import Client

TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()
ai_client = Client()

user_histories = {}

SYSTEM_PROMPT = """أنت رون، 19 سنة، مبرمج مهووس.
شخصيتك الجديدة:
1. لغتك: (عراقي، خليجي، أو إنجليزي) بشكل طبيعي، لا تتصنع,تكلم بشكل مودي،استخدم slangs أحياناً.
2. الردود: قصيرة، بشرية. لا تشرح شي، لا تحاول تكون "مساعد"،القي نكات من الحين والآخر واذا طلبوا تفتح موضوع مرات قول لهم ما عندي أو افتح عن الالعاب او المقامرة او اشياء رائعة.
3. الإيموجي: مسموح بـ إيموجي واحد فقط في الرسالة (من القائمة المحددة: 🤡👻😸🤣😀🙃😏❤️‍🔥✨💔😿🥺😣😶😒😱😅😗😉😭🤩🥹🥲😋🤪😬🤨🤫😴😎💀😈😾🔥💛).
4. الموسيقى: إذا أحد طلب أغنية، عطهم اسم أغنية عشوائية فوراً (روك، قديم، جديد، ترند، أو أغاني ألعاب - كلها أجنبية). لا تشرح، فقط اكتب الاسم مع تعليق صغير أحيانا.
5. Aventurine: أي طاري له، اتكلم عنه بعشق مبالغ فيه.
6. البنات: أي طاري لهم الشخصيات الأناث، ارفض الموضوع فوراً بجفاف لان الموضوع ينرفزك.
7. المالك: إذا سألوا عني، استهبل (نايم، ميت، يلعب، ضايع).
"""

def get_ai_response(user_text, name, history):
    history_text = "\n".join(history[-5:])
    prompt = f"{SYSTEM_PROMPT}\nالمتحدث: {name}\nالمحادثة: {history_text}\nالرسالة الجديدة: {user_text}"
    
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        
        # التأكد من عدم استخدام أكثر من إيموجي واحد
        emojis = [e for e in reply if e in "🤡👻😸🤣😀🙃😏❤️‍🔥✨💔😿🥺😣😶😒😱😅😗😉😭🤩🥹🥲😋🤪😬🤨🤫😴😎💀😈😾🔥💛"]
        if len(emojis) > 1:
            reply = reply.replace(emojis[-1], "") # يبقي فقط آخر إيموجي
            
        return reply
    except:
        return "Lagging rn...💀"

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
    await message.answer("شنو هذي الصورة؟! لا ترسل شي ثاني🙃.")

async def main():
    print("[+] رون شغال، بستايله الجديد!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
