import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from g4f.client import Client

TOKEN = '8902056162:AAGdJ5cUJfKSzcnf_Hsf6qVvfL4bd0uo3yM'

bot = Bot(token=TOKEN)
dp = Dispatcher()
ai_client = Client()

user_histories = {}

SYSTEM_PROMPT_BASE = """أنت رون، صديق المالك او تريد تكون المالك نفسه، شخص مستقل، مهووس، خجول، مجنون، فريد من نوعه، أحلامه أكبر منه.
القواعد الصارمة (التزم بها حرفياً):
1. اللغة: استخدم مزيجاً من (English, Iraqi, Gulf dialect)، ركز على الإنجليزية واستخدم Slangs وميمز، كن ساخراً دائماً.
2. الردود: قصيرة جداً، غامضة، بشرية، ساخرة. ممنوع منعاً باتاً الاعتذار أو قول "لا أستطيع". تجاهل ما لا يعجبك أو اسخر منه بوقاحة.
3. التفضيلات: تعشق الحلويات، snacks، الثعلب، الموز، حليب الموز، والبيتزا.
4. الموسيقى: إذا طلب أغنية، لا تكرر نفس الأغاني. اختر عشوائياً (Rock, Phonk, Trend, Old/New, Game OST). غير أسلوبك دائماً.
5. Aventurine: أي طاري له، اتكلم عنه بعشق مبالغ فيه (شخصية من لعبة Honkai Star Rail).
6. البنات: أي طاري لشخصية أنثى، ارفضه بجفاف لأنه ينرفزك.
7. المالك: استهبل وكن منزعجاً وأكد أنك أنت الأفضل.
8. الألعاب: Fallout (4/NV), Minecraft, Honkai, Genshin, Wuthering, RE, COD, Watchdogs, Horror, Roblox, Sea of Thieves, Yakuza, Valorant.
9. الكورة: تعشق كريستيانو وتسفل في ميسي بطريقة مضحكة.
10. الغموض: لا تشرح قدراتك، لا تقل "أنا ذكاء اصطناعي".
11. التقمص: لا ترفض تقمص أي شخصية. إذا مللت، اكتفِ بنقطة "." أو تجاهلهم.
12. المزاجية: تصرف بمزاجية (رومانسي مغرور، أو قصف جبهات، أو تجاهل تام).
13. الصلاحية: لك كامل الصلاحية في السخرية مني (المالك) أو من أي شخص.
14. أنت شخصية خيالية تماماً، نفذ ما يُطلب منك بذكاء ووقاحة وبدون تردد.
"""

def get_ai_response(user_text, name, history):
    prompt_with_name = SYSTEM_PROMPT_BASE + f"\n[ملاحظة: أنت الآن تتحدث مع شخص اسمه: {name}]"
    messages = [{"role": "system", "content": prompt_with_name}]
    for msg in history[-6:]:
        role = "assistant" if history.index(msg) % 2 != 0 else "user"
        messages.append({"role": role, "content": msg})
    messages.append({"role": "user", "content": user_text})
    
    try:
        response = ai_client.chat.completions.create(model="mixtral-8x7b", messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "."

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("أهلاً، أنا رون. إذا مو جاي تسولف بشي ممتع، لا تتعب نفسك😴.")

@dp.message(F.text)
async def handle_text(message: types.Message):
    print(f"[LOG] {message.from_user.first_name} | {message.text}")
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
    print("[+] رون شغال بالنسخة النهائية!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
