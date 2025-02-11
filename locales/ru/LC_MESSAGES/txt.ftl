hello-user = 👋 Привет, { $username }!
subscription-info = 📜 Ваша подписка: { $plan }
subscription-currencies = 💰 Выбрано монет для отслеживания: { $current }/{ $max }
subscription-expires-infinite = ⏳ Бессрочная подписка
subscription-expires-until = ⏳ Дата окончания подписки: { $expires } (UTC+0)
subscription-purchase-success = ✅ Подписка успешно оформлена! Спасибо за покупку.
welcome-text = 📢 Хотите быть первыми, кто узнает о росте или падении цены? Выберите монету, задайте порог, и наш бот уведомит вас, когда цена дойдет до нужного уровня! 🚀
select-action = Выбери действие:
subscription-plans = Планы подписки:
plan-basic-description = Базовый — максимально { $limit } валют
plan-standard-description = Стандарт — максимально { $limit } валют
plan-premium-description = Премиум — максимально { $limit } валют
subscription-validity-period = Срок действия подписки: 30 дней
subscription-already-active = ❌ У вас уже есть активная подписка "{ $plan }" до { $expires }. Вы не можете купить новую, пока не истечёт текущая.
subscription-already-active-db = ❌ У вас уже есть активная подписка "{ $plan }" до { $expires }. Вы не можете купить новую, пока не истечёт текущая.
price-star = { $price } ⭐
#btn
btn-all-rates = 📊 Все курсы монет
btn-choose-currency = 💎 Выбрать монету
btn-set-alert = ⏰ Настроить уведомления
btn-subscription = 📜 Подписка
btn-help = ❓ Помощь
btn-basic = 💳 Купить базовый
btn-standard = 💎 Купить стандартный
btn-premium = 👑 Купить премиум
btn-back = ⬅️ Назад
button-enable-alerts = 🔔 Включить уведомления
button-disable-alerts = 🔕 Выключить уведомления
button-set-threshold-usd = 💲 Установить порог в $
button-set-threshold-rub = 💲 Установить порог в ₽
button-set-threshold-above = 📈 установить верхний порог
button-set-threshold-below = 📉 установить нижний порог
btn-toggle-currency = 🔄 Показать в { $currency }
button-choose-usd = 💵 В долларах (USD)
button-choose-rub = 💰 В рублях (RUB)
btn-set-new-threshold = 📝 Установить новый порог
btn-my-currencies = 🎯 Мои монеты
#help
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
#rate
rates-header = 📊 Текущие курсы криптовалют:
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Обновлено: { $time } (UTC+0)
dollar-rate = Курс доллара: { $price } ₽
show-in-rub = рублях
show-in-usd = долларах
rates-error = ❌ Произошла ошибка при получении курсов. Пожалуйста, попробуйте позже.
# Commands
cmd-start = Запустить бота
cmd-help = Помощь
cmd-subscription = Управление подпиской
my-currencies-empty = ⚠️ Вы пока не выбрали ни одной монеты
alerts-no-currencies = ⚠️ У вас нет отслеживаемых монет. Добавьте монеты в разделе "Мои монеты".
subscription-limit-reached = ⚠️ Вы достигли лимита отслеживаемых монет для вашей подписки! Чтобы добавить больше монет, требуется другой тип подписки.
currency-added = ✅ Монета {$currency} добавлена для отслеживания
currency-removed = ❌ Монета {$currency} удалена из отслеживания
choose-currency-instruction = Выберите монеты для отслеживания:
✅ - монета отслеживается
☑️ - монета не отслеживается
# alerts
alerts-list-header = 🔔 Настройки уведомлений для ❨{$currency}❩
alerts-choose-currency = Выберите монету для настройки уведомлений:
alerts-error = ❌ Произошла ошибка. Попробуйте позже.
alerts-current-price = Текущая цена:
alerts-current-price-both = Текущая цена: {$price_usd} $ / {$price_rub} ₽⁩
alerts-current-settings = Текущие настройки:
alerts-notifications-enabled = ✅ Уведомления включены
alerts-notifications-disabled = ❌ Уведомления отключены
alerts-usd-header = Пороговые значения (USD):
alerts-rub-header = Пороговые значения (RUB):
alerts-not-set = не установлен
alerts-threshold-above = ⬆️ Выше
alerts-threshold-below = ⬇️ Ниже
alerts-disabled-successfully = ✅ Уведомления успешно отключены
alert-details = Валюта: {$currency}
alerts-no-thresholds = ℹ️ Чтобы включить уведомления, сначала установите пороговые значения!
no-alerts-to-disable = ⚠️ Нет активных уведомлений для отключения
alert-added-successfully = ✅ Уведомление успешно добавлено!
alert-updated-successfully = ✅ Уведомление успешно обновлено!
alert-price = Цена
alert-price-above = ⬆️ превысила
alert-price-below = ⬇️ опустилась ниже
alert-not-found = ⚠️ Уведомление не найдено
error-invalid-alert = ❌ Ошибка: неверный ID уведомления
alerts-enter-threshold-above-usd = Введите верхний порог цены в USD:
alerts-enter-threshold-below-usd = Введите нижний порог цены в USD:
alerts-enter-threshold-above-rub = Введите верхний порог цены в рублях:
alerts-enter-threshold-below-rub = Введите нижний порог цены в рублях:
# Threshold Settings
select-currency-type = 💵 Выберите валюту для порога:
select-condition = Выберите условие для уведомления:
enter-threshold-value = Введите пороговое значение:
invalid-threshold-value = ❌ Некорректное значение. Пожалуйста, введите положительное число.
enter-new-threshold = Введите новое пороговое значение для { $currency } в { $currency_type }:
# Errors
error-occurred = ❌ Произошла ошибка. Пожалуйста, попробуйте позже.
currency-not-found = ❌ Валюта не найдена.
rate-not-found = ❌ Не удалось получить курс валюты.
alerts-invalid-number = ❌ Пожалуйста, введите корректное число

currency-settings-menu = Настройки уведомлений для { $currency }
Выберите действие:исло
error-threshold-must-be-positive = ❌ Значение должно быть больше 0
error-threshold-invalid-format = ❌ Неверный формат числа. Используйте точку в качестве разделителя (например: 1.23)
error-threshold-too-many-decimals-small = ❌ Слишком много знаков после точки: { $decimals }\nДля чисел меньше 1 допустимо максимум 5 знаков после точки\nПример: 0.00123
error-threshold-too-many-decimals-large = ❌ Слишком много знаков после точки: { $decimals }\nДля чисел больше или равных 1 допустимо максимум 2 знака после точки\nПримеры: 1.23, 10.5, 100.00
error-threshold-generic = ❌ Введите корректное число\nПримеры:\n- Целые числа: 1, 10, 100\n- С точкой: 1.23, 0.0012