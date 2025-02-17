hello-user = 👋 Hello, { $username }!
default-username = Friend
subscription-info = 💳 Your subscription: { $plan }
subscription-currencies = 💰 Coins selected for tracking: { $current }/{ $max }
subscription-expires-infinite = ⏳ Lifetime subscription
subscription-expires-until = ⏳ Subscription end date: { $expires } (UTC+0)
subscription-purchase-success = ✅ Subscription successfully purchased! Thank you for your purchase.
subscription-terms-link = Please review the terms before payment: /subscription_terms
welcome-text = 📢 Want to be the first to know when a price rises or falls? Choose a coin, set a threshold, and our bot will notify you when the price reaches your specified level! 🚀
select-action = Choose an action:
subscription-plans = Subscription plans:
plan-basic-description = Basic — up to { $limit } currencies
plan-standard-description = Standard — up to { $limit } currencies
plan-premium-description = Premium — up to { $limit } currencies
subscription-validity-period = Subscription validity period: 30 days
subscription-already-active = ❌ You already have an active subscription "{ $plan }" until { $expires }. You cannot purchase a new one until the current one expires.
subscription-already-active-db = ❌ You already have an active subscription "{ $plan }" until { $expires }. You cannot purchase a new one until the current one expires.
price-star = { $price } ⭐
#payment
subscription-payment-button = Send { $price } ⭐️
subscription-invoice-title = Subscription { $plan }
subscription-invoice-description = Subscribe to { $plan } for 30 days
subscription-price-label = Subscription { $plan }
#btn
btn-all-rates = 📊 All coin rates
btn-my-currencies = 🎯 My coins
btn-choose-currency = 🪙 Choose coin
btn-set-alert = 🔔 Set up alerts
btn-subscription = 💳 Subscription
btn-help = ❓ Help
btn-basic = 🔰 Buy Basic
btn-standard = 💎 Buy Standard
btn-premium = 👑 Buy Premium
btn-back = ⬅️ Back
button-enable-alerts = 🔔 Enable alerts
button-disable-alerts = 🔕 Disable alerts
button-set-threshold-usd = 💲 Set threshold in $
button-set-threshold-rub = 💲 Set threshold in ₽
button-set-threshold-above = 📈 Set upper threshold
button-set-threshold-below = 📉 Set lower threshold
btn-toggle-currency = 🔄 Show in { $currency }
button-choose-usd = 💵 In dollars (USD)
button-choose-rub = 💰 In rubles (RUB)
btn-set-new-threshold = 📝 Set new threshold
#help
help-text = 👋 Hello! This is the help section
help-how-to-use = 🔍 How to use the bot?
help-get-rates = 📌 1. Get rate information.
help-get-rates-desc = Press the “📊 All coin rates” button. The bot will display the current rates of all available coins.
help-my-currencies = 📌 2. 🎯 My Coins.
help-my-currencies-desc = In the «🎯 My Coins» section you can:
  - View all your tracked coins
  - Check current prices
help-add-currency = 📌 3. Add a coin to the tracking list.
help-add-currency-desc = Press the “🪙 Choose coin” button. When selecting a coin, tap “☑️ Coin” to track its price changes. Depending on your subscription, you can track from 1 to 10 coins simultaneously.
help-set-alert = 📌 4. Set up rate alerts.
help-set-alert-desc = Tap “🔔 Set up alerts” and choose a coin from your tracking list. Enter the threshold price (e.g., upper threshold for Bitcoin 99000$). The bot will send a notification when the rate reaches the specified value.
help-manage-subscription = 📌 5. Manage subscription.
help-manage-subscription-desc = In the “💳 Subscription” section, you can:
  - Check your current plan and limits.
  - Purchase a new subscription using Telegram Stars.
  - View the subscription validity period.
  - After purchasing a subscription, coin limits are updated automatically.
help-commands = 📌 6. Main commands:
help-commands-list = 
  /start — Main menu
  /help — Help
  /subscription — Manage subscription
  /subscription_terms — Subscription terms
  /support — Support
help-support = ✉️ Support: pricealertprobot@outlook.com
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
cmd-start = Start the bot
cmd-help = Help
cmd-subscription = Manage subscription
cmd-subscription-terms = Subscription terms
cmd-support = Support
my-currencies-empty = ⚠️ You haven’t selected any coins yet
alerts-no-currencies = ⚠️ You have no coins being tracked. Add coins in the “My coins” section.
subscription-limit-reached = ⚠️ You have reached the coin tracking limit for your subscription! To add more coins, you will need a different subscription plan.
currency-added = ✅ Coin {$currency} added for tracking
currency-removed = ❌ Coin {$currency} removed from tracking
choose-currency-instruction = Choose coins to track:
✅ - coin is being tracked
☑️ - coin is not being tracked
# alerts
alerts-list-header = 🔔 Alert settings for ❨{$currency}❩
alerts-choose-currency = Choose a coin to set up alerts:
alerts-error = ❌ An error occurred. Please try again later.
alerts-current-price = Current price:
alerts-current-price-both = Current price: {$price_usd} $ / {$price_rub} ₽
alerts-current-settings = Current settings:
alerts-notifications-enabled = ✅ Alerts enabled
alerts-notifications-disabled = ❌ Alerts disabled
alerts-usd-header = Threshold values (USD):
alerts-rub-header = Threshold values (RUB):
alerts-not-set = not set
alerts-threshold-above = ⬆️ Above
alerts-threshold-below = ⬇️ Below
alerts-disabled-successfully = ✅ Alerts successfully disabled
alert-details = Currency: {$currency}
alerts-no-thresholds = ℹ️ To enable alerts, first set the threshold values!
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
select-condition = Choose the condition for the alert:
enter-threshold-value = Enter the threshold value:
invalid-threshold-value = ❌ Invalid value. Please enter a positive number.
enter-new-threshold = Enter the new threshold value for { $currency } in { $currency_type }:
# Errors
error-occurred = ❌ An error occurred. Please try again later.
currency-not-found = ❌ Currency not found.
rate-not-found = ❌ Unable to retrieve the currency rate.
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
                          - Whole numbers: 1, 10, 100
                          - With decimals: 1.23, 0.0012
error-threshold-too-large = ❌ The value is too high. The maximum allowed value is 999999999
unsupported-text-message = Sorry, I do not understand text. Please use the bot commands or menu buttons.
unsupported-photo = Sorry, I do not process photos. Please use the bot commands or menu buttons.
unsupported-sticker = Sorry, I do not process stickers. Please use the bot commands or menu buttons.
unsupported-document = Sorry, I do not process documents. Please use the bot commands or menu buttons.
unsupported-voice = Sorry, I do not process voice messages. Please use the bot commands or menu buttons.
unsupported-video = Sorry, I do not process videos. Please use the bot commands or menu buttons.
unsupported-message = Sorry, this type of message is not supported. Please use the bot commands or menu buttons.
subscription-terms-text = 
      📄 Subscription Terms

      1. Free Subscription (Free)
      📊 Available: 1 coin for monitoring.
      🔄 Flexibility: You can change the selected coin at any time.
      💡 Recommendation: We recommend starting with the free version to evaluate the bot's functionality.

      2. Paid Subscriptions
      Basic (200 Stars):
      📈 Monitoring: Up to { $basic_limit } coins.
      ⏳ Validity: 30 days.

      Standard (300 Stars):
      📈 Monitoring: Up to { $standard_limit } coins.
      ⏳ Validity: 30 days.
      
      Premium (400 Stars):
      📈 Monitoring: Up to { $premium_limit } coins.
      ⏳ Validity: 30 days.

      3. Important Terms
      ❗ No Refunds: Refunds are not provided after purchasing a subscription.
      🔄 Plan Change: You can change your paid subscription plan only after the current subscription expires (for example, switch from Premium to Standard).
      ⛔ Manual Renewal: Subscriptions do not renew automatically — payment is made manually.
      💎 Use of Telegram Stars: Telegram Stars are used exclusively for digital services (the sale of physical goods is prohibited).

      4. Recommendations
      🚀 Testing: Before purchasing a paid subscription, we recommend using the free version to ensure the bot's functionality meets your needs.
      ⚠️ Choose Carefully: Choose your plan carefully, as it cannot be changed after purchase.
      Legal Disclaimer:
      By purchasing a subscription, you agree to these terms. All subscriptions are final, and refunds are not provided. The bot provides digital services only and is not responsible for any potential losses incurred while using the service.
cmd-support-text =
      🛠 Support

      If you have any questions, payment issues, or problems with the bot's functionality, please contact us: 
      ✉️ pricealertprobot@outlook.com

      ⏰ Support Hours: 
      Our support service is available from 12:00 to 21:00 (UTC+0).

      ❗ Important:  
      🚀 Testing: Before purchasing a paid subscription, we recommend using the free version to ensure the bot's functionality meets your needs.
      ⚠️ Choose Carefully: Choose your plan carefully, as it cannot be changed after purchase.
      
      Legal Disclaimer:
      All subscriptions are final, and refunds are not provided. The bot provides digital services only and is not responsible for any potential losses incurred while using the service. (see “Subscription Terms”).  
      
      Please note: Response times may vary.