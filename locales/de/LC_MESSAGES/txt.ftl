hello-user = 👋 Hallo, { $username }!
default-username = Freund
subscription-info = 💳 Ihr Abonnement: { $plan }
subscription-currencies = 💰 Ausgewählte Coins für das Tracking: { $current }/{ $max }
subscription-expires-infinite = ⏳ Unbefristetes Abonnement
subscription-expires-until = ⏳ Ablaufdatum des Abonnements: { $expires } (UTC+0)
subscription-purchase-success = ✅ Abonnement erfolgreich abgeschlossen! Vielen Dank für Ihren Kauf.
subscription-terms-link = Bitte lesen Sie die Bedingungen vor der Zahlung: /subscription_terms
welcome-text = 📢 Möchten Sie als Erster erfahren, wenn der Preis steigt oder fällt? Wählen Sie eine Münze, setzen Sie einen Schwellenwert, und unser Bot benachrichtigt Sie, sobald der Preis den gewünschten Wert erreicht! 🚀
select-action = Wählen Sie eine Aktion:
subscription-plans = Abonnement-Pläne:
plan-basic-description = Basic — maximal { $limit } Münzen
plan-standard-description = Standard — maximal { $limit } Münzen
plan-premium-description = Premium — maximal { $limit } Münzen
subscription-validity-period = Abonnementdauer: 30 Tage
subscription-already-active = ❌ Sie haben bereits ein aktives Abonnement „{ $plan }“ bis zum { $expires }. Sie können kein neues kaufen, bevor das aktuelle abläuft.
subscription-already-active-db = ❌ Sie haben bereits ein aktives Abonnement „{ $plan }“ bis zum { $expires }. Sie können kein neues kaufen, bevor das aktuelle abläuft.
price-star = { $price } ⭐
#payment
subscription-payment-button = Senden Sie { $price } ⭐️
subscription-invoice-title = Abonnement { $plan }
subscription-invoice-description = Abonnieren Sie { $plan } für 30 Tage
subscription-price-label = Abonnement { $plan }
#btn
btn-all-rates = 📊 Alle Coin-Kurse
btn-choose-currency = 🪙 Münze auswählen
btn-set-alert = 🔔 Benachrichtigungen einstellen
btn-subscription = 💳 Abonnement
btn-help = ❓ Hilfe
btn-basic = 🔰 Basic kaufen
btn-standard = 💎 Standard kaufen
btn-premium = 👑 Premium kaufen
btn-back = ⬅️ Zurück
button-enable-alerts = 🔔 Benachrichtigungen aktivieren
button-disable-alerts = 🔕 Benachrichtigungen deaktivieren
button-set-threshold-usd = 💲 Schwellenwert in $ festlegen
button-set-threshold-rub = 💲 Schwellenwert in ₽ festlegen
button-set-threshold-above = 📈 Oberen Schwellenwert festlegen
button-set-threshold-below = 📉 Unteren Schwellenwert festlegen
btn-toggle-currency = 🔄 In { $currency } anzeigen
button-choose-usd = 💵 In US-Dollar (USD)
button-choose-rub = 💰 In Rubel (RUB)
btn-set-new-threshold = 📝 Neuen Schwellenwert festlegen
btn-my-currencies = 🎯 Meine Münzen
#help
help-text = 👋 Hallo! Dies ist der Hilfebereich.
help-how-to-use = 🔍 Wie benutzt man den Bot?
help-get-rates = 📌 1. Informationen zu den Kursen abrufen.
help-get-rates-desc = Drücken Sie den Button «📊 Alle Coin-Kurse». Der Bot zeigt den aktuellen Kurs aller verfügbaren Coins an.
help-add-currency = 📌 2. Eine Münze zur Überwachungsliste hinzufügen.
help-add-currency-desc = Drücken Sie den Button «🪙 Münze auswählen». Wählen Sie eine Münze aus und tippen Sie auf «☑️ Münze», um Preisänderungen zu überwachen. Je nach Abonnement können Sie 1 bis 10 Münzen gleichzeitig überwachen.
help-set-alert = 📌 3. Kursbenachrichtigungen einrichten.
help-set-alert-desc = Drücken Sie «🔔 Benachrichtigungen einstellen» und wählen Sie eine Münze aus der Überwachungsliste. Geben Sie den Schwellenwert ein (z. B. obere Grenze für Bitcoin 99000$). Der Bot sendet eine Benachrichtigung, sobald der Kurs den angegebenen Wert erreicht.
help-manage-subscription = 📌 4. Abonnement verwalten.
help-manage-subscription-desc = Im Bereich «💳 Abonnement» können Sie:
  - Den aktuellen Tarif und die Limits abrufen.
  - Ein neues Abonnement mit Telegram Stars kaufen.
  - Die Gültigkeitsdauer des Abonnements einsehen.
  - Nach dem Kauf wird das Münzlimit automatisch aktualisiert.
help-commands = 📌 5. Hauptbefehle:
help-commands-list = 
  /start — Hauptmenü
  /help — Hilfe
  /subscription — Abonnement verwalten
  /subscription_terms — Abonnement-Bedingungen
  /support — Support
help-support = ✉️ Support: pricealertprobot@outlook.com
#rate
rates-header = 📊 Aktuelle Kryptowährungskurse:
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Aktualisiert: { $time } (UTC+0)
dollar-rate = Kurs des Dollars: { $price } ₽
show-in-rub = in Rubel
show-in-usd = in Dollar
rates-error = ❌ Beim Abrufen der Kurse ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.
# Commands
cmd-start = Bot starten
cmd-help = Hilfe
cmd-subscription = Abonnement verwalten
cmd-subscription-terms = Abonnement-Bedingungen
cmd-support = Support
my-currencies-empty = ⚠️ Sie haben noch keine Münzen ausgewählt
alerts-no-currencies = ⚠️ Sie haben keine überwachten Münzen. Fügen Sie Münzen im Bereich "Meine Münzen" hinzu.
subscription-limit-reached = ⚠️ Sie haben das Limit der überwachten Münzen für Ihr Abonnement erreicht! Um weitere Münzen hinzuzufügen, ist ein anderer Abonnementtyp erforderlich.
currency-added = ✅ Münze {$currency} wurde zur Überwachung hinzugefügt
currency-removed = ❌ Münze {$currency} wurde aus der Überwachung entfernt
choose-currency-instruction = Wählen Sie die Münzen zur Überwachung aus:
✅ - Münze wird überwacht
☑️ - Münze wird nicht überwacht
# alerts
alerts-list-header = 🔔 Benachrichtigungseinstellungen für ❨{$currency}❩
alerts-choose-currency = Wählen Sie eine Münze zur Konfiguration der Benachrichtigungen aus:
alerts-error = ❌ Es ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.
alerts-current-price = Aktueller Preis:
alerts-current-price-both = Aktueller Preis: {$price_usd} $ / {$price_rub} ₽
alerts-current-settings = Aktuelle Einstellungen:
alerts-notifications-enabled = ✅ Benachrichtigungen aktiviert
alerts-notifications-disabled = ❌ Benachrichtigungen deaktiviert
alerts-usd-header = Schwellenwerte (USD):
alerts-rub-header = Schwellenwerte (RUB):
alerts-not-set = nicht festgelegt
alerts-threshold-above = ⬆️ Über
alerts-threshold-below = ⬇️ Unter
alerts-disabled-successfully = ✅ Benachrichtigungen erfolgreich deaktiviert
alert-details = Währung: {$currency}
alerts-no-thresholds = ℹ️ Um Benachrichtigungen zu aktivieren, legen Sie zunächst die Schwellenwerte fest!
no-alerts-to-disable = ⚠️ Es gibt keine aktiven Benachrichtigungen zum Deaktivieren
alert-added-successfully = ✅ Benachrichtigung erfolgreich hinzugefügt!
alert-updated-successfully = ✅ Benachrichtigung erfolgreich aktualisiert!
alert-price = Preis
alert-price-above = ⬆️ hat überschritten
alert-price-below = ⬇️ ist gefallen unter
alert-not-found = ⚠️ Benachrichtigung nicht gefunden
error-invalid-alert = ❌ Fehler: Ungültige Benachrichtigungs-ID
alerts-enter-threshold-above-usd = Geben Sie den oberen Schwellenwert des Preises in USD ein:
alerts-enter-threshold-below-usd = Geben Sie den unteren Schwellenwert des Preises in USD ein:
alerts-enter-threshold-above-rub = Geben Sie den oberen Schwellenwert des Preises in Rubel ein:
alerts-enter-threshold-below-rub = Geben Sie den unteren Schwellenwert des Preises in Rubel ein:
# Threshold Settings
select-currency-type = 💵 Wählen Sie die Währung für den Schwellenwert:
select-condition = Wählen Sie die Bedingung für die Benachrichtigung:
enter-threshold-value = Geben Sie den Schwellenwert ein:
invalid-threshold-value = ❌ Ungültiger Wert. Bitte geben Sie eine positive Zahl ein.
enter-new-threshold = Geben Sie einen neuen Schwellenwert für { $currency } in { $currency_type } ein:
# Errors
error-occurred = ❌ Es ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.
currency-not-found = ❌ Währung nicht gefunden.
rate-not-found = ❌ Der Kurs der Währung konnte nicht abgerufen werden.
alerts-invalid-number = ❌ Bitte geben Sie eine gültige Zahl ein
error-threshold-must-be-positive = ❌ Der Wert muss größer als 0 sein
error-threshold-invalid-format = ❌ Ungültiges Zahlenformat. Bitte verwenden Sie einen Punkt als Dezimaltrennzeichen (z. B.: 1.23)
error-threshold-too-many-decimals-small = ❌ Zu viele Nachkommastellen: { $decimals }
                                          Für Zahlen unter 1 sind maximal 5 Nachkommastellen zulässig
                                          Beispiel: 0.00123
error-threshold-too-many-decimals-large = ❌ Zu viele Nachkommastellen: { $decimals }
                                          Für Zahlen ab 1 sind maximal 2 Nachkommastellen zulässig
                                          Beispiele: 1.23, 10.5, 100.00
error-threshold-generic = ❌ Bitte geben Sie eine gültige Zahl ein
                          Beispiele:
                          - Ganze Zahlen: 1, 10, 100
                          - Mit Dezimalstellen: 1.23, 0.0012
error-threshold-too-large = ❌ Der Wert ist zu hoch. Der maximal zulässige Wert ist 999999999
unsupported-text-message = Entschuldigung, ich verstehe den Text nicht. Bitte verwenden Sie die Bot-Befehle oder die Menütasten.
unsupported-photo = Entschuldigung, ich verarbeite keine Fotos. Bitte verwenden Sie die Bot-Befehle oder die Menütasten.
unsupported-sticker = Entschuldigung, ich verarbeite keine Sticker. Bitte verwenden Sie die Bot-Befehle oder die Menütasten.
unsupported-document = Entschuldigung, ich verarbeite keine Dokumente. Bitte verwenden Sie die Bot-Befehle oder die Menütasten.
unsupported-voice = Entschuldigung, ich verarbeite keine Sprachnachrichten. Bitte verwenden Sie die Bot-Befehle oder die Menütasten.
unsupported-video = Entschuldigung, ich verarbeite keine Videos. Bitte verwenden Sie die Bot-Befehle oder die Menütasten.
unsupported-message = Entschuldigung, dieser Nachrichtentyp wird nicht unterstützt. Bitte verwenden Sie die Bot-Befehle oder die Menütasten.
subscription-terms-text = 
      📄 Abonnement-Bedingungen

      1. Kostenloses Abonnement (Free)
      📊 Verfügbar: 1 Münze zur Überwachung.
      🔄 Flexibilität: Sie können die ausgewählte Münze jederzeit ändern.
      💡 Empfehlung: Wir empfehlen, mit der kostenlosen Version zu beginnen, um die Funktionen des Bots zu testen.

      2. Kostenpflichtige Abonnements
      Basic (200 Stars):
      📈 Überwachung: Bis zu { $limit } Münzen.
      ⏳ Gültigkeit: 30 Tage.

      Standard (300 Stars):
      📈 Überwachung: Bis zu { $limit } Münzen.
      ⏳ Gültigkeit: 30 Tage.
      
      Premium (400 Stars):
      📈 Überwachung: Bis zu { $limit } Münzen.
      ⏳ Gültigkeit: 30 Tage.

      3. Wichtige Bedingungen
      ❗ Keine Rückerstattung: Nach dem Kauf des Abonnements erfolgt keine Rückerstattung.
      🔄 Tarifwechsel: Ein kostenpflichtiges Abonnement kann erst nach Ablauf des aktuellen Abonnements geändert werden (z. B. Wechsel von Premium zu Standard).
      ⛔ Manuelle Verlängerung: Abonnements verlängern sich nicht automatisch – die Zahlung erfolgt manuell.
      💎 Verwendung von Telegram Stars: Telegram Stars werden ausschließlich für digitale Dienstleistungen verwendet (der Verkauf physischer Waren ist untersagt).

      4. Empfehlungen
      🚀 Testphase: Bevor Sie ein kostenpflichtiges Abonnement erwerben, empfehlen wir, die kostenlose Version zu nutzen, um sicherzustellen, dass die Funktionen des Bots Ihren Bedürfnissen entsprechen.
      ⚠️ Sorgfältige Auswahl: Wählen Sie Ihren Tarif sorgfältig, da eine Änderung nach dem Kauf nicht möglich ist.
      Rechtlicher Hinweis:
      Mit dem Abschluss eines Abonnements stimmen Sie diesen Bedingungen zu. Alle Abonnements sind endgültig, Rückerstattungen erfolgen nicht. Der Bot bietet ausschließlich digitale Dienstleistungen und haftet nicht für etwaige Verluste, die aus der Nutzung des Dienstes entstehen.
cmd-support-text =
      🛠 Support

      Wenn Sie Fragen haben, Probleme mit der Zahlung oder den Funktionen des Bots auftreten, schreiben Sie uns: 
      ✉️ pricealertprobot@outlook.com

      ⏰ Supportzeiten: 
      Unser Support ist von 12:00 bis 21:00 (UTC+0) erreichbar.

      ❗ Wichtig:  
      🚀 Testphase: Bevor Sie ein kostenpflichtiges Abonnement erwerben, empfehlen wir, die kostenlose Version zu nutzen, um sicherzustellen, dass die Funktionen des Bots Ihren Bedürfnissen entsprechen.
      ⚠️ Sorgfältige Auswahl: Wählen Sie Ihren Tarif sorgfältig, da eine Änderung nach dem Kauf nicht möglich ist.
      
      Rechtlicher Hinweis:
      Alle Abonnements sind endgültig, Rückerstattungen erfolgen nicht. Der Bot bietet ausschließlich digitale Dienstleistungen und haftet nicht für etwaige Verluste, die aus der Nutzung des Dienstes entstehen. (Siehe „Abonnement-Bedingungen“).
      
      Hinweis: Die Antwortzeiten können variieren.