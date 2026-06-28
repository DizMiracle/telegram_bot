import os
import json
import requests

def handler(event, context):
    """
    Точка входа для Yandex Cloud Functions.
    Telegram будет присылать сюда обновления (Webhook).
    """
    try:
        # 1. Получаем тело запроса от Telegram
        body = json.loads(event['body'])
    except (json.JSONDecodeError, KeyError):
        # Если это не JSON от Telegram, просто игнорируем
        return {
            'statusCode': 200,
            'body': 'OK'
        }

    # 2. Извлекаем данные о сообщении
    message = body.get('message')
    if not message:
        # Если это не сообщение (например, callback), тоже игнорируем
        return {
            'statusCode': 200,
            'body': 'OK'
        }

    chat_id = message.get('chat', {}).get('id')
    text = message.get('text', '')

    # 3. Ваша бизнес-логика (вместо "Hello, Username!")
    if chat_id:
        # Пример ответа. Здесь будет ваш код для работы с Яндекс.Транспортом
        if text == '/start':
            reply = "Привет! Я бот для расписания транспорта."
        elif text == '/help':
            reply = "Напишите мне название остановки, и я скажу, когда придет транспорт."
        else:
            # Здесь будет запрос к Яндекс.Транспорту
            reply = f"Вы написали: '{text}'. Я пока учусь, но скоро заработаю!"

        # 4. Отправляем ответ обратно в Telegram
        send_telegram_message(chat_id, reply)

    # 5. Обязательно возвращаем успешный ответ для Telegram
    return {
        'statusCode': 200,
        'body': 'OK'
    }

def send_telegram_message(chat_id, text):
    """
    Вспомогательная функция для отправки сообщений в Telegram.
    """
    # Токен берется из переменных окружения (БЕЗОПАСНО!)
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("Ошибка: BOT_TOKEN не найден в переменных окружения!")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(url, json={'chat_id': chat_id, 'text': text}, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")