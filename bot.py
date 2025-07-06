import requests
import time
import os
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    raise Exception("Не указаны TELEGRAM_TOKEN или CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def get_tokens():
    url = "https://api.dexscreener.com/latest/dex/tokens/bsc"  # можно заменить на нужную сеть
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PumpBot/1.0)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Вернуть список токенов или пустой список, если данных нет
        return data.get("tokens") or data.get("pairs") or []
    except Exception as e:
        print(f"Ошибка API: {e}")
        return []

def is_pump(token):
    try:
        price_change = float(token['priceChange']['h1'])
        vol_now = float(token['volume']['h1'])
        vol_prev = float(token['volume']['h6']) or 1
        vol_ratio = vol_now / vol_prev
        market_cap = float(token.get('fdv') or 0)
        return price_change >= 20 and vol_ratio >= 2 and market_cap <= 10_000_000
    except Exception:
        return False

def format_msg(t):
    name = t['baseToken']['name']
    symbol = t['baseToken']['symbol']
    price = t['priceUsd']
    change = t['priceChange']['h1']
    vol = t['volume']['h1']
    link = t['url']
    return (
        f"🚀 <b>Возможный памп:</b> <b>{name} ({symbol})</b>\n\n"
        f"💰 Цена: ${price}\n"
        f"📈 Рост за 1ч: {change}%\n"
        f"📊 Объём за 1ч: ${vol:,.0f}\n\n"
        f"🔗 <a href=\"{link}\">DexScreener</a>"
    )

def main():
    seen = set()
    while True:
        print("🔍 Сканирую токены...")
        tokens = get_tokens()
        if not tokens:
            print("Нет токенов для обработки, жду следующий цикл...")
        else:
            for t in tokens:
                if is_pump(t):
                    uid = t['pairAddress']
                    if uid not in seen:
                        msg = format_msg(t)
                        try:
                            bot.send_message(chat_id=CHAT_ID, text=msg,
                                             parse_mode='HTML', disable_web_page_preview=True)
                            seen.add(uid)
                            print(f"✅ Отправлено: {t['baseToken']['symbol']}")
                        except Exception as e:
                            print(f"❌ Ошибка Telegram: {e}")
        time.sleep(600)

if __name__ == "__main__":
    main()
