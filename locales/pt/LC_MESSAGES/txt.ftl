hello-user = 👋 Olá, { $username }!
default-username = Amigo
subscription-info = 💳 Sua assinatura: { $plan }
subscription-currencies = 💰 Moedas selecionadas para monitoramento: { $current }/{ $max }
subscription-expires-infinite = ⏳ Assinatura vitalícia
subscription-expires-until = ⏳ Data de expiração da assinatura: { $expires } (UTC+0)
subscription-purchase-success = ✅ Assinatura efetuada com sucesso! Obrigado pela sua compra.
subscription-terms-link = Consulte os termos antes de pagar: /subscription_terms
welcome-text = 📢 Quer ser o primeiro a saber quando o preço subir ou cair? Escolha uma moeda, defina um limite, e nosso bot notificará você quando o preço atingir o nível desejado! 🚀
select-action = Escolha uma ação:
subscription-plans = Planos de Assinatura:
plan-basic-description = Basic — até { $limit } moedas
plan-standard-description = Standard — até { $limit } moedas
plan-premium-description = Premium — até { $limit } moedas
subscription-validity-period = Validade da assinatura: 30 dias
subscription-already-active = ❌ Você já possui uma assinatura ativa "{ $plan }" até { $expires }. Você não pode adquirir uma nova até que a atual expire.
subscription-already-active-db = ❌ Você já possui uma assinatura ativa "{ $plan }" até { $expires }. Você não pode adquirir uma nova até que a atual expire.
price-star = { $price } ⭐
#payment
subscription-payment-button = Enviar { $price } ⭐️
subscription-invoice-title = Assinatura { $plan }
subscription-invoice-description = Assine { $plan } por 30 dias
subscription-price-label = Assinatura { $plan }
#btn
btn-all-rates = 📊 Todas as cotações das moedas
btn-choose-currency = 🪙 Escolher moeda
btn-set-alert = 🔔 Configurar alertas
btn-subscription = 💳 Assinatura
btn-help = ❓ Ajuda
btn-basic = 🔰 Comprar Basic
btn-standard = 💎 Comprar Standard
btn-premium = 👑 Comprar Premium
btn-back = ⬅️ Voltar
button-enable-alerts = 🔔 Ativar alertas
button-disable-alerts = 🔕 Desativar alertas
button-set-threshold-usd = 💲 Definir limite em $
button-set-threshold-rub = 💲 Definir limite em ₽
button-set-threshold-above = 📈 Definir limite superior
button-set-threshold-below = 📉 Definir limite inferior
btn-toggle-currency = 🔄 Mostrar em { $currency }
button-choose-usd = 💵 Em dólares (USD)
button-choose-rub = 💰 Em rublos (RUB)
btn-set-new-threshold = 📝 Definir novo limite
btn-my-currencies = 🎯 Minhas moedas
#help
help-text = 👋 Olá! Esta é a seção de ajuda
help-how-to-use = 🔍 Como usar o bot?
help-get-rates = 📌 1. Obter informações sobre as cotações.
help-get-rates-desc = Toque no botão «📊 Todas as cotações das moedas». O bot exibirá a cotação atual de todas as moedas disponíveis.
help-my-currencies = 📌 2. 🎯 Minhas moedas.
help-my-currencies-desc = Na seção «🎯 Minhas moedas» você pode:
  - Ver todas as moedas monitoradas
  - Consultar as cotações atuais
help-add-currency = 📌 3. Adicionar uma moeda à lista de monitoramento.
help-add-currency-desc = Toque no botão «🪙 Escolher moeda». Ao selecionar uma moeda, toque em «☑️ Moeda» para monitorar a variação do seu preço. Dependendo da sua assinatura, você pode monitorar de 1 a 10 moedas simultaneamente.
help-set-alert = 📌 4. Configurar notificações de cotação.
help-set-alert-desc = Toque em «🔔 Configurar notificações» e escolha uma moeda da lista de monitoramento. Insira um valor limite para o preço (por exemplo, limite superior para Bitcoin 99000$). O bot enviará uma notificação quando o preço atingir o valor especificado.
help-manage-subscription = 📌 5. Gerenciar a assinatura.
help-manage-subscription-desc = Na seção «💳 Assinatura» você pode:
  - Ver o plano atual e os limites.
  - Comprar uma nova assinatura com Telegram Stars.
  - Consultar a validade da assinatura.
  - Após a compra, os limites de moedas são atualizados automaticamente.
help-commands = 📌 6. Comandos principais:
help-commands-list = 
  /start — Menu principal
  /help — Ajuda
  /subscription — Gerenciar a assinatura
  /subscription_terms — Termos da assinatura
  /support — Suporte
help-support = ✉️ Suporte: pricealertprobot@outlook.com
#rate
rates-header = 📊 Cotações atuais de criptomoedas:
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
cmd-subscription-terms = Termos de assinatura
cmd-support = Suporte
my-currencies-empty = ⚠️ Você ainda não selecionou nenhuma moeda
alerts-no-currencies = ⚠️ Você não tem moedas monitoradas. Adicione moedas na seção "Minhas moedas".
subscription-limit-reached = ⚠️ Você atingiu o limite de moedas monitoradas para sua assinatura! Para adicionar mais moedas, é necessário um tipo de assinatura diferente.
currency-added = ✅ A moeda {$currency} foi adicionada para monitoramento
currency-removed = ❌ A moeda {$currency} foi removida do monitoramento
choose-currency-instruction = Escolha as moedas para monitoramento:
✅ - moeda monitorada
☑️ - moeda não monitorada
# alerts
alerts-list-header = 🔔 Configurações de alertas para ❨{$currency}❩
alerts-choose-currency = Escolha uma moeda para configurar os alertas:
alerts-error = ❌ Ocorreu um erro. Por favor, tente novamente mais tarde.
alerts-current-price = Preço atual:
alerts-current-price-both = Preço atual: {$price_usd} $ / {$price_rub} ₽
alerts-current-settings = Configurações atuais:
alerts-notifications-enabled = ✅ Alertas ativados
alerts-notifications-disabled = ❌ Alertas desativados
alerts-usd-header = Limites (USD):
alerts-rub-header = Limites (RUB):
alerts-not-set = não definido
alerts-threshold-above = ⬆️ Acima
alerts-threshold-below = ⬇️ Abaixo
alerts-disabled-successfully = ✅ Alertas desativados com sucesso
alert-details = Moeda: {$currency}
alerts-no-thresholds = ℹ️ Para ativar os alertas, primeiro defina os limites!
no-alerts-to-disable = ⚠️ Não há alertas ativos para desativar
alert-added-successfully = ✅ Alerta adicionado com sucesso!
alert-updated-successfully = ✅ Alerta atualizado com sucesso!
alert-price = Preço
alert-price-above = ⬆️ ultrapassou
alert-price-below = ⬇️ caiu abaixo de
alert-not-found = ⚠️ Alerta não encontrado
error-invalid-alert = ❌ Erro: ID do alerta inválido
alerts-enter-threshold-above-usd = Digite o limite superior do preço em USD:
alerts-enter-threshold-below-usd = Digite o limite inferior do preço em USD:
alerts-enter-threshold-above-rub = Digite o limite superior do preço em rublos:
alerts-enter-threshold-below-rub = Digite o limite inferior do preço em rublos:
# Threshold Settings
select-currency-type = 💵 Escolha a moeda para o limite:
select-condition = Escolha a condição para o alerta:
enter-threshold-value = Digite o valor do limite:
invalid-threshold-value = ❌ Valor inválido. Por favor, insira um número positivo.
enter-new-threshold = Digite o novo valor do limite para { $currency } em { $currency_type }:
# Errors
error-occurred = ❌ Ocorreu um erro. Por favor, tente novamente mais tarde.
currency-not-found = ❌ Moeda não encontrada.
rate-not-found = ❌ Não foi possível obter a cotação da moeda.
alerts-invalid-number = ❌ Por favor, insira um número válido
error-threshold-must-be-positive = ❌ O valor deve ser maior que 0
error-threshold-invalid-format = ❌ Formato de número inválido. Utilize ponto como separador (exemplo: 1.23)
error-threshold-too-many-decimals-small = ❌ Muitas casas decimais: { $decimals }
                                          Para números menores que 1, é permitido no máximo 5 casas decimais
                                          Exemplo: 0.00123
error-threshold-too-many-decimals-large = ❌ Muitas casas decimais: { $decimals }
                                          Para números maiores ou iguais a 1, é permitido no máximo 2 casas decimais
                                          Exemplos: 1.23, 10.5, 100.00
error-threshold-generic = ❌ Insira um número válido
                          Exemplos:
                          - Números inteiros: 1, 10, 100
                          - Com decimais: 1.23, 0.0012
error-threshold-too-large = ❌ Valor muito elevado. O valor máximo permitido é 999999999
unsupported-text-message = Desculpe, não entendo o texto. Por favor, utilize os comandos do bot ou os botões do menu.
unsupported-photo = Desculpe, não processo fotos. Por favor, utilize os comandos do bot ou os botões do menu.
unsupported-sticker = Desculpe, não processo stickers. Por favor, utilize os comandos do bot ou os botões do menu.
unsupported-document = Desculpe, não processo documentos. Por favor, utilize os comandos do bot ou os botões do menu.
unsupported-voice = Desculpe, não processo mensagens de voz. Por favor, utilize os comandos do bot ou os botões do menu.
unsupported-video = Desculpe, não processo vídeos. Por favor, utilize os comandos do bot ou os botões do menu.
unsupported-message = Desculpe, este tipo de mensagem não é suportado. Por favor, utilize os comandos do bot ou os botões do menu.
subscription-terms-text = 
      📄 Termos de Assinatura

      1. Assinatura Gratuita (Free)
      📊 Disponível: 1 moeda para monitoramento.
      🔄 Flexibilidade: Você pode mudar a moeda selecionada a qualquer momento.
      💡 Recomendação: Recomendamos começar com a versão gratuita para avaliar as funcionalidades do bot.

      2. Assinaturas Pagas
      Basic (200 Stars):
      📈 Monitoramento: Até { $basic_limit } moedas.
      ⏳ Validade: 30 dias.

      Standard (300 Stars):
      📈 Monitoramento: Até { $standard_limit } moedas.
      ⏳ Validade: 30 dias.
      
      Premium (400 Stars):
      📈 Monitoramento: Até { $premium_limit } moedas.
      ⏳ Validade: 30 dias.

      3. Condições Importantes
      ❗ Sem reembolso: Nenhum reembolso é realizado após a compra da assinatura.
      🔄 Alteração de plano: O tipo de assinatura paga só pode ser alterado após o término da assinatura atual (por exemplo, mudar de Premium para Standard).
      ⛔ Renovação manual: As assinaturas não são renovadas automaticamente — o pagamento é feito manualmente.
      💎 Uso dos Telegram Stars: Os Telegram Stars são utilizados exclusivamente para serviços digitais (a venda de produtos físicos é proibida).

      4. Recomendações
      🚀 Teste: Antes de adquirir uma assinatura paga, recomendamos usar a versão gratuita para ter certeza de que as funcionalidades do bot atendem às suas necessidades.
      ⚠️ Escolha com cuidado: Escolha seu plano com atenção, pois ele não poderá ser alterado após a compra.
      Cláusula Legal:
      Ao adquirir uma assinatura, você concorda com estes termos. Todas as assinaturas são definitivas, não há reembolso. O bot fornece exclusivamente serviços digitais e não se responsabiliza por eventuais perdas decorrentes do uso do serviço.
cmd-support-text =
      🛠 Suporte

      Se você tiver dúvidas, problemas com o pagamento ou com as funcionalidades do bot, escreva-nos: 
      ✉️ pricealertprobot@outlook.com

      ⏰ Horário de Suporte: 
      Nosso suporte funciona das 12:00 às 21:00 (UTC+0).

      ❗ Importante:
      🚀 Teste: Antes de adquirir uma assinatura paga, recomendamos usar a versão gratuita para ter certeza de que as funcionalidades do bot atendem às suas necessidades.
      ⚠️ Escolha com cuidado: Escolha seu plano com atenção, pois ele não poderá ser alterado após a compra.
      
      Cláusula Legal:
      Todas as assinaturas são definitivas, não há reembolso. O bot fornece exclusivamente serviços digitais e não se responsabiliza por eventuais perdas decorrentes do uso do serviço. (consulte «Termos de Assinatura»).
      
      Observe: os tempos de resposta podem variar.