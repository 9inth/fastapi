from telethon import TelegramClient, events
from datetime import datetime, timedelta
import asyncio

# === НАСТРОЙКИ ===
ID_HASH = 32298860
API_HASH = '52da255fff426eb52c0e4a176914f2e4'
phone = '+79017109737'

TARGET_GROUP_ID = -5156583755  # ID целевой группы (отрицательное)
TARGET_USER_ID = 1947162373        # ID целевого пользователя
KEYWORD = 'запис'                 # ключевое слово для ответа
REPLY_TEXT = '1. Антон, ЛИ'  # текст ответа
COOLDOWN_MINUTES = 1               # задержка между ответами (в минутах)

# === ПАМЯТЬ ОТВЕТОВ ===
last_reply = {}

# === КЛИЕНТ ===
client = TelegramClient('session', api_id=ID_HASH, api_hash=API_HASH)

# === ОБРАБОТЧИК ВХОДЯЩИХ ===
@client.on(events.NewMessage(incoming = True))
async  def auto_reply(event):
    try:
        # Проверка группы
        if event.chat_id != TARGET_GROUP_ID:
            print(TARGET_GROUP_ID)
            return

        # Проверка отправителя
        sender = await event.get_sender()
        if sender.id != TARGET_USER_ID:
            print(TARGET_USER_ID)
            return

        # Проверка ключевого слова
        if KEYWORD not in (event.raw_text):
            print(event.raw_text)
            return

        # Проверка, не наше ли сообщение (на всякий случай)
        if event.message.out:
            return

        # Проверка времени последнего ответа
        last = last_reply.get(TARGET_USER_ID)
        if last and (datetime.now() - last) < timedelta(minutes=COOLDOWN_MINUTES):
            return

        # Отправка ответа
        await event.respond(REPLY_TEXT)
        print(f"Автоответ отправлен пользователю {TARGET_USER_ID}")

        # Обновление времени
        last_reply[TARGET_USER_ID] = datetime.now()

    except Exception as e:
        print(f"Ошибка:{e}")

# === ОБРАБОТЧИК ИСХОДЯЩИХ (наши ответы вручную) ===
@client.on(events.NewMessage(outgoing=True))
async def track(event):
    try:
        if event.chat_id != TARGET_GROUP_ID:
            return
        if not event.is_reply:
            return
        replied = await event.get_reply_message()
        if not replied:
            return
        sender = await replied.get_sender()
        if sender.id == TARGET_USER_ID:
            last_reply[TARGET_USER_ID] = datetime.now()
            print(f"Обновлено время (ручной ответ пользователю {TARGET_USER_ID})")
    except Exception:
        pass  # игнорируем ошибки

# === ЗАПУСК ===
async def main():
    await client.start(phone)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())