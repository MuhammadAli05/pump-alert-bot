# 🚀 Pump Alert Bot

Бот отслеживает возможные пампы токенов через DexScreener и присылает уведомления в Telegram.

## 🧠 Локальный запуск

1. Установи зависимости:
pip install -r requirements.txt
2. Запусти:
TELEGRAM_TOKEN=... CHAT_ID=... python bot.py

## ☁️ Деплой на Render

1. Залей проект в GitHub (назови репозиторий `pump-alert-bot`)
2. Перейди в Render → New Web Service → выбери репозиторий
3. Render автоматически подхватит `.render.yaml`
4. Укажи переменные:
- `TELEGRAM_TOKEN`: токен от BotFather
- `CHAT_ID`: ID чата (можно узнать через @userinfobot)
5. Жди запуска — бот пойдёт в работу

---

## ⚙️ Настройка фильтров

Изменяй пороги `price_change`, `vol_ratio` и `market_cap` в функции `is_pump()`.

---

🎉 Бот запущен — теперь каждый 10 минут он монитоит токены и шлёт сигналы в твой Telegram.
