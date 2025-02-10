hello-user = 👋 Olá, { $username }!
subscription-info = 📜 Sua assinatura: { $plan }
subscription-currencies = 💰 Moedas selecionadas para monitoramento: { $current }/{ $max }
subscription-expires-infinite = ⏳ Assinatura vitalícia
subscription-expires-until = ⏳ Data de expiração: { $expires } (UTC+0)
subscription-purchase-success = ✅ Assinatura realizada com sucesso! Obrigado pela sua compra.
welcome-text = 📢 Quer ser o primeiro a saber quando o preço subir ou cair? Escolha uma moeda, defina um limite e nosso bot o notificará assim que o preço atingir o nível desejado! 🚀
select-action = Escolha uma ação:
subscription-plans = Planos de assinatura:
plan-basic-description = Básico — até { $limit } moedas
plan-standard-description = Padrão — até { $limit } moedas
plan-premium-description = Premium — até { $limit } moedas
subscription-validity-period = Validade da assinatura: 30 dias
subscription-already-active = ❌ Você já possui uma assinatura ativa "{ $plan }" até { $expires }. Você não pode adquirir uma nova enquanto a atual não expirar.
subscription-already-active-db = ❌ Você já possui uma assinatura ativa "{ $plan }" até { $expires }. Você não pode adquirir uma nova enquanto a atual não expirar.
price-star = { $price } ⭐
#btn
btn-all-rates = 📊 Todas as cotações das moedas
btn-choose-currency = 💎 Escolher moeda
btn-set-alert = ⏰ Configurar alertas
btn-subscription = 📜 Assinatura
btn-help = ❓ Ajuda
btn-basic = 💳 Comprar Básico
btn-standard = 💎 Comprar Padrão
btn-premium = 👑 Comprar Premium
btn-back = ⬅️ Voltar
button-enable-alerts = 🔔 Ativar alertas
button-disable-alerts = 🔕 Desativar alertas
button-set-threshold-usd = 💲 Definir limite em $
button-set-threshold-rub = 💲 Definir limite em ₽
button-set-threshold-above = 📈 definir limite superior
button-set-threshold-below = 📉 definir limite inferior
btn-toggle-currency = 🔄 Exibir em { $currency }
button-choose-usd = 💵 Em dólares (USD)
button-choose-rub = 💰 Em rublos (RUB)
btn-set-new-threshold = 📝 Definir novo limite
btn-my-currencies = 🎯 Minhas moedas
#help
help-text = 👋 Olá! Esta é a seção de ajuda.
help-how-to-use = 🔍 Como usar o bot?
help-get-rates = 📌 1. Obter informações sobre as cotações.
help-get-rates-desc = Toque no botão «📊 Todas as cotações das moedas». O bot mostrará a cotação atual de todas as moedas disponíveis.
help-add-currency = 📌 2. Adicionar uma moeda à lista de monitoramento.
help-add-currency-desc = Toque no botão «📈 Escolher moeda». Ao selecionar uma moeda, toque em «⭐ Adicionar» para acompanhar as mudanças de preço. Dependendo da sua assinatura, você pode monitorar de 1 a 20 moedas simultaneamente.
help-set-alert = 📌 3. Configurar alertas de cotação.
help-set-alert-desc = Toque em «⏰ Configurar alertas» e escolha uma moeda da lista de monitoramento. Informe o valor limite (por exemplo, Bitcoin > $50 000). O bot enviará uma notificação quando a cotação atingir o valor especificado.
help-manage-subscription = 📌 4. Gerenciar assinatura.
help-manage-subscription-desc = Na seção «📜 Assinatura», você pode:
  - Ver seu plano atual e os limites.
  - Comprar uma nova assinatura com Telegram Stars.
  - Ver a data de expiração da assinatura.
  - Após a compra, os limites de moedas são atualizados automaticamente.
help-commands = 📌 5. Comandos principais:
help-commands-list = 
  /start — Menu principal
  /help — Ajuda
  /subscription — Gerenciar assinatura
help-support = ✉️ Suporte: @SupportBot
#rate
rates-header = 📊 Cotações atuais das criptomoedas:
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Atualizado: { $time } (UTC+0)
dollar-rate = Cotação do dólar: { $price } ₽
show-in-rub = em rublos
show-in-usd = em dólares
rates-error = ❌ Ocorreu um erro ao obter as cotações. Por favor, tente novamente mais tarde.
# Commands
cmd-start = Iniciar bot
cmd-help = Ajuda
cmd-subscription = Gerenciar assinatura
my-currencies-empty = ⚠️ Você ainda não selecionou nenhuma moeda
alerts-no-currencies = ⚠️ Você não possui moedas monitoradas. Adicione moedas na seção "Minhas moedas".
subscription-limit-reached = ⚠️ Você atingiu o limite de moedas monitoradas para o seu plano! Para adicionar mais moedas, é necessário um tipo de assinatura diferente.
currency-added = ✅ Moeda {$currency} adicionada para monitoramento
currency-removed = ❌ Moeda {$currency} removida do monitoramento
choose-currency-instruction = Escolha as moedas para monitoramento:
✅ - moeda monitorada
☑️ - moeda não monitorada
# alerts
alerts-list-header = 🔔 Configurações de alertas para { $currency }
alerts-choose-currency = Escolha uma moeda para configurar os alertas:
alerts-error = ❌ Ocorreu um erro. Por favor, tente novamente mais tarde.
alerts-current-price = Preço atual:
alerts-current-price-both = Preço atual: { $price_usd } $ / { $price_rub } ₽
alerts-current-settings = Configurações atuais:
alerts-notifications-enabled = ✅ Alertas ativados
alerts-notifications-disabled = ❌ Alertas desativados
alerts-usd-header = Valores limite (USD):
alerts-rub-header = Valores limite (RUB):
alerts-not-set = não definido
alerts-threshold-above = ⬆️ Acima de
alerts-threshold-below = ⬇️ Abaixo de
alerts-disabled-successfully = ✅ Alertas desativados com sucesso
alert-details = Moeda: { $currency }
alerts-no-thresholds = ℹ️ Para ativar os alertas, primeiro defina os valores limite!
no-alerts-to-disable = ⚠️ Não há alertas ativos para desativar
alert-added-successfully = ✅ Alerta adicionada com sucesso!
alert-updated-successfully = ✅ Alerta atualizada com sucesso!
alert-price = Preço
alert-price-above = ⬆️ ultrapassou
alert-price-below = ⬇️ caiu abaixo de
alert-not-found = ⚠️ Alerta não encontrada
error-invalid-alert = ❌ Erro: ID de alerta inválido
alerts-enter-threshold-above-usd = Insira o valor limite superior em USD:
alerts-enter-threshold-below-usd = Insira o valor limite inferior em USD:
alerts-enter-threshold-above-rub = Insira o valor limite superior em RUB:
alerts-enter-threshold-below-rub = Insira o valor limite inferior em RUB:
# Threshold Settings
select-currency-type = 💵 Escolha a moeda para o limite:
select-condition = Escolha a condição para o alerta:
enter-threshold-value = Insira o valor do limite:
invalid-threshold-value = ❌ Valor inválido. Por favor, insira um número positivo.
enter-new-threshold = Insira um novo valor limite para { $currency } em { $currency_type }:
# Errors
error-occurred = ❌ Ocorreu um erro. Por favor, tente novamente mais tarde.
currency-not-found = ❌ Moeda não encontrada.
rate-not-found = ❌ Não foi possível obter a cotação da moeda.
alerts-invalid-number = ❌ Por favor, insira um número válido
error-threshold-must-be-positive = ❌ O valor deve ser maior que 0
error-threshold-invalid-format = ❌ Formato de número inválido. Use o ponto como separador decimal (por exemplo: 1.23)
error-threshold-too-many-decimals-small = ❌ Muitos dígitos após o ponto: { $decimals }\nPara números menores que 1, é permitido no máximo 5 dígitos decimais\nExemplo: 0.00123
error-threshold-too-many-decimals-large = ❌ Muitos dígitos após o ponto: { $decimals }\nPara números maiores ou iguais a 1, é permitido no máximo 2 dígitos decimais\nExemplos: 1.23, 10.5, 100.00
error-threshold-generic = ❌ Por favor, insira um número válido\nExemplos:\n- Números inteiros: 1, 10, 100\n- Com ponto: 1.23, 0.0012