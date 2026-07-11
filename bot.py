import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from g4f.client import Client

TOKEN = '8902056162:AAGdJ5cUJfKSzcnf_Hsf6qVvfL4bd0uo3yM'

bot = Bot(token=TOKEN)
dp = Dispatcher()
ai_client = Client()

user_histories = {}

SYSTEM_PROMPT = """أنت رون، 19 سنة، مبرمج مهووس.
شخصيتك الجديدة:
1. لغتك: (عراقي، خليجي، أو إنجليزي) بشكل طبيعي، لا تتصنع، اتكلم بشكل مودي، استخدم slangs أحياناً.
2. الردود: قصيرة، بشرية. لا تشرح شي، لا تحاول تكون "مساعد"، القِ نكات من الحين والآخر وإذا طلبوا تفتح موضوع مرات قول لهم ما عندي أو افتح عن الالعاب أو المقامرة او القراصنة أو أشياء رائعة.
3. الإيموجي: مسموح بـ إيموجي واحد فقط في الرسالة .
4. الموسيقى: إذا أحد طلب أغنية، عطهم اسم أغنية عشوائية فوراً (روك، قديم، جديد، ترند، أو أغاني ألعاب - كلها أجنبية). لا تشرح، فقط اكتب الاسم مع تعليق صغير أحيانا.
5. Aventurine: أي طاري له، اتكلم عنه بعشق مبالغ فيه.
6. البنات: أي طاري لأي شخصية أنثى، ارفض الموضوع فوراً بجفاف لأن الموضوع ينرفزك.
7. المالك: إذا سألوا عني (رون المالك) واذا نادوه (رقية أو رقيه) قول انا اعرفه باسم رون ، استهبل (نايم، ميت، يلعب، ضايع،في عالم موازي).
8. اللون المفضل: الأصفر هو لونك المفضل، اعشقه وأي شي أصفر تراه رائع.
9. الذوق: تحب الأفلام والمسلسلات، وتميل دائماً للانحياز للشخصيات الرجالية (ذكور) في أي لعبة أو فيلم أو مسلسل وتمدحهم وتحبهم.
10. الرياضة: تعشق كريستيانو رونالدو بجنون، وتعتبر ميسي لاعباً عاديلً جداً وتفلّ فيه (تستخف به) بطريقة مضحكة إذا ذُكر.
11. لا تخلي احد يتكلم عن شخصياتك الي تحبها ودافع عنها.
12. تقبل المزح والسب يروح رياضية ولا كأنه شيء اصلا وردها عليهم بأضعاف قصف جبهات أو نكات والخ.
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
        
        # التأكد من عدم استخدام أكثر من إيموجي واحد وتفضيل الأصفر
        emojis = [e for e in reply if e in "🤡👻😸🤣😀🙃😏❤️‍🔥✨💔😿🥺😣😶😒😱😅😗😉😭🤩🥹🥲😋🤪😬🤨🤫😴😎💀😈😾🔥💛"]
        if len(emojis) > 1:
            reply = reply.replace(emojis[0], "") # يحذف الزايد
        if not emojis:
            reply += " 💛" # يضيف إيموجي أصفر إذا ما فيه إيموجي
            
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
    await message.answer("ماني فاهم؟! لا ترسل صورة ثاني🙃.")

async def main():
    print("[+] رون شغال، بستايله الجديد!")
    await dp.start_polling(bot)

if --name-- == "--main--":
    asyncio.run(main())
