hello-user = 👋 Ciao, { $username }!
default-username = Amico
subscription-info = 💳 Il tuo abbonamento: { $plan }
subscription-currencies = 💰 Monete selezionate per il monitoraggio: { $current }/{ $max }
subscription-expires-infinite = ⏳ Abbonamento illimitato
subscription-expires-until = ⏳ Data di scadenza dell'abbonamento: { $expires } (UTC+0)
subscription-purchase-success = ✅ Abbonamento attivato con successo! Grazie per il tuo acquisto.
subscription-terms-link = Consulta i termini prima del pagamento: /subscription_terms
welcome-text = 📢 Vuoi essere il primo a sapere quando il prezzo sale o scende? Scegli una moneta, imposta una soglia, e il nostro bot ti notificherà quando il prezzo raggiungerà il livello desiderato! 🚀
select-action = Scegli un'azione:
subscription-plans = Piani di abbonamento:
plan-basic-description = Basic — fino a { $limit } monete
plan-standard-description = Standard — fino a { $limit } monete
plan-premium-description = Premium — fino a { $limit } monete
subscription-validity-period = Durata dell'abbonamento: 30 giorni
subscription-already-active = ❌ Hai già un abbonamento attivo "{ $plan }" fino al { $expires }. Non puoi acquistare un nuovo abbonamento finché quello attuale non scade.
subscription-already-active-db = ❌ Hai già un abbonamento attivo "{ $plan }" fino al { $expires }. Non puoi acquistare un nuovo abbonamento finché quello attuale non scade.
price-star = { $price } ⭐
#payment
subscription-payment-button = Invia { $price } ⭐️
subscription-invoice-title = Abbonamento { $plan }
subscription-invoice-description = Sottoscrivi { $plan } per 30 giorni
subscription-price-label = Abbonamento { $plan }
#btn
btn-all-rates = 📊 Tutti i tassi delle monete
btn-choose-currency = 🪙 Scegli la moneta
btn-set-alert = 🔔 Configura le notifiche
btn-subscription = 💳 Abbonamento
btn-help = ❓ Aiuto
btn-basic = 🔰 Acquista Basic
btn-standard = 💎 Acquista Standard
btn-premium = 👑 Acquista Premium
btn-back = ⬅️ Indietro
button-enable-alerts = 🔔 Attiva le notifiche
button-disable-alerts = 🔕 Disattiva le notifiche
button-set-threshold-usd = 💲 Imposta la soglia in $
button-set-threshold-rub = 💲 Imposta la soglia in ₽
button-set-threshold-above = 📈 Imposta la soglia superiore
button-set-threshold-below = 📉 Imposta la soglia inferiore
btn-toggle-currency = 🔄 Mostra in { $currency }
button-choose-usd = 💵 In dollari (USD)
button-choose-rub = 💰 In rubli (RUB)
btn-set-new-threshold = 📝 Imposta una nuova soglia
btn-my-currencies = 🎯 Le mie monete
#help
help-text = 👋 Ciao! Questa è la sezione di aiuto
help-how-to-use = 🔍 Come usare il bot?
help-get-rates = 📌 1. Ottenere informazioni sui tassi.
help-get-rates-desc = Premi il pulsante «📊 Tutti i tassi delle monete». Il bot mostrerà il tasso attuale di tutte le monete disponibili.
help-my-currencies = 📌 2. 🎯 Le mie monete.
help-my-currencies-desc = Nella sezione «🎯 Le mie monete» puoi:
  - Visualizzare tutte le monete monitorate
  - Controllare i tassi attuali
help-add-currency = 📌 3. Aggiungere una moneta alla lista di monitoraggio.
help-add-currency-desc = Premi il pulsante «🪙 Scegli la moneta». Seleziona una moneta e tocca «☑️ Moneta» per monitorarne le variazioni di prezzo. A seconda dell'abbonamento, puoi monitorare da 1 a 10 monete contemporaneamente.
help-set-alert = 📌 4. Configurare le notifiche sui tassi.
help-set-alert-desc = Premi «🔔 Configura le notifiche» e scegli una moneta dalla lista di monitoraggio. Inserisci un valore limite per il prezzo (ad es., limite superiore per Bitcoin 99000$). Il bot invierà una notifica quando il tasso raggiungerà il valore specificato.
help-manage-subscription = 📌 5. Gestire l'abbonamento.
help-manage-subscription-desc = Nella sezione «💳 Abbonamento» puoi:
  - Conoscere il piano attuale e i limiti.
  - Acquistare un nuovo abbonamento con Telegram Stars.
  - Visualizzare la validità dell'abbonamento.
  - Dopo l'acquisto, i limiti delle monete vengono aggiornati automaticamente.
help-commands = 📌 6. Comandi principali:
help-commands-list = 
  /start — Menu principale
  /help — Aiuto
  /subscription — Gestire l'abbonamento
  /subscription_terms — Termini di abbonamento
  /support — Supporto
help-support = ✉️ Supporto: pricealertprobot@outlook.com
#rate
rates-header = 📊 Tassi attuali delle criptovalute:
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Aggiornato: { $time } (UTC+0)
dollar-rate = Tasso del dollaro: { $price } ₽
show-in-rub = in rubli
show-in-usd = in dollari
rates-error = ❌ Si è verificato un errore nel recupero dei tassi. Per favore riprova più tardi.
# Commands
cmd-start = Avvia il bot
cmd-help = Aiuto
cmd-subscription = Gestisci abbonamento
cmd-subscription-terms = Termini di abbonamento
cmd-support = Supporto
my-currencies-empty = ⚠️ Non hai ancora selezionato alcuna moneta
alerts-no-currencies = ⚠️ Non hai monete monitorate. Aggiungi monete nella sezione "Le mie monete".
subscription-limit-reached = ⚠️ Hai raggiunto il limite di monete monitorate per il tuo abbonamento! Per aggiungere altre monete è necessario un tipo di abbonamento diverso.
currency-added = ✅ La moneta {$currency} è stata aggiunta al monitoraggio
currency-removed = ❌ La moneta {$currency} è stata rimossa dal monitoraggio
choose-currency-instruction = Seleziona le monete da monitorare:
✅ - moneta monitorata
☑️ - moneta non monitorata
# alerts
alerts-list-header = 🔔 Impostazioni delle notifiche per ❨{$currency}❩
alerts-choose-currency = Seleziona una moneta per configurare le notifiche:
alerts-error = ❌ Si è verificato un errore. Per favore riprova più tardi.
alerts-current-price = Prezzo attuale:
alerts-current-price-both = Prezzo attuale: {$price_usd} $ / {$price_rub} ₽
alerts-current-settings = Impostazioni attuali:
alerts-notifications-enabled = ✅ Notifiche attivate
alerts-notifications-disabled = ❌ Notifiche disattivate
alerts-usd-header = Soglie (USD):
alerts-rub-header = Soglie (RUB):
alerts-not-set = non impostato
alerts-threshold-above = ⬆️ Sopra
alerts-threshold-below = ⬇️ Sotto
alerts-disabled-successfully = ✅ Notifiche disattivate con successo
alert-details = Moneta: {$currency}
alerts-no-thresholds = ℹ️ Per attivare le notifiche, imposta prima le soglie!
no-alerts-to-disable = ⚠️ Nessuna notifica attiva da disattivare
alert-added-successfully = ✅ Notifica aggiunta con successo!
alert-updated-successfully = ✅ Notifica aggiornata con successo!
alert-price = Prezzo
alert-price-above = ⬆️ ha superato
alert-price-below = ⬇️ è scesa sotto
alert-not-found = ⚠️ Notifica non trovata
error-invalid-alert = ❌ Errore: ID notifica non valido
alerts-enter-threshold-above-usd = Inserisci la soglia superiore del prezzo in USD:
alerts-enter-threshold-below-usd = Inserisci la soglia inferiore del prezzo in USD:
alerts-enter-threshold-above-rub = Inserisci la soglia superiore del prezzo in rubli:
alerts-enter-threshold-below-rub = Inserisci la soglia inferiore del prezzo in rubli:
# Threshold Settings
select-currency-type = 💵 Seleziona la valuta per la soglia:
select-condition = Seleziona la condizione per la notifica:
enter-threshold-value = Inserisci il valore soglia:
invalid-threshold-value = ❌ Valore non valido. Inserisci un numero positivo.
enter-new-threshold = Inserisci il nuovo valore soglia per { $currency } in { $currency_type }:
# Errors
error-occurred = ❌ Si è verificato un errore. Per favore, riprova più tardi.
currency-not-found = ❌ Valuta non trovata.
rate-not-found = ❌ Non è stato possibile ottenere il tasso della valuta.
alerts-invalid-number = ❌ Per favore, inserisci un numero valido
error-threshold-must-be-positive = ❌ Il valore deve essere maggiore di 0
error-threshold-invalid-format = ❌ Formato del numero non valido. Usa il punto come separatore (esempio: 1.23)
error-threshold-too-many-decimals-small = ❌ Troppe cifre decimali: { $decimals }
                                          Per i numeri inferiori a 1 è consentito al massimo 5 cifre decimali
                                          Esempio: 0.00123
error-threshold-too-many-decimals-large = ❌ Troppe cifre decimali: { $decimals }
                                          Per i numeri maggiori o uguali a 1 è consentito al massimo 2 cifre decimali
                                          Esempi: 1.23, 10.5, 100.00
error-threshold-generic = ❌ Inserisci un numero valido
                          Esempi:
                          - Numeri interi: 1, 10, 100
                          - Con decimali: 1.23, 0.0012
error-threshold-too-large = ❌ Valore troppo elevato. Il valore massimo consentito è 999999999
unsupported-text-message = Mi dispiace, non capisco il testo. Per favore, usa i comandi del bot o i pulsanti del menu.
unsupported-photo = Mi dispiace, non elaboro le foto. Per favore, usa i comandi del bot o i pulsanti del menu.
unsupported-sticker = Mi dispiace, non elaboro gli sticker. Per favore, usa i comandi del bot o i pulsanti del menu.
unsupported-document = Mi dispiace, non elaboro i documenti. Per favore, usa i comandi del bot o i pulsanti del menu.
unsupported-voice = Mi dispiace, non elaboro i messaggi vocali. Per favore, usa i comandi del bot o i pulsanti del menu.
unsupported-video = Mi dispiace, non elaboro i video. Per favore, usa i comandi del bot o i pulsanti del menu.
unsupported-message = Mi dispiace, questo tipo di messaggio non è supportato. Per favore, usa i comandi del bot o i pulsanti del menu.
subscription-terms-text = 
      📄 Termini di abbonamento

      1. Abbonamento gratuito (Free)
      📊 Disponibile: 1 moneta per il monitoraggio.
      🔄 Flessibilità: Puoi cambiare la moneta selezionata in qualsiasi momento.
      💡 Raccomandazione: Ti consigliamo di iniziare con la versione gratuita per valutare le funzionalità del bot.

      2. Abbonamenti a pagamento
      Basic (200 Stars):
      📈 Monitoraggio: Fino a { $basic_limit } monete.
      ⏳ Durata: 30 giorni.

      Standard (300 Stars):
      📈 Monitoraggio: Fino a { $standard_limit } monete.
      ⏳ Durata: 30 giorni.
      
      Premium (400 Stars):
      📈 Monitoraggio: Fino a { $premium_limit } monete.
      ⏳ Durata: 30 giorni.

      3. Condizioni importanti
      ❗ Nessun rimborso: Non viene effettuato alcun rimborso dopo l'acquisto dell'abbonamento.
      🔄 Modifica del piano: Il tipo di abbonamento a pagamento può essere modificato solo dopo la scadenza dell'abbonamento corrente (ad esempio, passare da Premium a Standard).
      ⛔ Rinnovo manuale: Gli abbonamenti non si rinnovano automaticamente — il pagamento viene effettuato manualmente.
      💎 Utilizzo di Telegram Stars: Telegram Stars vengono utilizzati esclusivamente per servizi digitali (è vietata la vendita di prodotti fisici).

      4. Raccomandazioni
      🚀 Test: Prima di acquistare un abbonamento a pagamento, ti consigliamo di utilizzare la versione gratuita per assicurarti che le funzionalità del bot soddisfino le tue esigenze.
      ⚠️ Scelta attenta: Scegli il tuo piano con cura, poiché non potrà essere modificato dopo l'acquisto.
      Clausola legale:
      Acquistando un abbonamento, accetti questi termini. Tutti gli abbonamenti sono definitivi, non viene effettuato alcun rimborso. Il bot fornisce esclusivamente servizi digitali e non è responsabile per eventuali perdite derivanti dall'utilizzo del servizio.
cmd-support-text =
      🛠 Supporto

      Se hai domande, problemi con il pagamento o con le funzionalità del bot, scrivici:
      ✉️ pricealertprobot@outlook.com

      ⏰ Orari di supporto:
      Il nostro servizio di supporto è attivo dalle 12:00 alle 21:00 (UTC+0).

      ❗ Importante:
      🚀 Test: Prima di acquistare un abbonamento a pagamento, ti consigliamo di utilizzare la versione gratuita per assicurarti che le funzionalità del bot soddisfino le tue esigenze.
      ⚠️ Scelta attenta: Scegli il tuo piano con cura, poiché non potrà essere modificato dopo l'acquisto.
      
      Clausola legale:
      Tutti gli abbonamenti sono definitivi, non viene effettuato alcun rimborso. Il bot fornisce esclusivamente servizi digitali e non è responsabile per eventuali perdite derivanti dall'utilizzo del servizio. (vedi «Termini di abbonamento»).
      
      Nota: i tempi di risposta possono variare.