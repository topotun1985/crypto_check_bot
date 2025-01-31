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
