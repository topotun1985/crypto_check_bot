hello-user = 👋 Salut, { $username }!
default-username = Ami
subscription-info = 💳 Votre abonnement : { $plan }
subscription-currencies = 💰 Devises sélectionnées pour le suivi : { $current }/{ $max }
subscription-expires-infinite = ⏳ Abonnement illimité
subscription-expires-until = ⏳ Date d'expiration de l'abonnement : { $expires } (UTC+0)
subscription-purchase-success = ✅ Abonnement souscrit avec succès ! Merci pour votre achat.
subscription-terms-link = Veuillez consulter les conditions avant de payer : /subscription_terms
welcome-text = 📢 Voulez-vous être le premier à savoir quand le prix monte ou descend ? Choisissez une devise, définissez un seuil, et notre bot vous notifiera lorsque le prix atteindra le niveau souhaité ! 🚀
select-action = Choisissez une action :
subscription-plans = Plans d'abonnement :
plan-basic-description = Basic — jusqu'à { $limit } devises
plan-standard-description = Standard — jusqu'à { $limit } devises
plan-premium-description = Premium — jusqu'à { $limit } devises
subscription-validity-period = Durée de validité de l'abonnement : 30 jours
subscription-already-active = ❌ Vous avez déjà un abonnement actif « { $plan } » jusqu'au { $expires }. Vous ne pouvez pas en acheter un nouveau tant que l'actuel n'a pas expiré.
subscription-already-active-db = ❌ Vous avez déjà un abonnement actif « { $plan } » jusqu'au { $expires }. Vous ne pouvez pas en acheter un nouveau tant que l'actuel n'a pas expiré.
price-star = { $price } ⭐
#payment
subscription-payment-button = Envoyer { $price } ⭐️
subscription-invoice-title = Abonnement { $plan }
subscription-invoice-description = Abonnez-vous à { $plan } pour 30 jours
subscription-price-label = Abonnement { $plan }
#btn
btn-all-rates = 📊 Tous les taux des devises
btn-choose-currency = 🪙 Choisir une devise
btn-set-alert = 🔔 Configurer les notifications
btn-subscription = 💳 Abonnement
btn-help = ❓ Aide
btn-basic = 🔰 Acheter Basic
btn-standard = 💎 Acheter Standard
btn-premium = 👑 Acheter Premium
btn-back = ⬅️ Retour
button-enable-alerts = 🔔 Activer les notifications
button-disable-alerts = 🔕 Désactiver les notifications
button-set-threshold-usd = 💲 Définir le seuil en $
button-set-threshold-rub = 💲 Définir le seuil en ₽
button-set-threshold-above = 📈 Définir le seuil supérieur
button-set-threshold-below = 📉 Définir le seuil inférieur
btn-toggle-currency = 🔄 Afficher en { $currency }
button-choose-usd = 💵 En dollars (USD)
button-choose-rub = 💰 En roubles (RUB)
btn-set-new-threshold = 📝 Définir un nouveau seuil
btn-my-currencies = 🎯 Mes devises
#help
help-text = 👋 Salut! Ceci est la section d'aide
help-how-to-use = 🔍 Comment utiliser le bot?
help-get-rates = 📌 1. Obtenir des informations sur les taux.
help-get-rates-desc = Appuyez sur le bouton «📊 Tous les taux de pièces». Le bot affichera le taux actuel de toutes les pièces disponibles.
help-my-currencies = 📌 2. 🎯 Mes pièces.
help-my-currencies-desc = Dans la section «🎯 Mes pièces», vous pouvez :
  - Voir toutes les pièces suivies
  - Consulter les taux actuels
help-add-currency = 📌 3. Ajouter une pièce à la liste de suivi.
help-add-currency-desc = Appuyez sur le bouton «🪙 Choisir la pièce». En sélectionnant une pièce, appuyez sur «☑️ Pièce» pour suivre les variations de prix. Selon votre abonnement, vous pouvez suivre de 1 à 10 pièces simultanément.
help-set-alert = 📌 4. Configurer les notifications de taux.
help-set-alert-desc = Appuyez sur «🔔 Configurer les notifications» et choisissez une pièce dans la liste de suivi. Entrez une valeur seuil pour le prix (par exemple, seuil supérieur pour Bitcoin 99000$). Le bot enverra une notification lorsque le taux atteindra la valeur spécifiée.
help-manage-subscription = 📌 5. Gérer l'abonnement.
help-manage-subscription-desc = Dans la section «💳 Abonnement», vous pouvez :
  - Consulter le plan actuel et les limites.
  - Acheter un nouvel abonnement avec Telegram Stars.
  - Vérifier la durée de validité de l'abonnement.
  - Après l'achat, les limites des pièces sont automatiquement mises à jour.
help-commands = 📌 6. Commandes principales:
help-commands-list = 
  /start — Menu principal
  /help — Aide
  /subscription — Gérer l'abonnement
  /subscription_terms — Conditions d'abonnement
  /support — Support
help-support = ✉️ Support: pricealertprobot@outlook.com
#rate
rates-header = 📊 Taux actuels des cryptomonnaies :
rate-format-usd = { $name } ({ $symbol }) : { $price } $
rate-format-rub = { $name } ({ $symbol }) : { $price } ₽
rates-updated = 🕒 Mis à jour : { $time } (UTC+0)
dollar-rate = Taux du dollar : { $price } ₽
show-in-rub = en roubles
show-in-usd = en dollars
rates-error = ❌ Une erreur s'est produite lors de la récupération des taux. Veuillez réessayer plus tard.
# Commands
cmd-start = Démarrer le bot
cmd-help = Aide
cmd-subscription = Gérer l'abonnement
cmd-subscription-terms = Conditions d'abonnement
cmd-support = Support
my-currencies-empty = ⚠️ Vous n'avez sélectionné aucune devise pour le moment
alerts-no-currencies = ⚠️ Vous n'avez aucune devise suivie. Ajoutez des devises dans la section « Mes devises ».
subscription-limit-reached = ⚠️ Vous avez atteint la limite de devises suivies pour votre abonnement ! Pour ajouter plus de devises, un autre type d'abonnement est nécessaire.
currency-added = ✅ La devise {$currency} a été ajoutée pour le suivi
currency-removed = ❌ La devise {$currency} a été retirée du suivi
choose-currency-instruction = Choisissez les devises à suivre :
✅ - devise suivie
☑️ - devise non suivie
# alerts
alerts-list-header = 🔔 Paramètres des notifications pour ❨{$currency}❩
alerts-choose-currency = Choisissez une devise pour configurer les notifications :
alerts-error = ❌ Une erreur s'est produite. Veuillez réessayer plus tard.
alerts-current-price = Prix actuel :
alerts-current-price-both = Prix actuel : {$price_usd} $ / {$price_rub} ₽
alerts-current-settings = Paramètres actuels :
alerts-notifications-enabled = ✅ Notifications activées
alerts-notifications-disabled = ❌ Notifications désactivées
alerts-usd-header = Seuils (USD) :
alerts-rub-header = Seuils (RUB) :
alerts-not-set = non défini
alerts-threshold-above = ⬆️ Supérieur à
alerts-threshold-below = ⬇️ Inférieur à
alerts-disabled-successfully = ✅ Notifications désactivées avec succès
alert-details = Devise : {$currency}
alerts-no-thresholds = ℹ️ Pour activer les notifications, veuillez d'abord définir les seuils !
no-alerts-to-disable = ⚠️ Aucune notification active à désactiver
alert-added-successfully = ✅ Notification ajoutée avec succès !
alert-updated-successfully = ✅ Notification mise à jour avec succès !
alert-price = Prix
alert-price-above = ⬆️ a dépassé
alert-price-below = ⬇️ est descendu en dessous de
alert-not-found = ⚠️ Notification non trouvée
error-invalid-alert = ❌ Erreur : ID de notification invalide
alerts-enter-threshold-above-usd = Entrez le seuil supérieur du prix en USD :
alerts-enter-threshold-below-usd = Entrez le seuil inférieur du prix en USD :
alerts-enter-threshold-above-rub = Entrez le seuil supérieur du prix en roubles :
alerts-enter-threshold-below-rub = Entrez le seuil inférieur du prix en roubles :
# Threshold Settings
select-currency-type = 💵 Choisissez la devise pour le seuil :
select-condition = Choisissez la condition pour la notification :
enter-threshold-value = Entrez la valeur seuil :
invalid-threshold-value = ❌ Valeur incorrecte. Veuillez entrer un nombre positif.
enter-new-threshold = Entrez une nouvelle valeur seuil pour { $currency } en { $currency_type }:
# Errors
error-occurred = ❌ Une erreur s'est produite. Veuillez réessayer plus tard.
currency-not-found = ❌ Devise non trouvée.
rate-not-found = ❌ Impossible d'obtenir le taux de la devise.
alerts-invalid-number = ❌ Veuillez entrer un nombre valide
error-threshold-must-be-positive = ❌ La valeur doit être supérieure à 0
error-threshold-invalid-format = ❌ Format de nombre invalide. Utilisez un point comme séparateur (par exemple : 1.23)
error-threshold-too-many-decimals-small = ❌ Trop de chiffres après le point : { $decimals }
                                          Pour les nombres inférieurs à 1, un maximum de 5 chiffres décimaux est autorisé
                                          Exemple : 0.00123
error-threshold-too-many-decimals-large = ❌ Trop de chiffres après le point : { $decimals }
                                          Pour les nombres supérieurs ou égaux à 1, un maximum de 2 chiffres décimaux est autorisé
                                          Exemples : 1.23, 10.5, 100.00
error-threshold-generic = ❌ Veuillez entrer un nombre valide
                          Exemples :
                          - Nombres entiers : 1, 10, 100
                          - Avec décimales : 1.23, 0.0012
error-threshold-too-large = ❌ Valeur trop élevée. La valeur maximale autorisée est 999999999
unsupported-text-message = Désolé, je ne comprends pas le texte. Veuillez utiliser les commandes du bot ou les boutons du menu.
unsupported-photo = Désolé, je ne traite pas les photos. Veuillez utiliser les commandes du bot ou les boutons du menu.
unsupported-sticker = Désolé, je ne traite pas les stickers. Veuillez utiliser les commandes du bot ou les boutons du menu.
unsupported-document = Désolé, je ne traite pas les documents. Veuillez utiliser les commandes du bot ou les boutons du menu.
unsupported-voice = Désolé, je ne traite pas les messages vocaux. Veuillez utiliser les commandes du bot ou les boutons du menu.
unsupported-video = Désolé, je ne traite pas les vidéos. Veuillez utiliser les commandes du bot ou les boutons du menu.
unsupported-message = Désolé, ce type de message n'est pas supporté. Veuillez utiliser les commandes du bot ou les boutons du menu.
subscription-terms-text = 
      📄 Conditions d'abonnement

      1. Abonnement gratuit (Free)
      📊 Disponible : 1 devise pour le suivi.
      🔄 Flexibilité : Vous pouvez changer la devise sélectionnée à tout moment.
      💡 Recommandation : Nous vous recommandons de commencer par la version gratuite pour évaluer les fonctionnalités du bot.

      2. Abonnements payants
      Basic (200 Stars) :
      📈 Suivi : Jusqu'à { $basic_limit } devises.
      ⏳ Durée : 30 jours.

      Standard (300 Stars) :
      📈 Suivi : Jusqu'à { $standard_limit } devises.
      ⏳ Durée : 30 jours.
      
      Premium (400 Stars) :
      📈 Suivi : Jusqu'à { $premium_limit } devises.
      ⏳ Durée : 30 jours.

      3. Conditions importantes
      ❗ Sans remboursement : Aucun remboursement n'est effectué après l'achat de l'abonnement.
      🔄 Changement de plan : Le type d'abonnement payant ne peut être modifié qu'après l'expiration de l'abonnement en cours (par exemple, passer de Premium à Standard).
      ⛔ Renouvellement manuel : Les abonnements ne se renouvellent pas automatiquement — le paiement est effectué manuellement.
      💎 Utilisation des Telegram Stars : Les Telegram Stars sont utilisés exclusivement pour les services numériques (la vente de biens physiques est interdite).

      4. Recommandations
      🚀 Test : Avant d'acheter un abonnement payant, nous vous recommandons d'utiliser la version gratuite pour vous assurer que les fonctionnalités du bot répondent à vos besoins.
      ⚠️ Choix attentif : Choisissez votre plan avec soin, car il ne peut pas être modifié après achat.
      Clause légale :
      En souscrivant à un abonnement, vous acceptez ces conditions. Tous les abonnements sont définitifs, aucun remboursement n'est effectué. Le bot fournit uniquement des services numériques et n'est pas responsable des pertes potentielles liées à l'utilisation du service.
cmd-support-text =
      🛠 Support

      Si vous avez des questions, des problèmes de paiement ou concernant les fonctionnalités du bot, écrivez-nous : 
      ✉️ pricealertprobot@outlook.com

      ⏰ Horaires de support : 
      Notre service de support est disponible de 12:00 à 21:00 (UTC+0).

      ❗ Important :  
      🚀 Test : Avant d'acheter un abonnement payant, nous vous recommandons d'utiliser la version gratuite pour vous assurer que les fonctionnalités du bot répondent à vos besoins.
      ⚠️ Choix attentif : Choisissez votre plan avec soin, car il ne peut pas être modifié après achat.
      
      Clause légale :
      Tous les abonnements sont définitifs, aucun remboursement n'est effectué. Le bot fournit uniquement des services numériques et n'est pas responsable des pertes potentielles liées à l'utilisation du service. (voir « Conditions d'abonnement »).
      
      Veuillez noter : les temps de réponse peuvent varier.