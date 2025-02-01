hello-user = Hello, { $username }!

subscription-info = 📜 Your subscription: { $plan } 

subscription-currencies = 💰 Tracked currencies: { $current }/{ $max }

subscription-expires-infinite = ⏳ Unlimited subscription

subscription-expires-until = ⏳  Subscription end date: { $expires } (UTC+0)

subscription-purchase-success = ✅ Subscription successfully purchased! Thank you.

welcome-text = 📢 To receive notifications, choose a cryptocurrency and set a threshold value. The bot will alert you when the price reaches the right level! 🚀

select-action = Choose action:

subscription-plans = Subscription plans:

plan-basic-description = Basic — { $limit } currencies

plan-standard-description = Standard — { $limit } currencies

plan-premium-description = Premium — { $limit } currencies

subscription-validity-period = Subscription validity period: 30 days

subscription-already-active = ❌ You already have an active "{ $plan }" subscription until { $expires }. You cannot buy a new one until the current one expires.

subscription-already-active-db = ❌ You already have an active "{ $plan }" subscription until { $expires }. You cannot buy a new one until the current one expires.

price-star = { $price } ⭐

btn-all-rates = 📊 All rates

btn-choose-currency = 📈 Choose currency

btn-set-alert = ⏰ Set alerts

btn-subscription = 📜 Subscription

btn-help = ❓ Help

btn-basic = 💳 Buy basic

btn-standard = 💎 Buy standard

btn-premium = 👑 Buy premium

btn-back = ⬅️ Back



help-text = 👋 Hello! This is the help section.

help-how-to-use = 🔍 How to use the bot?

help-get-rates = 📌 1. Get exchange rate information.

help-get-rates-desc = Click the "📊 All exchange rates" button. The bot will show the current rate of all available currencies.

help-add-currency = 📌 2. Add a currency to the watchlist.

help-add-currency-desc = Click the "📈 Select currency" button. When selecting a currency, click "⭐ Add" to track its price changes. Depending on your subscription, you can track from 1 to 20 currencies.

help-set-alert = 📌 3. Set price alerts.

help-set-alert-desc = Click "⏰ Set alert" and select a currency from the watchlist. Set a price threshold (e.g., Bitcoin > $50,000). The bot will send a notification when the rate reaches the specified value.

help-manage-subscription = 📌 4. Manage your subscription.

help-manage-subscription-desc = In the "📜 Subscription" section, you can:
  - Check your current plan and limits.
  - Purchase a new subscription using Telegram Stars.
  - See the expiration date of your subscription.
  - After purchasing a subscription, currency limits are updated automatically.

help-commands = 📌 5. Main commands:

help-commands-list = 
  /start — Main menu
  /help — Help
  /subscription — Manage subscription

help-support = ✉️ Support: @SupportBot

rates-header = 📊 Current cryptocurrency rates:

rate-format-usd = { $name } ({ $symbol }): ${ $price }

rate-format-rub = { $name } ({ $symbol }): { $price } ₽

rates-updated = 🕒 Updated: { $time } (UTC+0)


rates-error = ❌ Error getting rates. Please try again later.


cmd-start = Start bot

cmd-help = Help

cmd-subscription = Subscription management


btn-my-currencies = 👀 My Currencies

my-currencies-empty = ⚠️ You haven't selected any currencies yet

subscription-limit-reached = ⚠️ Currency limit reached for your subscription. To track more currencies, please upgrade to a paid subscription.

currency-added = ✅ Currency {$currency} added to tracking

currency-removed = ❌ Currency {$currency} removed from tracking

# Alerts
alerts-list-header = 🔔 Alert Settings
alerts-choose-currency = Choose a currency to set up alerts:
alerts-no-currencies = You don't have any tracked currencies. Add currencies in the "My Currencies" section.
alerts-error = ❌ An error occurred. Please try again later.
alerts-currency-not-found = ❌ Currency not found.

alerts-settings-header = 🔔 Alert Settings for { $currency }
alerts-current-price = 💰 Current price: { $price } USD

alerts-current-settings = Current settings:
alerts-notifications-enabled = ✅ Notifications enabled
alerts-notifications-disabled = ❌ Notifications disabled
alerts-threshold-not-set = 💲 Threshold not set
alerts-threshold-usd = 💲 Threshold: { $threshold } USD
alerts-percent-not-set = 📊 Percent change not set
alerts-percent-change = 📊 Percent change: { $percent }%

alerts-enabled = ✅ Notifications for { $currency } enabled
alerts-disabled = ❌ Notifications for { $currency } disabled
alerts-threshold-set = ✅ Threshold set to: { $value } USD
alerts-percent-set = ✅ Percent change set to: { $value }%

alerts-enter-threshold = Enter threshold value in USD:
alerts-enter-percent = Enter percent change (positive number):
alerts-invalid-number = ❌ Please enter a valid number
alerts-invalid-percent = ❌ Please enter a positive number

# Percentage changes
alerts-choose-percent-type = Choose price change type:
alerts-percent-type-up = 📈 On increase
alerts-percent-type-down = 📉 On decrease
alerts-percent-type-both = 🔄 On any change

alerts-percent-type-up-text = on increase
alerts-percent-type-down-text = on decrease
alerts-percent-type-both-text = on any change

alerts-enter-percent-with-type = Enter percentage change {$type}:
alerts-percent-set-with-type = ✅ Alert set {$type} when price changes by {$value}%

alerts-percent-type-current-up = 📈 On increase by {$value}%
alerts-percent-type-current-down = 📉 On decrease by {$value}%
alerts-percent-type-current-both = 🔄 On any change by {$value}%

# Buttons
button-enable-alerts = 🔔 Enable notifications
button-disable-alerts = 🔕 Disable notifications
button-set-threshold = 💲 Set threshold
button-change-threshold = 💲 Change threshold
button-set-percent = 📊 Set percent
button-back-to-alerts = ↩️ Back to currencies
