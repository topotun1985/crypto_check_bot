hello-user = Привет, { $username }!

subscription-info = 📜 Ваша подписка: { $plan } 

subscription-currencies = 💰 Выбрано валют для отслеживания: { $current }/{ $max }

subscription-expires-infinite = ⏳ Бессрочная подписка

subscription-expires-until = ⏳ Дата окончания подписки: { $expires } (UTC+0)

subscription-purchase-success = ✅ Подписка успешно оформлена! Спасибо за покупку.

welcome-text = 📢 Чтобы получать уведомления, выбери криптовалюту и установи пороговое значение. Бот предупредит тебя, когда цена достигнет нужного уровня! 🚀

select-action = Выбери действие:

subscription-plans = Планы подписки:

plan-basic-description = Базовый — { $limit } валют

plan-standard-description = Стандарт — { $limit } валют

plan-premium-description = Премиум — { $limit } валют

subscription-validity-period = Срок действия подписки: 30 дней

subscription-already-active = ❌ У вас уже есть активная подписка "{ $plan }" до { $expires }. Вы не можете купить новую, пока не истечёт текущая.

subscription-already-active-db = ❌ У вас уже есть активная подписка "{ $plan }" до { $expires }. Вы не можете купить новую, пока не истечёт текущая.

price-star = { $price } ⭐

btn-all-rates = 📊 Все курсы валют

btn-choose-currency = 📈 Выбрать валюту

btn-set-alert = ⏰ Настроить уведомления

btn-subscription = 📜 Подписка

btn-help = ❓ Помощь

btn-basic = 💳 Купить базовый

btn-standard = 💎 Купить стандартный

btn-premium = 👑 Купить премиум

btn-back = ⬅️ Назад



help-text = 👋 Привет! Это раздел помощи.

help-how-to-use = 🔍 Как пользоваться ботом?

help-get-rates = 📌 1. Получить информацию о курсах.

help-get-rates-desc = Нажми кнопку «📊 Все курсы валют». Бот покажет актуальный курс всех доступных валют в боте.

help-add-currency = 📌 2. Добавить валюту в список отслеживания.

help-add-currency-desc = Нажми кнопку «📈 Выбрать валюту». При выборе валюты нажми «⭐ Добавить» для отслеживания изменения цены валюты. В зависимости от подписки можно отслеживать от 1 до 20 валют одновременно.

help-set-alert = 📌 3. Настроить уведомления о курсе.

help-set-alert-desc = Нажми «⏰ Настроить уведомления» и выбери валюту из списка отслеживаемых. Укажи пороговое значение цены (например, Bitcoin > 50 000$). Бот отправит уведомление, когда курс достигнет указанного значения.

help-manage-subscription = 📌 4. Управление подпиской.

help-manage-subscription-desc = В разделе «📜 Подписка» ты можешь:
  - Узнать текущий тариф и лимиты.
  - Купить новую подписку с помощью Telegram Stars.
  - Посмотреть срок действия подписки.
  - После покупки подписки лимиты валют обновляются автоматически.

help-commands = 📌 5. Основные команды:

help-commands-list = 
  /start — Главное меню
  /help — Помощь
  /subscription — Управление подпиской

help-support = ✉️ Служба поддержки: @SupportBot

rates-header = 📊 Текущие курсы криптовалют:

rate-format-usd = { $name } ({ $symbol }): ${ $price }

rate-format-rub = { $name } ({ $symbol }): { $price } ₽

rates-updated = 🕒 Обновлено: { $time } (UTC+0)