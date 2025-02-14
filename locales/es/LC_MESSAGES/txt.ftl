hello-user = 👋 ¡Hola, { $username }!
default-username = Amigo
subscription-info = 💳 Tu suscripción: { $plan }
subscription-currencies = 💰 Monedas seleccionadas para seguimiento: { $current }/{ $max }
subscription-expires-infinite = ⏳ Suscripción ilimitada
subscription-expires-until = ⏳ Fecha de finalización de la suscripción: { $expires } (UTC+0)
subscription-purchase-success = ✅ ¡Suscripción adquirida con éxito! Gracias por tu compra.
subscription-terms-link = Antes de pagar, revisa los términos: /subscription_terms
welcome-text = 📢 ¿Quieres ser el primero en enterarte cuando suba o baje el precio? ¡Elige una moneda, establece un umbral, y nuestro bot te notificará cuando el precio alcance el nivel deseado! 🚀
select-action = Elige una acción:
subscription-plans = Planes de suscripción:
plan-basic-description = Básico — hasta { $limit } monedas
plan-standard-description = Estándar — hasta { $limit } monedas
plan-premium-description = Premium — hasta { $limit } monedas
subscription-validity-period = Periodo de validez de la suscripción: 30 días
subscription-already-active = ❌ Ya tienes una suscripción activa "{ $plan }" hasta { $expires }. No puedes comprar una nueva hasta que la actual expire.
subscription-already-active-db = ❌ Ya tienes una suscripción activa "{ $plan }" hasta { $expires }. No puedes comprar una nueva hasta que la actual expire.
price-star = { $price } ⭐
#payment
subscription-payment-button = Enviar { $price } ⭐️
subscription-invoice-title = Suscripción { $plan }
subscription-invoice-description = Suscríbete a { $plan } por 30 días
subscription-price-label = Suscripción { $plan }
#btn
btn-all-rates = 📊 Todas las cotizaciones de monedas
btn-choose-currency = 🪙 Elegir moneda
btn-set-alert = 🔔 Configurar notificaciones
btn-subscription = 💳 Suscripción
btn-help = ❓ Ayuda
btn-basic = 🔰 Comprar Básico
btn-standard = 💎 Comprar Estándar
btn-premium = 👑 Comprar Premium
btn-back = ⬅️ Atrás
button-enable-alerts = 🔔 Activar notificaciones
button-disable-alerts = 🔕 Desactivar notificaciones
button-set-threshold-usd = 💲 Establecer umbral en $
button-set-threshold-rub = 💲 Establecer umbral en ₽
button-set-threshold-above = 📈 Establecer umbral superior
button-set-threshold-below = 📉 Establecer umbral inferior
btn-toggle-currency = 🔄 Mostrar en { $currency }
button-choose-usd = 💵 En dólares (USD)
button-choose-rub = 💰 En rublos (RUB)
btn-set-new-threshold = 📝 Establecer nuevo umbral
btn-my-currencies = 🎯 Mis monedas
#help
help-text = 👋 ¡Hola! Esta es la sección de ayuda.
help-how-to-use = 🔍 ¿Cómo usar el bot?
help-get-rates = 📌 1. Obtener información sobre las tasas.
help-get-rates-desc = Presiona el botón «📊 Todas las cotizaciones de monedas». El bot mostrará la tasa actual de todas las monedas disponibles en el bot.
help-add-currency = 📌 2. Agregar una moneda a la lista de seguimiento.
help-add-currency-desc = Presiona el botón «🪙 Elegir moneda». Al seleccionar una moneda, toca «☑️ Moneda» para seguir sus cambios de precio. Dependiendo de tu suscripción, puedes seguir de 1 a 10 monedas simultáneamente.
help-set-alert = 📌 3. Configurar notificaciones de tasas.
help-set-alert-desc = Presiona «🔔 Configurar notificaciones» y elige una moneda de la lista de seguimiento. Ingresa el valor umbral del precio (por ejemplo, umbral superior para Bitcoin 99000$). El bot enviará una notificación cuando la tasa alcance el valor especificado.
help-manage-subscription = 📌 4. Gestión de suscripción.
help-manage-subscription-desc = En la sección «💳 Suscripción» puedes:
  - Conocer el plan actual y los límites.
  - Comprar una nueva suscripción con Telegram Stars.
  - Ver el periodo de validez de la suscripción.
  - Después de adquirir una suscripción, los límites de monedas se actualizan automáticamente.
help-commands = 📌 5. Comandos principales:
help-commands-list = 
  /start — Menú principal
  /help — Ayuda
  /subscription — Gestión de suscripción
  /subscription_terms — Términos de suscripción
  /support — Soporte
help-support = ✉️ Soporte: pricealertprobot@outlook.com
#rate
rates-header = 📊 Tasas actuales de criptomonedas:
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Actualizado: { $time } (UTC+0)
dollar-rate = Tasa del dólar: { $price } ₽
show-in-rub = en rublos
show-in-usd = en dólares
rates-error = ❌ Ocurrió un error al obtener las tasas. Por favor, inténtalo más tarde.
# Commands
cmd-start = Iniciar bot
cmd-help = Ayuda
cmd-subscription = Gestión de suscripción
cmd-subscription-terms = Términos de suscripción
cmd-support = Soporte
my-currencies-empty = ⚠️ Aún no has seleccionado ninguna moneda
alerts-no-currencies = ⚠️ No tienes monedas en seguimiento. Agrega monedas en la sección "Mis monedas".
subscription-limit-reached = ⚠️ ¡Has alcanzado el límite de monedas en seguimiento para tu suscripción! Para agregar más monedas, se requiere un tipo de suscripción diferente.
currency-added = ✅ Moneda {$currency} añadida para seguimiento
currency-removed = ❌ Moneda {$currency} eliminada del seguimiento
choose-currency-instruction = Elige las monedas para seguimiento:
✅ - la moneda está siendo seguida
☑️ - la moneda no está siendo seguida
# alerts
alerts-list-header = 🔔 Configuración de notificaciones para ❨{$currency}❩
alerts-choose-currency = Elige una moneda para configurar las notificaciones:
alerts-error = ❌ Ocurrió un error. Por favor, inténtalo más tarde.
alerts-current-price = Precio actual:
alerts-current-price-both = Precio actual: {$price_usd} $ / {$price_rub} ₽
alerts-current-settings = Configuración actual:
alerts-notifications-enabled = ✅ Notificaciones activadas
alerts-notifications-disabled = ❌ Notificaciones desactivadas
alerts-usd-header = Umbrales (USD):
alerts-rub-header = Umbrales (RUB):
alerts-not-set = no establecido
alerts-threshold-above = ⬆️ Por encima
alerts-threshold-below = ⬇️ Por debajo
alerts-disabled-successfully = ✅ Notificaciones desactivadas con éxito
alert-details = Moneda: {$currency}
alerts-no-thresholds = ℹ️ Para activar las notificaciones, primero establece los umbrales!
no-alerts-to-disable = ⚠️ No hay notificaciones activas para desactivar
alert-added-successfully = ✅ ¡Notificación agregada con éxito!
alert-updated-successfully = ✅ ¡Notificación actualizada con éxito!
alert-price = Precio
alert-price-above = ⬆️ superó
alert-price-below = ⬇️ bajó de
alert-not-found = ⚠️ Notificación no encontrada
error-invalid-alert = ❌ Error: ID de notificación inválido
alerts-enter-threshold-above-usd = Ingresa el umbral superior del precio en USD:
alerts-enter-threshold-below-usd = Ingresa el umbral inferior del precio en USD:
alerts-enter-threshold-above-rub = Ingresa el umbral superior del precio en rublos:
alerts-enter-threshold-below-rub = Ingresa el umbral inferior del precio en rublos:
# Threshold Settings
select-currency-type = 💵 Elige la moneda para el umbral:
select-condition = Elige la condición para la notificación:
enter-threshold-value = Ingresa el valor umbral:
invalid-threshold-value = ❌ Valor incorrecto. Por favor, ingresa un número positivo.
enter-new-threshold = Ingresa un nuevo valor umbral para { $currency } en { $currency_type }:
# Errors
error-occurred = ❌ Ha ocurrido un error. Por favor, inténtalo más tarde.
currency-not-found = ❌ Moneda no encontrada.
rate-not-found = ❌ No se pudo obtener la tasa de la moneda.
alerts-invalid-number = ❌ Por favor, introduce un número válido
error-threshold-must-be-positive = ❌ El valor debe ser mayor que 0
error-threshold-invalid-format = ❌ Formato de número inválido. Usa un punto como separador (por ejemplo: 1.23)
error-threshold-too-many-decimals-small = ❌ Demasiados dígitos decimales: { $decimals }
                                          Para números menores que 1 se permite un máximo de 5 dígitos decimales
                                          Ejemplo: 0.00123
error-threshold-too-many-decimals-large = ❌ Demasiados dígitos decimales: { $decimals }
                                          Para números mayores o iguales a 1 se permite un máximo de 2 dígitos decimales
                                          Ejemplos: 1.23, 10.5, 100.00
error-threshold-generic = ❌ Por favor, introduce un número válido
                          Ejemplos:
                          - Números enteros: 1, 10, 100
                          - Con decimales: 1.23, 0.0012
error-threshold-too-large = ❌ Valor demasiado alto. El valor máximo permitido es 999999999
unsupported-text-message = Lo siento, no entiendo el texto. Por favor, utiliza los comandos del bot o los botones del menú.
unsupported-photo = Lo siento, no proceso fotos. Por favor, utiliza los comandos del bot o los botones del menú.
unsupported-sticker = Lo siento, no proceso stickers. Por favor, utiliza los comandos del bot o los botones del menú.
unsupported-document = Lo siento, no proceso documentos. Por favor, utiliza los comandos del bot o los botones del menú.
unsupported-voice = Lo siento, no proceso mensajes de voz. Por favor, utiliza los comandos del bot o los botones del menú.
unsupported-video = Lo siento, no proceso videos. Por favor, utiliza los comandos del bot o los botones del menú.
unsupported-message = Lo siento, este tipo de mensaje no es compatible. Por favor, utiliza los comandos del bot o los botones del menú.
subscription-terms-text = 
      📄 Términos de suscripción

      1. Suscripción gratuita (Free)
      📊 Disponible: 1 moneda para seguimiento.
      🔄 Flexibilidad: Puedes cambiar la moneda seleccionada en cualquier momento.
      💡 Recomendación: Recomendamos comenzar con la versión gratuita para evaluar la funcionalidad del bot.

      2. Suscripciones de pago
      Basic (200 Stars):
      📈 Seguimiento: Hasta 4 monedas.
      ⏳ Validez: 30 días.

      Standard (300 Stars):
      📈 Seguimiento: Hasta 7 monedas.
      ⏳ Validez: 30 días.
      
      Premium (400 Stars):
      📈 Seguimiento: Hasta 10 monedas.
      ⏳ Validez: 30 días.

      3. Condiciones importantes
      ❗ Sin reembolso: No se realizan reembolsos después de comprar una suscripción.
      🔄 Cambio de plan: Solo se puede cambiar el tipo de suscripción de pago después de que expire la suscripción actual (por ejemplo, cambiar de Premium a Standard).
      ⛔ Renovación manual: Las suscripciones no se renuevan automáticamente — el pago se realiza manualmente.
      💎 Uso de Telegram Stars: Telegram Stars se utilizan exclusivamente para servicios digitales (se prohíbe la venta de productos físicos).

      4. Recomendaciones
      🚀 Prueba: Antes de adquirir una suscripción de pago, recomendamos usar la versión gratuita para asegurarte de que la funcionalidad del bot se ajuste a tus necesidades.
      ⚠️ Elección cuidadosa: Elige tu plan cuidadosamente, ya que no se puede cambiar después de la compra.
      Aviso legal:
      Al adquirir una suscripción, aceptas estos términos. Todas las suscripciones son definitivas, no se realizan reembolsos. El bot ofrece únicamente servicios digitales y no se hace responsable de posibles pérdidas derivadas del uso del servicio.
cmd-support-text =
      🛠 Soporte

      Si tienes alguna pregunta, problemas con el pago o con la funcionalidad del bot, escríbenos:
      ✉️ pricealertprobot@outlook.com

      ⏰ Horario de soporte:
      Nuestro servicio de soporte está disponible de 12:00 a 21:00 (UTC+0).

      ❗ Importante:
      🚀 Prueba: Antes de adquirir una suscripción de pago, recomendamos usar la versión gratuita para asegurarte de que la funcionalidad del bot se ajuste a tus necesidades.
      ⚠️ Elección cuidadosa: Elige tu plan cuidadosamente, ya que no se puede cambiar después de la compra.
      
      Aviso legal:
      Todas las suscripciones son definitivas, no se realizan reembolsos. El bot ofrece únicamente servicios digitales y no se hace responsable de posibles pérdidas derivadas del uso del servicio. (ver “Términos de suscripción”).
      
      Ten en cuenta: los tiempos de respuesta pueden variar.