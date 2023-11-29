# My-Candle

Le code que partagé est un programme MicroPython destiné à être exécuté sur un dispositif matériel compatible avec le langage MicroPython. Ce programme combine plusieurs fonctionnalités, notamment la connexion Wi-Fi, la configuration d'un serveur HTTP, le contrôle de périphériques (LED, bouton, PIR, moteur pas à pas, etc.), et l'utilisation de pages HTML pour le contrôle à distance.


### Importation des bibliothèques
Le code commence par l'importation des bibliothèques nécessaires, telles que `machine`, `time`, `network`, `socket`, et d'autres.

### Configuration du pays pour la radio RP2
Il configure le pays pour la radio RP2 en utilisant la fonction `rp2.country('FR')`.

### Connexion Wi-Fi
Le code définit le nom du réseau (`ssid`) et le mot de passe (`pw`), active l'interface Wi-Fi, et tente de se connecter au réseau Wi-Fi avec une gestion du délai.

### Clignotement de la LED embarquée
Une fonction `blink_onboard_led` est définie pour faire clignoter la LED embarquée, indiquant le statut de la connexion Wi-Fi.

### Configuration du serveur HTTP
Le code configure un serveur HTTP simple à l'aide de sockets, en écoutant sur l'adresse IP '0.0.0.0' et le port 80.

### Configuration des broches pour le contrôle des périphériques
Les broches du microcontrôleur sont configurées pour contrôler différents périphériques tels que LED, bouton, PIR, moteur pas à pas, ventilateur, etc.

### Initialisation du moteur pas à pas
Le code initialise un moteur pas à pas en définissant une séquence de pas et en initialisant les broches correspondantes.

### Boucle principale
Le programme entre ensuite dans une boucle infinie où il attend une connexion client. Une fois une connexion établie, il vérifie les commandes dans l'URL et effectue des actions en conséquence, telles que le contrôle de la LED, le mouvement du moteur pas à pas, etc.

### Gestion des commandes de la LED
Le code examine les commandes dans l'URL et réagit en conséquence. Il peut s'agir d'allumer ou d'éteindre la LED, avec une logique de déplacement du moteur pas à pas, gestion du PIR, etc.

### Gestion de la commande d'extinction
Si une commande spécifique est détectée dans l'URL, le programme exécute la fonction `extinction()`, éteignant le ventilateur et terminant le programme.

### Réponse avec la page HTML
Une fois les actions traitées, le code renvoie une page HTML en réponse à la requête du client.



# À la ligne 218

La boucle est amenée à changer elle sera optimisé.
