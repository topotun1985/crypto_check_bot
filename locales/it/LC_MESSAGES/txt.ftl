hello-user = 👋 Ciao, { $username }!
subscription-info = 📜 Il tuo abbonamento: { $plan }
subscription-currencies = 💰 Monete selezionate per il monitoraggio: { $current }/{ $max }
subscription-expires-infinite = ⏳ Abbonamento a tempo indeterminato
subscription-expires-until = ⏳ Scadenza dell'abbonamento: { $expires } (UTC+0)
subscription-purchase-success = ✅ Abbonamento attivato con successo! Grazie per il tuo acquisto.
welcome-text = 📢 Vuoi essere il primo a sapere quando il prezzo sale o scende? Scegli una moneta, imposta una soglia e il nostro bot ti notificherà quando il prezzo raggiungerà il livello desiderato! 🚀
select-action = Scegli un'azione:
subscription-plans = Piani di abbonamento:
plan-basic-description = Basico — fino a { $limit } monete
plan-standard-description = Standard — fino a { $limit } monete
plan-premium-description = Premium — fino a { $limit } monete
subscription-validity-period = Durata dell'abbonamento: 30 giorni
subscription-already-active = ❌ Hai già un abbonamento attivo "{ $plan }" fino al { $expires }. Non puoi acquistare un nuovo abbonamento finché quello attuale non scade.
subscription-already-active-db = ❌ Hai già un abbonamento attivo "{ $plan }" fino al { $expires }. Non puoi acquistare un nuovo abbonamento finché quello attuale non scade.
price-star = { $price } ⭐
#btn
btn-all-rates = 📊 Tutti i tassi delle monete
btn-choose-currency = 💎 Scegli una moneta
btn-set-alert = ⏰ Imposta le notifiche
btn-subscription = 📜 Abbonamento
btn-help = ❓ Aiuto
btn-basic = 💳 Acquista il piano Basico
btn-standard = 💎 Acquista il piano Standard
btn-premium = 👑 Acquista il piano Premium
btn-back = ⬅️ Indietro
button-enable-alerts = 🔔 Attiva le notifiche
button-disable-alerts = 🔕 Disattiva le notifiche
button-set-threshold-usd = 💲 Imposta soglia in $
button-set-threshold-rub = 💲 Imposta soglia in ₽
button-set-threshold-above = 📈 imposta soglia superiore
button-set-threshold-below = 📉 imposta soglia inferiore
btn-toggle-currency = 🔄 Mostra in { $currency }
button-choose-usd = 💵 In dollari (USD)
button-choose-rub = 💰 In rubli (RUB)
btn-set-new-threshold = 📝 Imposta una nuova soglia
btn-my-currencies = 🎯 Le mie monete
#help
help-text = 👋 Ciao! Questa è la sezione di aiuto.
help-how-to-use = 🔍 Come usare il bot?
help-get-rates = 📌 1. Ottieni informazioni sui tassi.
help-get-rates-desc = Premi il pulsante «📊 Tutti i tassi delle monete». Il bot mostrerà il tasso attuale di tutte le monete disponibili.
help-add-currency = 📌 2. Aggiungi una moneta alla lista di monitoraggio.
help-add-currency-desc = Premi il pulsante «📈 Scegli una moneta». Al momento della selezione, premi «⭐ Aggiungi» per monitorare le variazioni di prezzo. A seconda del tuo abbonamento, puoi monitorare da 1 a 20 monete contemporaneamente.
help-set-alert = 📌 3. Imposta le notifiche sul tasso.
help-set-alert-desc = Premi «⏰ Imposta le notifiche» e scegli una moneta dalla lista di monitoraggio. Inserisci il valore soglia (ad esempio, Bitcoin > $50,000). Il bot ti notificherà quando il tasso raggiungerà il valore indicato.
help-manage-subscription = 📌 4. Gestisci l'abbonamento.
help-manage-subscription-desc = Nella sezione «📜 Abbonamento» puoi:
  - Visualizzare il piano attuale e i limiti.
  - Acquistare un nuovo abbonamento con Telegram Stars.
  - Verificare la scadenza dell'abbonamento.
  - Dopo l'acquisto, i limiti delle monete si aggiornano automaticamente.
help-commands = 📌 5. Comandi principali:
help-commands-list = 
  /start — Menu principale
  /help — Aiuto
  /subscription — Gestisci abbonamento
help-support = ✉️ Assistenza: @SupportBot
#rate
rates-header = 📊 Tassi attuali delle criptovalute:
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Aggiornato: { $time } (UTC+0)
dollar-rate = Tasso del dollaro: { $price } ₽
show-in-rub = in rubli
show-in-usd = in dollari
rates-error = ❌ Si è verificato un errore durante il recupero dei tassi. Per favore, riprova più tardi.
# Commands
cmd-start = Avvia il bot
cmd-help = Aiuto
cmd-subscription = Gestisci abbonamento
my-currencies-empty = ⚠️ Non hai ancora selezionato alcuna moneta
alerts-no-currencies = ⚠️ Non hai monete monitorate. Aggiungi monete nella sezione "Le mie monete".
subscription-limit-reached = ⚠️ Hai raggiunto il limite di monete monitorate per il tuo abbonamento! Per aggiungerne di più è necessario un piano di abbonamento diverso.
currency-added = ✅ La moneta {$currency} è stata aggiunta al monitoraggio
currency-removed = ❌ La moneta {$currency} è stata rimossa dal monitoraggio
choose-currency-instruction = Scegli le monete da monitorare:
✅ - moneta monitorata
☑️ - moneta non monitorata
# alerts
alerts-list-header = 🔔 Impostazioni delle notifiche per { $currency }
alerts-choose-currency = Scegli una moneta per configurare le notifiche:
alerts-error = ❌ Si è verificato un errore. Per favore, riprova più tardi.
alerts-current-price = Prezzo attuale:
alerts-current-price-both = Prezzo attuale: { $price_usd } $ / { $price_rub } ₽
alerts-current-settings = Impostazioni attuali:
alerts-notifications-enabled = ✅ Notifiche attive
alerts-notifications-disabled = ❌ Notifiche disattivate
alerts-usd-header = Soglie (USD):
alerts-rub-header = Soglie (RUB):
alerts-not-set = non impostato
alerts-threshold-above = ⬆️ Superiore a
alerts-threshold-below = ⬇️ Inferiore a
alerts-disabled-successfully = ✅ Notifiche disattivate con successo
alert-details = Moneta: { $currency }
alerts-no-thresholds = ℹ️ Per attivare le notifiche, imposta prima le soglie!
no-alerts-to-disable = ⚠️ Nessuna notifica attiva da disattivare
alert-added-successfully = ✅ Notifica aggiunta con successo!
alert-updated-successfully = ✅ Notifica aggiornata con successo!
alert-price = Prezzo
alert-price-above = ⬆️ ha superato
alert-price-below = ⬇️ è scesa sotto
alert-not-found = ⚠️ Notifica non trovata
error-invalid-alert = ❌ Errore: ID notifica non valido
alerts-enter-threshold-above-usd = Inserisci la soglia superiore in USD:
alerts-enter-threshold-below-usd = Inserisci la soglia inferiore in USD:
alerts-enter-threshold-above-rub = Inserisci la soglia superiore in RUB:
alerts-enter-threshold-below-rub = Inserisci la soglia inferiore in RUB:
# Threshold Settings
select-currency-type = 💵 Scegli la valuta per la soglia:
select-condition = Scegli la condizione per la notifica:
enter-threshold-value = Inserisci il valore soglia:
invalid-threshold-value = ❌ Valore non valido. Inserisci un numero positivo.
enter-new-threshold = Inserisci una nuova soglia per { $currency } in { $currency_type }:
# Errors
error-occurred = ❌ Si è verificato un errore. Per favore, riprova più tardi.
currency-not-found = ❌ Moneta non trovata.
rate-not-found = ❌ Impossibile ottenere il tasso della moneta.
alerts-invalid-number = ❌ Inserisci un numero valido
error-threshold-must-be-positive = ❌ Il valore deve essere maggiore di 0
error-threshold-invalid-format = ❌ Formato del numero non valido. Usa il punto come separatore decimale (esempio: 1.23)
error-threshold-too-many-decimals-small = ❌ Troppi decimali: { $decimals }\nPer i numeri inferiori a 1 sono ammessi al massimo 5 cifre decimali\nEsempio: 0.00123
error-threshold-too-many-decimals-large = ❌ Troppi decimali: { $decimals }\nPer i numeri maggiori o uguali a 1 sono ammessi al massimo 2 cifre decimali\nEsempi: 1.23, 10.5, 100.00
error-threshold-generic = ❌ Inserisci un numero valido\nEsempi:\n- Numeri interi: 1, 10, 100\n- Con il punto: 1.23, 0.0012