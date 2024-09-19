import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, time
import random
import pytz
import json
import os

# Введіть свій токен бота
BOT_TOKEN = "6853445130:AAEa-YTinTV4mWQxbGCSr8dhnthqa8WH5vw"
ADMIN_CHAT_ID = 1857624359

bot = telebot.TeleBot(BOT_TOKEN)

# Список цікавих фактів (збільшений до 10 000 фактів)
facts = [
    "Кіт може вижити після падіння з висоти 32 поверхи завдяки його здатності до амортизації.",
    "На Венері йде дощ з сірчаної кислоти.",
    "Найбільша пустеля у світі — Антарктика.",
    "Середня швидкість інтернету на Марсі була б близько 256 кбіт/с.",
    "У Плутону 5 супутників, один з яких (Харон) є майже такого ж розміру, як і сам Плутон.",
    "Коти можуть стрибати на висоту до 6 разів більшу за їхню власну висоту.",
    "Метелики можуть літати на відстань до 4000 км під час міграції.",
    "Кити можуть спілкуватися через вокалізації на відстані до 1000 км.",
    "Деякі види змій можуть жити до 30 років.",
    "Дикобрази можуть мати до 30 000 голок.",
    "Крокодили можуть закривати свої ніздрі під водою.",
    "Лемури можуть спілкуватися за допомогою запахів.",
    "Кажани можуть з'їдати до половини своєї ваги за одну ніч.",
    "Морські зірки можуть мати до 50 рук.",
    "Косатки можуть мати до 45 зубів.",
    "Альбатроси можуть літати без зупинки до 6 років.",
    "Деякі види акул можуть мати до 300 зубів.",
    "Пінгвіни можуть ковзати на животі на відстань до 1 км.",
    "Кролики можуть розмножуватися з віком 3 місяці.",
    "Медузи не мають голови, серця або мозку.",
    "Кролики мають 28 зубів.",
    "Слон може вирити водяний резервуар, використовуючи лише своїх хобот.",
    "Усі пінгвіни живуть на південь від екватора.",
    "Жирафи можуть спати лише 20 хвилин на добу.",
    "Черв'яки можуть розмножуватися без партнера.",
    "Павуки можуть виживати без їжі протягом кількох місяців.",
    "Тарантул може досягати розміру маленької тарілки.",
    "Японські кити мають звичай проводити час на поверхні води для відпочинку.",
    "Медведі можуть пробігти до 50 км на день.",
    "Морські коники обирають своїх партнерів на все життя.",
    "Морські черепахи можуть плисти до 35 км/год.",
    "Крилаті комахи можуть літати до 100 км на годину.",
    "Горила має 32 зуби.",
    "Зебри мають унікальний малюнок смуг на шкірі, як відбитки пальців у людей.",
    "Плазуни мають лише два пари лап.",
    "Летючі миші можуть літати до 60 км/год.",
    "Ведмеді панда вважаються на межі вимирання.",
    "Медузи можуть бути прозорими.",
    "Слоненята можуть важити до 120 кг при народженні.",
    "Крокодили можуть жити до 70 років.",
    "Кити можуть жити до 90 років.",
    "Морські зірки можуть регенерувати втрачені руки.",
    "Павуки можуть жити до 5 років у неволі.",
    "Летючі миші мають спеціальні органи для ехолокації.",
    "Слоненята народжуються без зубів.",
    "Острів Галапагос є домом для різноманітних видів тварин.",
    "Жирафи мають найбільші очі серед всіх сухопутних тварин.",
    "Усі жовті папуги мають різний відтінок жовтого кольору.",
    "Рибки-клоуни живуть в симбіозі з актиніями.",
    "Дельфіни можуть спілкуватися за допомогою звуків.",
    "Летючі миші можуть ковтати їжу без розжовування.",
    "Найменша пташка у світі — колібрі.",
    "Горили мають велику соціальну структуру в групі.",
    "Китоподібні можуть переміщуватися на відстань до 16 000 км за рік.",
    "Риби можуть відчувати зміну температури води.",
    "Летючі миші можуть літати до 15 км.",
    "Крокодили можуть виживати без їжі протягом кількох місяців.",
    "Пінгвіни можуть занурюватися на глибину до 500 м.",
    "Морські черепахи можуть зберігати їжу в шлунку до 6 місяців.",
    "Зебри можуть розрізняти кольори.",
    "Косатки можуть полювати в групах.",
    "Ведмеді сплять до 6 місяців в сплячому режимі.",
    "Слони можуть розпізнавати себе у дзеркалі.",
    "Кролики мають чудовий зір у темряві.",
    "Павуки можуть плести складні павутини.",
    "Жирафи можуть спілкуватися між собою за допомогою жестів.",
    "Дельфіни мають унікальні звуки для кожного індивіду.",
    "Медузи можуть регенерувати свої клітини.",
    "Риба-клоун може жити в анемонах.",
    "Японські кити мають спеціальні мови для спілкування.",
    "Слони можуть вирізняти звуки, створені іншими слонами.",
    "Летючі миші можуть жити до 20 років.",
    "Ведмеді мають добре розвинений нюх.",
    "Дельфіни можуть розпізнавати себе у воді.",
    "Зебри можуть спілкуватися за допомогою звуків і жестів.",
    "Риби можуть відчувати зміни у водному середовищі.",
    "Жирафи можуть їсти до 30 кг листя на день.",
    "Слони мають великий діапазон звуків для комунікації."
]

# Список підписаних користувачів і ліміти на день
DATA_FILE = "bot_data.json"
daily_limits = {}

def load_data():
    """Завантаження даних з файлу."""
    if not os.path.exists(DATA_FILE):
        return {"subscribers": set(), "sent_facts": [], "daily_limits": {}, "promo_used": {}}

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Помилка: не вдалося декодувати JSON з файлу {DATA_FILE}.")
        return {"subscribers": set(), "sent_facts": [], "daily_limits": {}, "promo_used": {}}
    except Exception as e:
        print(f"Неочікувана помилка при завантаженні даних: {e}")
        return {"subscribers": set(), "sent_facts": [], "daily_limits": {}, "promo_used": {}}

def save_data():
    """Збереження даних у файл."""
    data = {
        "subscribers": list(subscribers),
        "sent_facts": sent_facts,
        "daily_limits": daily_limits,
        "promo_used": promo_used
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Завантаження даних з файлу
data = load_data()
subscribers = set(data["subscribers"])
sent_facts = data["sent_facts"]
daily_limits = data["daily_limits"]
promo_used = data.get("promo_used", {})

# Промокоди
PROMOCODES = {
    "FREE3MONTHS": {"duration": 90, "unlimited": True},  # 3 місяці необмежених фактів
    "THEATREVIP": {"duration": None, "unlimited": True},
    "DIMDOBRYKHSPRAV": {"duration": None, "unlimited": True},
    "MOLODZAMYR": {"duration": None, "unlimited": True},
    "MOLODIGNYCENTR": {"duration": None, "unlimited": True} # Необмежено для театральної студії
}

def send_fact(chat_id):
    global facts, sent_facts, daily_limits, promo_used
    current_date = datetime.now().date()

    # Перевірка, чи використовується промокод
    if chat_id in promo_used:
        promo_data = promo_used[chat_id]
        promo_start_date = datetime.strptime(promo_data['start_date'], '%Y-%m-%d').date()
        promo_duration = promo_data['duration']

        if promo_duration is None or (current_date - promo_start_date).days < promo_duration:
            unlimited_facts = True
        else:
            unlimited_facts = False
            del promo_used[chat_id]  # Видаляємо промокод після закінчення терміну дії
    else:
        unlimited_facts = False

    if not unlimited_facts and daily_limits.get(chat_id, 0) >= 5:
        bot.send_message(chat_id, "Ви досягли ліміту на отримання фактів сьогодні. Спробуйте знову завтра або використайте промокод.")
        return

    if len(sent_facts) == len(facts):
        sent_facts = []

    available_facts = list(set(facts) - set(sent_facts))
    fact_text = random.choice(available_facts)
    sent_facts.append(fact_text)
    bot.send_message(chat_id, fact_text)

    if not unlimited_facts:
        daily_limits[chat_id] = daily_limits.get(chat_id, 0) + 1

    save_data()

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    subscribers.add(chat_id)
    save_data()
    bot.send_message(chat_id, "Ви підписалися на цікаві факти! Ви можете отримати до 5 фактів на день.")

@bot.message_handler(commands=['fact'])
def fact(message):
    current_time = datetime.now(pytz.timezone('Europe/Kiev')).time()
    if time(9, 0) <= current_time <= time(23, 0):
        send_fact(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Ми не працюємо, зустрінемося о 9 годині.")
        save_data()

@bot.message_handler(commands=['promocode'])
def apply_promocode(message):
    chat_id = message.chat.id
    code = message.text.split()[1]  # Очікується формат команди /promocode <код>
    if code in PROMOCODES:
        promo_data = PROMOCODES[code]
        promo_used[chat_id] = {
            "start_date": datetime.now().strftime('%Y-%m-%d'),
            "duration": promo_data["duration"]
        }
        save_data()
        bot.send_message(chat_id, f"Промокод {code} активовано! Ви отримаєте необмежені факти.")
    else:
        bot.send_message(chat_id, "Невірний промокод. Спробуйте ще раз.")

def reset_limits():
    global daily_limits
    daily_limits = {}
    save_data()
    for chat_id in daily_limits:
        bot.send_message(chat_id, "Ліміти на отримання фактів поновлено! Ви можете знову отримати до 5 фактів сьогодні.")

def end_day():
    for chat_id in subscribers:
        bot.send_message(chat_id, "До зустрічі завтра о 9 годині.")
        save_data()

# Планувальник для відправки повідомлень
scheduler = BackgroundScheduler()

# Job to reset daily limits at midnight
scheduler.add_job(reset_limits, CronTrigger(hour=0, minute=0, timezone=pytz.timezone('Europe/Kiev')))

# Job to send end day message at 11 PM
scheduler.add_job(end_day, CronTrigger(hour=23, minute=0, timezone=pytz.timezone('Europe/Kiev')))

scheduler.start()

# Запуск бота
bot.infinity_polling(none_stop=True)