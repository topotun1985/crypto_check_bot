hello-user = 👋 Hello, { $username }!
subscription-info = 📜 Your subscription: { $plan }
subscription-currencies = 💰 Coins tracked: { $current }/{ $max }
subscription-expires-infinite = ⏳ Lifetime subscription
subscription-expires-until = ⏳ Subscription expires on: { $expires } (UTC+0)
subscription-purchase-success = ✅ Subscription purchased successfully! Thank you for your purchase.
welcome-text = 📢 Want to be the first to know when prices rise or fall? Choose a coin, set a threshold, and our bot will notify you when the price reaches your target! 🚀
select-action = Choose an action:
subscription-plans = Subscription Plans:
plan-basic-description = Basic — up to { $limit } coins
plan-standard-description = Standard — up to { $limit } coins
plan-premium-description = Premium — up to { $limit } coins
subscription-validity-period = Subscription validity: 30 days
subscription-already-active = ❌ You already have an active subscription "{ $plan }" until { $expires }. You cannot purchase a new one until the current one expires.
subscription-already-active-db = ❌ You already have an active subscription "{ $plan }" until { $expires }. You cannot purchase a new one until the current one expires.
price-star = { $price } ⭐
#btn
btn-all-rates = 📊 All coin rates
btn-choose-currency = 💎 Choose coin
btn-set-alert = ⏰ Set alerts
btn-subscription = 📜 Subscription
btn-help = ❓ Help
btn-basic = 💳 Buy Basic
btn-standard = 💎 Buy Standard
btn-premium = 👑 Buy Premium
btn-back = ⬅️ Back
button-enable-alerts = 🔔 Enable alerts
button-disable-alerts = 🔕 Disable alerts
button-set-threshold-usd = 💲 Set threshold in $
button-set-threshold-rub = 💲 Set threshold in ₽
button-set-threshold-above = 📈 set upper threshold
button-set-threshold-below = 📉 set lower threshold
btn-toggle-currency = 🔄 Show in { $currency }
button-choose-usd = 💵 In dollars (USD)
button-choose-rub = 💰 In rubles (RUB)
btn-set-new-threshold = 📝 Set new threshold
btn-my-currencies = 🎯 My coins
#help
help-text = 👋 Hello! This is the help section.
help-how-to-use = 🔍 How to use the bot?
help-get-rates = 📌 1. Get coin rates.
help-get-rates-desc = Press the “📊 All coin rates” button. The bot will display the current rate of all available coins.
help-add-currency = 📌 2. Add a coin to your tracking list.
help-add-currency-desc = Press the “💎 Choose coin” button. When selecting a coin, press “⭐ Add” to track its price changes. Depending on your subscription, you can track from 1 up to 20 coins.
help-set-alert = 📌 3. Set price alerts.
help-set-alert-desc = Press “⏰ Set alerts” and choose a coin from your tracked list. Specify a threshold price (e.g., Bitcoin > $50,000). The bot will notify you when the rate reaches the specified value.
help-manage-subscription = 📌 4. Manage subscription.
help-manage-subscription-desc = In the “📜 Subscription” section you can:
  - View your current plan and limits.
  - Purchase a new subscription using Telegram Stars.
  - Check the subscription expiration date.
  - After purchase, the coin limits update automatically.
help-commands = 📌 5. Main commands:
help-commands-list = 
  /start — Main menu
  /help — Help
  /subscription — Manage subscription
help-support = ✉️ Support: @SupportBot
#rate
rates-header = 📊 Current cryptocurrency rates:
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Updated: { $time } (UTC+0)
dollar-rate = Dollar rate: { $price } ₽
show-in-rub = in rubles
show-in-usd = in dollars
rates-error = ❌ An error occurred while fetching rates. Please try again later.
# Commands
cmd-start = Запустить бота
cmd-help = Помощь
cmd-subscription = Управление подпиской
cmd-subscription-terms = Условия подписок
cmd-support = Поддержка
my-currencies-empty = ⚠️ You haven't selected any coins yet
alerts-no-currencies = ⚠️ You have no tracked coins. Add coins in the "My coins" section.
subscription-limit-reached = ⚠️ You have reached the limit of tracked coins for your subscription! To add more coins, a different subscription plan is required.
currency-added = ✅ Coin {$currency} added for tracking
currency-removed = ❌ Coin {$currency} removed from tracking
choose-currency-instruction = Choose the coins you want to track:
✅ - coin is tracked
☑️ - coin is not tracked
# alerts
alerts-list-header = 🔔 Alert settings for { $currency }
alerts-choose-currency = Choose a coin to set up alerts:
alerts-error = ❌ An error occurred. Please try again later.
alerts-current-price = Current price:
alerts-current-price-both = Current price: { $price_usd } $ / { $price_rub } ₽
alerts-current-settings = Current settings:
alerts-notifications-enabled = ✅ Alerts are enabled
alerts-notifications-disabled = ❌ Alerts are disabled
alerts-usd-header = Thresholds (USD):
alerts-rub-header = Thresholds (RUB):
alerts-not-set = not set
alerts-threshold-above = ⬆️ Above
alerts-threshold-below = ⬇️ Below
alerts-disabled-successfully = ✅ Alerts disabled successfully
alert-details = Coin: { $currency }
alerts-no-thresholds = ℹ️ To enable alerts, first set threshold values!
no-alerts-to-disable = ⚠️ There are no active alerts to disable
alert-added-successfully = ✅ Alert added successfully!
alert-updated-successfully = ✅ Alert updated successfully!
alert-price = Price
alert-price-above = ⬆️ exceeded
alert-price-below = ⬇️ dropped below
alert-not-found = ⚠️ Alert not found
error-invalid-alert = ❌ Error: invalid alert ID
alerts-enter-threshold-above-usd = Enter the upper price threshold in USD:
alerts-enter-threshold-below-usd = Enter the lower price threshold in USD:
alerts-enter-threshold-above-rub = Enter the upper price threshold in RUB:
alerts-enter-threshold-below-rub = Enter the lower price threshold in RUB:
# Threshold Settings
select-currency-type = 💵 Choose the currency for the threshold:
select-condition = Choose the alert condition:
enter-threshold-value = Enter the threshold value:
invalid-threshold-value = ❌ Invalid value. Please enter a positive number.
enter-new-threshold = Enter a new threshold value for { $currency } in { $currency_type }:
# Errors
error-occurred = ❌ An error occurred. Please try again later.
currency-not-found = ❌ Coin not found.
rate-not-found = ❌ Unable to retrieve the coin rate.
alerts-invalid-number = ❌ Please enter a valid number
error-threshold-must-be-positive = ❌ The value must be greater than 0
error-threshold-invalid-format = ❌ Invalid number format. Use a dot as the decimal separator (e.g., 1.23)
error-threshold-too-many-decimals-small = ❌ Too many digits after the decimal point: { $decimals }
                                          For numbers less than 1, a maximum of 5 decimal places is allowed
                                          Example: 0.00123
error-threshold-too-many-decimals-large = ❌ Too many digits after the decimal point: { $decimals }
                                          For numbers greater than or equal to 1, a maximum of 2 decimal places is allowed
                                          Examples: 1.23, 10.5, 100.00
error-threshold-generic = ❌ Please enter a valid number
                          Examples:
                          - Integers: 1, 10, 100
                          - With a dot: 1.23, 0.0012
error-threshold-too-large = ❌ The value is too large. Maximum allowed value is 999,999,999