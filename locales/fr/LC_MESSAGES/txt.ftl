hello-user = 👋 Bonjour, { $username }!
subscription-info = 📜 Votre abonnement : { $plan }
subscription-currencies = 💰 Nombre de pièces suivies : { $current }/{ $max }
subscription-expires-infinite = ⏳ Abonnement à vie
subscription-expires-until = ⏳ Expiration de l'abonnement : { $expires } (UTC+0)
subscription-purchase-success = ✅ Abonnement souscrit avec succès ! Merci pour votre achat.
welcome-text = 📢 Vous souhaitez être parmi les premiers informés des hausses ou baisses de prix ? Choisissez une pièce, définissez un seuil, et notre bot vous notifiera dès que le prix atteindra le niveau souhaité ! 🚀
select-action = Choisissez une action :
subscription-plans = Plans d'abonnement :
plan-basic-description = Basique — jusqu'à { $limit } pièces
plan-standard-description = Standard — jusqu'à { $limit } pièces
plan-premium-description = Premium — jusqu'à { $limit } pièces
subscription-validity-period = Durée de l'abonnement : 30 jours
subscription-already-active = ❌ Vous avez déjà un abonnement actif "{ $plan }" jusqu'au { $expires }. Vous ne pouvez pas en acheter un nouveau tant que l'abonnement actuel n'est pas expiré.
subscription-already-active-db = ❌ Vous avez déjà un abonnement actif "{ $plan }" jusqu'au { $expires }. Vous ne pouvez pas en acheter un nouveau tant que l'abonnement actuel n'est pas expiré.
price-star = { $price } ⭐
#btn
btn-all-rates = 📊 Tous les taux des pièces
btn-choose-currency = 💎 Choisir une pièce
btn-set-alert = ⏰ Configurer les alertes
btn-subscription = 📜 Abonnement
btn-help = ❓ Aide
btn-basic = 💳 Acheter le Basique
btn-standard = 💎 Acheter le Standard
btn-premium = 👑 Acheter le Premium
btn-back = ⬅️ Retour
button-enable-alerts = 🔔 Activer les alertes
button-disable-alerts = 🔕 Désactiver les alertes
button-set-threshold-usd = 💲 Définir le seuil en $
button-set-threshold-rub = 💲 Définir le seuil en ₽
button-set-threshold-above = 📈 définir le seuil supérieur
button-set-threshold-below = 📉 définir le seuil inférieur
btn-toggle-currency = 🔄 Afficher en { $currency }
button-choose-usd = 💵 En dollars (USD)
button-choose-rub = 💰 En roubles (RUB)
btn-set-new-threshold = 📝 Définir un nouveau seuil
btn-my-currencies = 🎯 Mes pièces
#help
help-text = 👋 Bonjour ! Ceci est la section d'aide.
help-how-to-use = 🔍 Comment utiliser le bot ?
help-get-rates = 📌 1. Obtenir les taux.
help-get-rates-desc = Appuyez sur le bouton «📊 Tous les taux des pièces». Le bot affichera le taux actuel de toutes les pièces disponibles.
help-add-currency = 📌 2. Ajouter une pièce à la liste de suivi.
help-add-currency-desc = Appuyez sur le bouton «💎 Choisir une pièce». Lors du choix, appuyez sur «⭐ Ajouter» pour suivre l'évolution du prix de la pièce. Selon votre abonnement, vous pouvez suivre de 1 à 20 pièces simultanément.
help-set-alert = 📌 3. Configurer les alertes de taux.
help-set-alert-desc = Appuyez sur «⏰ Configurer les alertes» et choisissez une pièce dans la liste de suivi. Indiquez un seuil de prix (par exemple, Bitcoin > 50 000$). Le bot vous notifiera lorsque le taux atteindra la valeur indiquée.
help-manage-subscription = 📌 4. Gérer l'abonnement.
help-manage-subscription-desc = Dans la section «📜 Abonnement», vous pouvez :
  - Consulter votre plan actuel et vos limites.
  - Acheter un nouvel abonnement avec Telegram Stars.
  - Vérifier la date d'expiration de l'abonnement.
  - Après l'achat, les limites de pièces se mettent à jour automatiquement.
help-commands = 📌 5. Commandes principales :
help-commands-list = 
  /start — Menu principal
  /help — Aide
  /subscription — Gérer l'abonnement
help-support = ✉️ Support : @SupportBot
#rate
rates-header = 📊 Taux actuels des cryptomonnaies :
rate-format-usd = { $name } ({ $symbol }): { $price } $
rate-format-rub = { $name } ({ $symbol }): { $price } ₽
rates-updated = 🕒 Mis à jour : { $time } (UTC+0)
dollar-rate = Taux du dollar : { $price } ₽
show-in-rub = en roubles
show-in-usd = en dollars
rates-error = ❌ Une erreur s'est produite lors de la récupération des taux. Veuillez réessayer plus tard.
# Commands
cmd-start = Démarrer le bot
cmd-help = Aide
cmd-subscription = Gérer l'abonnement
my-currencies-empty = ⚠️ Vous n'avez encore sélectionné aucune pièce
alerts-no-currencies = ⚠️ Vous n'avez aucune pièce suivie. Ajoutez des pièces dans la section "Mes pièces".
subscription-limit-reached = ⚠️ Vous avez atteint la limite de pièces suivies pour votre abonnement ! Pour en ajouter davantage, un autre type d'abonnement est requis.
currency-added = ✅ La pièce {$currency} a été ajoutée pour le suivi
currency-removed = ❌ La pièce {$currency} a été retirée du suivi
choose-currency-instruction = Choisissez les pièces à suivre :
✅ - pièce suivie
☑️ - pièce non suivie
# alerts
alerts-list-header = 🔔 Paramètres d'alerte pour { $currency }
alerts-choose-currency = Choisissez une pièce pour configurer les alertes :
alerts-error = ❌ Une erreur est survenue. Veuillez réessayer plus tard.
alerts-current-price = Prix actuel :
alerts-current-price-both = Prix actuel : { $price_usd } $ / { $price_rub } ₽
alerts-current-settings = Paramètres actuels :
alerts-notifications-enabled = ✅ Alertes activées
alerts-notifications-disabled = ❌ Alertes désactivées
alerts-usd-header = Seuils (USD) :
alerts-rub-header = Seuils (RUB) :
alerts-not-set = non défini
alerts-threshold-above = ⬆️ Supérieur à
alerts-threshold-below = ⬇️ Inférieur à
alerts-disabled-successfully = ✅ Alertes désactivées avec succès
alert-details = Pièce : { $currency }
alerts-no-thresholds = ℹ️ Pour activer les alertes, définissez d'abord les seuils !
no-alerts-to-disable = ⚠️ Aucune alerte active à désactiver
alert-added-successfully = ✅ Alerte ajoutée avec succès !
alert-updated-successfully = ✅ Alerte mise à jour avec succès !
alert-price = Prix
alert-price-above = ⬆️ a dépassé
alert-price-below = ⬇️ est tombé en dessous de
alert-not-found = ⚠️ Alerte introuvable
error-invalid-alert = ❌ Erreur : ID d'alerte invalide
alerts-enter-threshold-above-usd = Entrez le seuil supérieur en USD :
alerts-enter-threshold-below-usd = Entrez le seuil inférieur en USD :
alerts-enter-threshold-above-rub = Entrez le seuil supérieur en RUB :
alerts-enter-threshold-below-rub = Entrez le seuil inférieur en RUB :
# Threshold Settings
select-currency-type = 💵 Choisissez la devise pour le seuil :
select-condition = Choisissez la condition de l'alerte :
enter-threshold-value = Entrez la valeur du seuil :
invalid-threshold-value = ❌ Valeur invalide. Veuillez entrer un nombre positif.
enter-new-threshold = Entrez un nouveau seuil pour { $currency } en { $currency_type } :
# Errors
error-occurred = ❌ Une erreur est survenue. Veuillez réessayer plus tard.
currency-not-found = ❌ Pièce non trouvée.
rate-not-found = ❌ Impossible d'obtenir le taux de la pièce.
alerts-invalid-number = ❌ Veuillez entrer un nombre valide