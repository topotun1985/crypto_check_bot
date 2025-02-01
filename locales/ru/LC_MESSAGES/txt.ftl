hello-user = 👋 Привет, { $username }!

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



dollar-rate = Курс доллара: { $price } ₽

btn-toggle-currency = 🔄 Показать в { $currency }

show-in-rub = рублях

show-in-usd = долларах

rates-error = ❌ Произошла ошибка при получении курсов. Пожалуйста, попробуйте позже.


cmd-start = Запустить бота

cmd-help = Помощь

cmd-subscription = Управление подпиской


btn-my-currencies = 👀 Мои валюты

my-currencies-empty = ⚠️ Вы пока не выбрали ни одной валюты

subscription-limit-reached = ⚠️ Достигнут лимит валют для вашей подписки. Для отслеживания большего количества валют приобретите платную подписку.

currency-added = ✅ Валюта {$currency} добавлена для отслеживания

currency-removed = ❌ Валюта {$currency} удалена из отслеживания

choose-currency-instruction = Выберите валюты для отслеживания:

✅ - валюта отслеживается

☑️ - валюта не отслеживается

# Уведомления
alerts-list-header = 🔔 Настройки уведомлений
alerts-choose-currency = Выберите валюту для настройки уведомлений:
alerts-no-currencies = У вас нет отслеживаемых валют. Добавьте валюты в разделе "Мои валюты".
alerts-error = ❌ Произошла ошибка. Попробуйте позже.
alerts-currency-not-found = ❌ Валюта не найдена.

alerts-settings-header = 🔔 Настройки уведомлений для { $currency }
alerts-current-price-both = 💰 Текущая цена: { $price_usd } USD / { $price_rub } ₽

alerts-current-settings = Текущие настройки:
alerts-notifications-enabled = ✅ Уведомления включены
alerts-notifications-disabled = ❌ Уведомления выключены
alerts-threshold-not-set = 💲 Пороговое значение не установлено
alerts-threshold-usd = 💲 Пороговое значение: { $threshold_usd } USD
alerts-threshold-rub = 💲 Пороговое значение: { $threshold_rub } ₽
alerts-percent-not-set = 📊 Процент изменения не установлен
alerts-percent-change = 📊 Процент изменения: { $percent }%

alerts-enabled = ✅ Уведомления для { $currency } включены
alerts-disabled = ❌ Уведомления для { $currency } выключены
alerts-threshold-set-usd = ✅ Установлено пороговое значение: { $value } USD
alerts-threshold-set-rub = ✅ Установлено пороговое значение: { $value } ₽
alerts-percent-set = ✅ Установлен процент изменения: { $value }%

alerts-choose-currency-usd-rub = Выберите валюту для порога:
alerts-choose-usd = В долларах (USD)
alerts-choose-rub = В рублях (₽)
alerts-enter-threshold-usd = Введите пороговое значение в USD:
alerts-enter-threshold-rub = Введите пороговое значение в рублях:
alerts-enter-percent = Введите процент изменения (положительное число):
alerts-invalid-number = ❌  Пожалуйста, введите корректное число
alerts-invalid-percent = ❌ Пожалуйста, введите положительное число

# Процентные изменения
alerts-choose-percent-type = Выберите тип изменения цены:
alerts-percent-type-up = При росте
alerts-percent-type-down = При падении
alerts-percent-type-both = При любом изменении

alerts-percent-type-up-text = при росте
alerts-percent-type-down-text = при падении
alerts-percent-type-both-text = при любом изменении

alerts-enter-percent-with-type = Введите процент изменения {$type}:
alerts-percent-set-with-type = Установлено уведомление {$type} при изменении на {$value}%

alerts-percent-type-current-up = При росте на {$value}%
alerts-percent-type-current-down = При падении на {$value}%
alerts-percent-type-current-both = При изменении на {$value}%

# Кнопки
button-enable-alerts = 🔔 Включить уведомления
button-disable-alerts = 🔕 Выключить уведомления
button-set-threshold = 💲 Установить порог
button-change-threshold = 💲 Изменить порог
button-set-threshold-usd = 💲 Установить порог (USD)
button-set-threshold-rub = 💲 Установить порог (₽)
button-set-percent = 📊 Установить процент
button-back-to-alerts = ↩️ К списку валют

alert-threshold-reached = 🚨 { $currency } достиг { $price } $!

alert-percent-changed = 📊 { $currency } изменился на { $percent }% за 24ч!
Текущая цена: { $price } $
