hello-user = 👋 Привет, { $username }!

subscription-info = 📜 Ваша подписка: { $plan }

subscription-currencies = 💰 Выбрано монет для отслеживания: { $current }/{ $max }

subscription-expires-infinite = ⏳ Бессрочная подписка

subscription-expires-until = ⏳ Дата окончания подписки: { $expires } (UTC+0)

subscription-purchase-success = ✅ Подписка успешно оформлена! Спасибо за покупку.

welcome-text = 📢 Чтобы получать уведомления, выбери монету и установи пороговое значение. Бот предупредит тебя, когда цена достигнет нужного уровня! 🚀

select-action = Выбери действие:

subscription-plans = Планы подписки:

plan-basic-description = Базовый — { $limit } валют

plan-standard-description = Стандарт — { $limit } валют

plan-premium-description = Премиум — { $limit } валют

subscription-validity-period = Срок действия подписки: 30 дней

subscription-already-active = ❌ У вас уже есть активная подписка "{ $plan }" до { $expires }. Вы не можете купить новую, пока не истечёт текущая.

subscription-already-active-db = ❌ У вас уже есть активная подписка "{ $plan }" до { $expires }. Вы не можете купить новую, пока не истечёт текущая.

price-star = { $price } ⭐

btn-all-rates = 📊 Все курсы монет

btn-choose-currency = 💎 Выбрать монету

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

help-get-rates-desc = Нажми кнопку «📊 Все курсы монет». Бот покажет актуальный курс всех доступных монет в боте.

help-add-currency = 📌 2. Добавить монету в список отслеживания.

help-add-currency-desc = Нажми кнопку «📈 Выбрать монету». При выборе монеты нажми «⭐ Добавить» для отслеживания изменения цены монеты. В зависимости от подписки можно отслеживать от 1 до 20 монет одновременно.

help-set-alert = 📌 3. Настроить уведомления о курсе.

help-set-alert-desc = Нажми «⏰ Настроить уведомления» и выбери монету из списка отслеживаемых. Укажи пороговое значение цены (например, Bitcoin > 50 000$). Бот отправит уведомление, когда курс достигнет указанного значения.

help-manage-subscription = 📌 4. Управление подпиской.

help-manage-subscription-desc = В разделе «📜 Подписка» ты можешь:
  - Узнать текущий тариф и лимиты.
  - Купить новую подписку с помощью Telegram Stars.
  - Посмотреть срок действия подписки.
  - После покупки подписки лимиты монет обновляются автоматически.

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


btn-my-currencies = 🎯 Мои монеты

my-currencies-empty = ⚠️ Вы пока не выбрали ни одной монеты
alerts-no-currencies = ⚠️ У вас нет отслеживаемых монет. Добавьте монеты в разделе "Мои монеты".

subscription-limit-reached = ⚠️ Достигнут лимит монет для вашей подписки. Для отслеживания большего количества монет приобретите платную подписку.

currency-added = ✅ Монета {$currency} добавлена для отслеживания

currency-removed = ❌ Монета {$currency} удалена из отслеживания

choose-currency-instruction = Выберите монеты для отслеживания:

✅ - монета отслеживается

☑️ - монета не отслеживается

# Уведомления
alerts-list-header = 🔔 Настройки уведомлений
alerts-choose-currency = Выберите монету для настройки уведомлений:
alerts-no-currencies = ⚠️ У вас нет отслеживаемых монет. Добавьте монеты в разделе "Мои монеты".
alerts-error = ❌ Произошла ошибка. Попробуйте позже.
alerts-currency-not-found = ❌ Монета не найдена.

alerts-settings-header = Настройки уведомлений для {$currency}

alerts-current-price = Текущая цена: {$price} USD
alerts-current-price-both = Текущая цена: {$price_usd} USD / {$price_rub} RUB

alerts-current-settings = Текущие настройки:

alerts-notifications-enabled = ✅ Уведомления включены
alerts-notifications-disabled = ❌ Уведомления отключены

alerts-usd-header = Пороговые значения (USD):
alerts-usd-not-set = Пороговые значения в USD не установлены

alerts-rub-header = Пороговые значения (RUB):
alerts-rub-not-set = Пороговые значения в RUB не установлены

alerts-threshold-above = ⬆️ Выше {$threshold}
alerts-threshold-below = ⬇️ Ниже {$threshold}

alerts-enabled = ✅ Уведомления для {$currency} включены
alerts-disabled = ❌ Уведомления для {$currency} отключены

alerts-error = ❌ Произошла ошибка при обработке уведомлений
alerts-currency-not-found = ❌ Монета не найдена


# Кнопки
button-enable-alerts = 🔔 Включить уведомления
button-disable-alerts = 🔕 Выключить уведомления
button-set-threshold = 💲 Установить порог
button-change-threshold = 💲 Изменить порог
button-set-threshold-usd = 💲 Установить порог в USD
button-set-threshold-rub = 💲 Установить порог в ₽
button-back-to-alerts = ↩️ К списку монет

# Кнопки настройки уведомлений
button-disable-alerts = 🔕 Выключить уведомления
button-enable-alerts = 🔔 Включить уведомления
button-set-threshold-above = 📈 установить верхний порог
button-set-threshold-below = 📉 установить нижний порог

alert-threshold-reached = 🚨 { $currency } достиг { $price } $!

Текущая цена: { $price } $

# Notification Settings
notification-settings = 🔔 Настройки уведомлений
choose-currency-for-notifications = Выберите криптовалюту для настройки уведомлений:
no-tracked-currencies = ❌ У вас нет отслеживаемых монет. Добавьте монеты через меню "Отслеживание".

# Alert Details
current-price = Текущая цена: {$current_price}
alert-details = Валюта: {$currency}
Условие: {$condition}
Порог: {$threshold}
Текущая цена: {$current_price}

# Threshold Settings
select-currency-type = Выберите валюту для порога:
choose-currency-type = Выберите валюту для порога:
select-condition = Выберите условие для уведомления:
button-set-threshold-usd = 💲 Установить в USD
button-set-threshold-rub = 💲 Установить в RUB
enter-threshold-value = Введите пороговое значение:
invalid-threshold-value = ❌ Некорректное значение. Пожалуйста, введите положительное число.

no-alerts-to-disable = ⚠️ Нет активных уведомлений для отключения
alerts-disabled-successfully = ✅ Уведомления успешно отключены
alert-added-successfully = ✅ Уведомление успешно добавлено!
alert-updated-successfully = ✅ Уведомление успешно обновлено!

# Navigation
back-button = ↩️ Назад
back-to-settings = « К настройкам
back-to-main = « В главное меню

# Errors
error-occurred = ❌ Произошла ошибка. Пожалуйста, попробуйте позже.
currency-not-found = ❌ Валюта не найдена.
rate-not-found = ❌ Не удалось получить курс валюты.
active-alerts = 📊 Активные уведомления:
no-active-alerts = ❌ Уведомления не настроены
add-alert-usd = 📈 Добавить в USD
add-alert-rub = 📈 Добавить в RUB
delete-alerts = ❌ Удалить все
alert-above = Выше
alert-below = Ниже
choose-alert-condition = Выберите условие для уведомления:
enter-threshold-value = Введите пороговое значение:

choose-currency-type = Выберите валюту для порогового значения:
set-in-usd = Установить в USD
set-in-rub = Установить в RUB
Текущая цена: { $current_price }
invalid-threshold = ❌ Неверное значение. Пожалуйста, введите положительное число.
alert-created = ✅ Уведомление создано
alert-updated = ✅ Уведомление обновлено
alert-deleted = ✅ Уведомления удалены
back-button = 🔙 Назад

# Новые строки для уведомлений
btn-set-new-threshold = 📝 Установить новый порог
btn-disable-alert = 🔕 Отключить уведомление
enter-new-threshold = Введите новое пороговое значение для { $currency } в { $currency_type }:
alert-disabled = 🔕 Уведомления для { $currency } отключены
alert-not-found = ⚠️ Уведомление не найдено
error-invalid-alert = ❌ Ошибка: неверный ID уведомления
error-occurred = ❌ Произошла ошибка. Попробуйте позже.

# Alert Notifications
alert-triggered = 🔔 Уведомление сработало!
{ $currency } достиг{ $currency_ending } { $condition } { $price }
Для продолжения мониторинга установите новое уведомление.

# Кнопки настройки уведомлений
button-enable-alerts = 🔔 Включить уведомления
button-disable-alerts = 🔕 Отключить уведомления
button-set-threshold-above = ⬆️ Установить верхний порог
button-set-threshold-below = ⬇️ Установить нижний порог
button-choose-usd = 💵 В долларах (USD)
button-choose-rub = 💰 В рублях (RUB)
button-back-to-alerts = ↩️ Назад к списку монет

# Сообщения для ввода порогов
alerts-enter-threshold-above-usd = Введите верхний порог цены в USD:
alerts-enter-threshold-below-usd = Введите нижний порог цены в USD:
alerts-enter-threshold-above-rub = Введите верхний порог цены в рублях:
alerts-enter-threshold-below-rub = Введите нижний порог цены в рублях:

# Сообщения об успешной установке порогов
alerts-threshold-set = ✅ Установлен {$type} порог: {$value} {$currency}

# Сообщения о статусе уведомлений
alerts-notifications-enabled = ✅ Уведомления включены
alerts-notifications-disabled = ❌ Уведомления отключены
alerts-no-thresholds = ℹ️ Чтобы включить уведомления, сначала установите пороговые значения!

# Заголовки настроек
alerts-settings-header = 🔔 Настройки уведомлений для {$currency}
alerts-choose-currency-type = 💵 Выберите валюту для порога:

# Сообщения об ошибках
alerts-invalid-number = ❌ Пожалуйста, введите корректное число
alerts-error = ❌ Произошла ошибка при обработке уведомлений
alerts-currency-not-found = ❌ Монета не найдена
