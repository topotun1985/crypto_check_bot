hello-user = 👋 ¡Hola, { $username }!
subscription-info = 📜 Tu suscripción: { $plan }
subscription-currencies = 💰 Monedas seleccionadas para seguimiento: { $current }/{ $max }
subscription-expires-infinite = ⏳ Suscripción indefinida
subscription-expires-until = ⏳ Fecha de expiración: { $expires } (UTC+0)
subscription-purchase-success = ✅ ¡Suscripción adquirida con éxito! Gracias por tu compra.
welcome-text = 📢 ¿Quieres ser de los primeros en saber cuándo sube o baja el precio? ¡Elige una moneda, establece un umbral y nuestro bot te notificará cuando el precio alcance el nivel deseado! 🚀
select-action = Elige una acción:
subscription-plans = Planes de suscripción:
plan-basic-description = Básico — hasta { $limit } monedas
plan-standard-description = Estándar — hasta { $limit } monedas
plan-premium-description = Premium — hasta { $limit } monedas
subscription-validity-period = Duración del abono: 30 días
subscription-already-active = ❌ Ya tienes una suscripción activa "{ $plan }" hasta { $expires }. No puedes comprar una nueva hasta que expire la actual.
subscription-already-active-db = ❌ Ya tienes una suscripción activa "{ $plan }" hasta { $expires }. No puedes comprar una nueva hasta que expire la actual.
price-star = { $price } ⭐
#btn
btn-all-rates = 📊 Todas las cotizaciones de las monedas
btn-choose-currency = 💎 Elegir moneda
btn-set-alert = ⏰ Configurar alertas
btn-subscription = 📜 Suscripción
btn-help = ❓ Ayuda
btn-basic = 💳 Comprar Básico
btn-standard = 💎 Comprar Estándar
btn-premium = 👑 Comprar Premium
btn-back = ⬅️ Atrás
button-enable-alerts = 🔔 Activar alertas
button-disable-alerts = 🔕 Desactivar alertas
button-set-threshold-usd = 💲 Establecer umbral en $
button-set-threshold-rub = 💲 Establecer umbral en ₽
button-set-threshold-above = 📈 establecer umbral superior
button-set-threshold-below = 📉 establecer umbral inferior
btn-toggle-currency = 🔄 Mostrar en { $currency }
button-choose-usd = 💵 En dólares (USD)
button-choose-rub = 💰 En rublos (RUB)
btn-set-new-threshold = 📝 Establecer nuevo umbral
btn-my-currencies = 🎯 Mis monedas
#help
help-text = 👋 ¡Hola! Esta es la sección de ayuda.
help-how-to-use = 🔍 ¿Cómo usar el bot?
help-get-rates = 📌 1. Obtener información sobre las cotizaciones.
help-get-rates-desc = Presiona el botón «📊 Todas las cotizaciones de las monedas». El bot mostrará la cotización actual de todas las monedas disponibles.
help-add-currency = 📌 2. Agregar una moneda a la lista de seguimiento.
help-add-currency-desc = Presiona el botón «📈 Elegir moneda». Al seleccionar una moneda, pulsa «⭐ Agregar» para seguir los cambios en su precio. Dependiendo de tu suscripción, puedes seguir de 1 a 20 monedas simultáneamente.
help-set-alert = 📌 3. Configurar alertas de cotización.
help-set-alert-desc = Presiona «⏰ Configurar alertas» y elige una moneda de la lista de seguimiento. Indica el umbral de precio (por ejemplo, Bitcoin > $50 000). El bot te notificará cuando la cotización alcance el valor indicado.
help-manage-subscription = 📌 4. Gestionar suscripción.
help-manage-subscription-desc = En la sección «📜 Suscripción» puedes:
  - Consultar tu plan actual y tus límites.
  - Comprar una nueva suscripción mediante Telegram Stars.
  - Ver la fecha de expiración de tu suscripción.
  - Tras la compra, los límites de monedas se actualizan automáticamente.
help-commands = 📌 5. Comandos principales:
help-commands-list = 
  /start — Menú principal
  /help — Ayuda
  /subscription — Gestionar suscripción
help-support = ✉️ Soporte: @SupportBot
#rate
rates-header = 📊 Cotizaciones actuales de criptomonedas:
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Actualizado: { $time } (UTC+0)
dollar-rate = Tasa del dólar: { $price } ₽
show-in-rub = en rublos
show-in-usd = en dólares
rates-error = ❌ Se produjo un error al obtener las cotizaciones. Por favor, inténtalo de nuevo más tarde.
# Commands
cmd-start = Iniciar bot
cmd-help = Ayuda
cmd-subscription = Gestionar suscripción
my-currencies-empty = ⚠️ Aún no has seleccionado ninguna moneda
alerts-no-currencies = ⚠️ No tienes monedas en seguimiento. Agrega monedas en la sección "Mis monedas".
subscription-limit-reached = ⚠️ Has alcanzado el límite de monedas en seguimiento para tu suscripción. Para agregar más monedas, se requiere otro tipo de suscripción.
currency-added = ✅ La moneda {$currency} ha sido agregada para seguimiento
currency-removed = ❌ La moneda {$currency} ha sido eliminada del seguimiento
choose-currency-instruction = Elige las monedas para seguimiento:
✅ - moneda en seguimiento
☑️ - moneda no en seguimiento
# alerts
alerts-list-header = 🔔 Configuración de alertas para { $currency }
alerts-choose-currency = Elige una moneda para configurar las alertas:
alerts-error = ❌ Se produjo un error. Por favor, inténtalo de nuevo más tarde.
alerts-current-price = Precio actual:
alerts-current-price-both = Precio actual: { $price_usd } $ / { $price_rub } ₽
alerts-current-settings = Configuración actual:
alerts-notifications-enabled = ✅ Alertas activadas
alerts-notifications-disabled = ❌ Alertas desactivadas
alerts-usd-header = Umbrales (USD):
alerts-rub-header = Umbrales (RUB):
alerts-not-set = no establecido
alerts-threshold-above = ⬆️ Superior a
alerts-threshold-below = ⬇️ Inferior a
alerts-disabled-successfully = ✅ Alertas desactivadas con éxito
alert-details = Moneda: { $currency }
alerts-no-thresholds = ℹ️ Para activar las alertas, primero establece los umbrales.
no-alerts-to-disable = ⚠️ No hay alertas activas para desactivar
alert-added-successfully = ✅ Alerta agregada con éxito!
alert-updated-successfully = ✅ Alerta actualizada con éxito!
alert-price = Precio
alert-price-above = ⬆️ superó
alert-price-below = ⬇️ cayó por debajo de
alert-not-found = ⚠️ Alerta no encontrada
error-invalid-alert = ❌ Error: ID de alerta inválido
alerts-enter-threshold-above-usd = Ingresa el umbral superior en USD:
alerts-enter-threshold-below-usd = Ingresa el umbral inferior en USD:
alerts-enter-threshold-above-rub = Ingresa el umbral superior en RUB:
alerts-enter-threshold-below-rub = Ingresa el umbral inferior en RUB:
# Threshold Settings
select-currency-type = 💵 Elige la moneda para el umbral:
select-condition = Elige la condición para la alerta:
enter-threshold-value = Ingresa el valor del umbral:
invalid-threshold-value = ❌ Valor incorrecto. Por favor, ingresa un número positivo.
enter-new-threshold = Ingresa un nuevo umbral para { $currency } en { $currency_type }:
# Errors
error-occurred = ❌ Se produjo un error. Por favor, inténtalo de nuevo más tarde.
currency-not-found = ❌ Moneda no encontrada.
rate-not-found = ❌ No se pudo obtener la cotización de la moneda.
alerts-invalid-number = ❌ Por favor, ingresa un número válido