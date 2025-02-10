hello-user = 👋 Hallo, { $username }!
subscription-info = 📜 Dein Abonnement: { $plan }
subscription-currencies = 💰 Verfolgte Coins: { $current }/{ $max }
subscription-expires-infinite = ⏳ Unbefristetes Abonnement
subscription-expires-until = ⏳ Abonnement endet am: { $expires } (UTC+0)
subscription-purchase-success = ✅ Abonnement erfolgreich abgeschlossen! Vielen Dank für deinen Kauf.
welcome-text = 📢 Möchtest du als Erster erfahren, wenn der Preis steigt oder fällt? Wähle eine Coin, setze einen Schwellenwert, und unser Bot benachrichtigt dich, sobald der Preis dein Ziel erreicht! 🚀
select-action = Wähle eine Aktion:
subscription-plans = Abonnementpläne:
plan-basic-description = Basic – maximal { $limit } Coins
plan-standard-description = Standard – maximal { $limit } Coins
plan-premium-description = Premium – maximal { $limit } Coins
subscription-validity-period = Abonnementdauer: 30 Tage
subscription-already-active = ❌ Du hast bereits ein aktives Abonnement "{ $plan }" bis { $expires }. Du kannst kein neues kaufen, solange das aktuelle nicht abläuft.
subscription-already-active-db = ❌ Du hast bereits ein aktives Abonnement "{ $plan }" bis { $expires }. Du kannst kein neues kaufen, solange das aktuelle nicht abläuft.
price-star = { $price } ⭐
#btn
btn-all-rates = 📊 Alle Coin-Kurse
btn-choose-currency = 💎 Coin wählen
btn-set-alert = ⏰ Benachrichtigungen einstellen
btn-subscription = 📜 Abonnement
btn-help = ❓ Hilfe
btn-basic = 💳 Basic kaufen
btn-standard = 💎 Standard kaufen
btn-premium = 👑 Premium kaufen
btn-back = ⬅️ Zurück
button-enable-alerts = 🔔 Benachrichtigungen aktivieren
button-disable-alerts = 🔕 Benachrichtigungen deaktivieren
button-set-threshold-usd = 💲 Schwellenwert in $ setzen
button-set-threshold-rub = 💲 Schwellenwert in ₽ setzen
button-set-threshold-above = 📈 oberen Schwellenwert setzen
button-set-threshold-below = 📉 unteren Schwellenwert setzen
btn-toggle-currency = 🔄 In { $currency } anzeigen
button-choose-usd = 💵 In Dollar (USD)
button-choose-rub = 💰 In Rubel (RUB)
btn-set-new-threshold = 📝 Neuen Schwellenwert setzen
btn-my-currencies = 🎯 Meine Coins
#help
help-text = 👋 Hallo! Dies ist der Hilfebereich.
help-how-to-use = 🔍 Wie benutzt man den Bot?
help-get-rates = 📌 1. Kursinformationen abrufen.
help-get-rates-desc = Drücke den Button «📊 Alle Coin-Kurse». Der Bot zeigt den aktuellen Kurs aller verfügbaren Coins an.
help-add-currency = 📌 2. Einen Coin zur Beobachtungsliste hinzufügen.
help-add-currency-desc = Drücke den Button «📈 Coin wählen». Wähle einen Coin aus und drücke dann «⭐ Hinzufügen», um Preisänderungen zu verfolgen. Je nach Abonnement kannst du 1 bis 20 Coins gleichzeitig beobachten.
help-set-alert = 📌 3. Benachrichtigungen zum Kurs einstellen.
help-set-alert-desc = Drücke «⏰ Benachrichtigungen einstellen» und wähle einen Coin aus deiner Beobachtungsliste. Gib einen Preisschwellenwert an (z.B. Bitcoin > $50.000). Der Bot benachrichtigt dich, wenn der Kurs diesen Wert erreicht.
help-manage-subscription = 📌 4. Abonnement verwalten.
help-manage-subscription-desc = Im Bereich «📜 Abonnement» kannst du:
  - Deinen aktuellen Tarif und die Limits einsehen.
  - Ein neues Abonnement mit Telegram Stars kaufen.
  - Die Laufzeit deines Abonnements überprüfen.
  - Nach dem Kauf werden die Coin-Limits automatisch aktualisiert.
help-commands = 📌 5. Hauptbefehle:
help-commands-list = 
  /start — Hauptmenü
  /help — Hilfe
  /subscription — Abonnement verwalten
help-support = ✉️ Support: @SupportBot
#rate
rates-header = 📊 Aktuelle Kryptowährungskurse:
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Aktualisiert: { $time } (UTC+0)
dollar-rate = Dollar-Kurs: { $price } ₽
show-in-rub = in Rubel
show-in-usd = in Dollar
rates-error = ❌ Beim Abrufen der Kurse ist ein Fehler aufgetreten. Bitte versuche es später erneut.
# Commands
cmd-start = Bot starten
cmd-help = Hilfe
cmd-subscription = Abonnement verwalten
my-currencies-empty = ⚠️ Du hast noch keine Coins ausgewählt
alerts-no-currencies = ⚠️ Du verfolgst keine Coins. Füge Coins im Bereich "Meine Coins" hinzu.
subscription-limit-reached = ⚠️ Du hast das Limit der verfolgten Coins für dein Abonnement erreicht! Um weitere Coins hinzuzufügen, ist ein anderer Abonnementtyp erforderlich.
currency-added = ✅ Coin {$currency} wurde zur Verfolgung hinzugefügt
currency-removed = ❌ Coin {$currency} wurde aus der Verfolgung entfernt
choose-currency-instruction = Wähle die Coins zur Verfolgung aus:
✅ - Coin wird verfolgt
☑️ - Coin wird nicht verfolgt
# alerts
alerts-list-header = 🔔 Benachrichtigungseinstellungen für { $currency }
alerts-choose-currency = Wähle einen Coin zur Einrichtung der Benachrichtigungen:
alerts-error = ❌ Ein Fehler ist aufgetreten. Bitte versuche es später erneut.
alerts-current-price = Aktueller Preis:
alerts-current-price-both = Aktueller Preis: { $price_usd } $ / { $price_rub } ₽
alerts-current-settings = Aktuelle Einstellungen:
alerts-notifications-enabled = ✅ Benachrichtigungen aktiviert
alerts-notifications-disabled = ❌ Benachrichtigungen deaktiviert
alerts-usd-header = Schwellenwerte (USD):
alerts-rub-header = Schwellenwerte (RUB):
alerts-not-set = nicht festgelegt
alerts-threshold-above = ⬆️ Höher als
alerts-threshold-below = ⬇️ Niedriger als
alerts-disabled-successfully = ✅ Benachrichtigungen wurden erfolgreich deaktiviert
alert-details = Coin: { $currency }
alerts-no-thresholds = ℹ️ Um Benachrichtigungen zu aktivieren, lege zunächst Schwellenwerte fest!
no-alerts-to-disable = ⚠️ Es gibt keine aktiven Benachrichtigungen zum Deaktivieren
alert-added-successfully = ✅ Benachrichtigung erfolgreich hinzugefügt!
alert-updated-successfully = ✅ Benachrichtigung erfolgreich aktualisiert!
alert-price = Preis
alert-price-above = ⬆️ hat überschritten
alert-price-below = ⬇️ ist gefallen unter
alert-not-found = ⚠️ Benachrichtigung nicht gefunden
error-invalid-alert = ❌ Fehler: Ungültige Benachrichtigungs-ID
alerts-enter-threshold-above-usd = Gib den oberen Preisschwellenwert in USD ein:
alerts-enter-threshold-below-usd = Gib den unteren Preisschwellenwert in USD ein:
alerts-enter-threshold-above-rub = Gib den oberen Preisschwellenwert in RUB ein:
alerts-enter-threshold-below-rub = Gib den unteren Preisschwellenwert in RUB ein:
# Threshold Settings
select-currency-type = 💵 Wähle die Währung für den Schwellenwert:
select-condition = Wähle die Bedingung für die Benachrichtigung:
enter-threshold-value = Gib den Schwellenwert ein:
invalid-threshold-value = ❌ Ungültiger Wert. Bitte gib eine positive Zahl ein.
enter-new-threshold = Gib einen neuen Schwellenwert für { $currency } in { $currency_type } ein:
# Errors
error-occurred = ❌ Es ist ein Fehler aufgetreten. Bitte versuche es später erneut.
currency-not-found = ❌ Coin nicht gefunden.
rate-not-found = ❌ Konnte den Kurs der Währung nicht abrufen.
alerts-invalid-number = ❌ Bitte gib eine gültige Zahl ein