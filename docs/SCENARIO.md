# 🎸 Projet : Six-String Hangover (Piscine Python)

## 📝 Pitch

Vous êtes **Johnny Fuzz**, une rockstar sur le déclin qui a plus de bouteille que de disques d'or. Votre mission ? Traverser la tournée la plus chaotique de l'histoire. Entre deux concerts, vous devrez gérer votre taux d'alcoolémie, affronter des fans enragés à coups de guitare et éviter de finir au trou avant le grand final.

---

## 🎭 Le Scénario : "La Route de la Déchéance"

### Acte I : Le Bar "Le Gosier Sec"

* **Contexte :** Vous commencez au fond du trou. Le patron du bar refuse de vous payer votre cachet tant que vous n'avez pas viré les motards qui squattent la scène.
* **Objectif :** Vaincre **Gros Bill** (le chef des motards) dans un combat au tour par tour.
* **Mécanique spéciale :** Apprentissage du système de "Bourre-Gueule". Si Johnny boit un shot, ses dégâts doublent mais sa précision chute.

### Acte II : Le Festival "Wood-Stock-Option"

* **Contexte :** Vous avez enfin un vrai contrat. Mais la sécurité a confisqué votre matériel. Vous devez récupérer votre guitare dans les loges en affrontant des agents de sécurité zélés.
* **Objectif :** Infiltrer le backstage et battre le **Chef de la Sécurité** en utilisant une guitare gonflable trouvée par terre.
* **Mécanique spéciale :** Premier mini-jeu de rythme. Si vous ratez trop de notes, le public lance des canettes de soda (perte de Points de Vie).

### Acte III : L'Ultime Stade de la Gloire

* **Contexte :** C'est le grand soir. Le stade est plein, mais votre manager a tenté de s'enfuir avec la caisse. Il vous attend sur le toit du stade avec ses gardes du corps.
* **Objectif :** Combat final contre **Le Manager Corrompu**.
* **Mécanique spéciale :** Mode "Overdrive Éthylique". Si vous atteignez le pic d'ivresse parfait sans tomber dans le coma, vous débloquez l'attaque spéciale : *Le Solo qui Brise les Vitres*.

---

## 🕹️ Mécaniques de Jeu (User Stories)

1. **Système de Combat (The Guitar Duel) :**
* `Attaque Simple` : Coup de manche de guitare.
* `Power Chord` : Attaque de zone qui utilise de l'énergie.
* `Dégueulando` : Johnny vomit, ce qui paralyse l'adversaire de dégoût pour 1 tour.


2. **Gestion de l'État :**
* `Ivresse (0-100%)` : Influe sur la force et la chance.
* `Street Cred` : Points d'expérience pour améliorer les compétences de combat.


3. **L'Arsenal :**
* *La Pelle* (Guitare de départ) : Dégâts minimes.
* *L'Électro-Choc* : Guitare chargée à l'électricité, chance de paralyser.
* *La "Hache" de Guerre* : Une guitare qui fait littéralement des dégâts tranchants.



---

## 🛠️ Structure Technique (POO)

* `Personnage` (Classe Mère) : Gère les PV, le nom, l'inventaire.
* `Joueur` & `Ennemi` (Classes Filles) : Comportements spécifiques.
* `Guitare` : Classe pour les armes avec différents modificateurs de dégâts.
* `Jeu` : La boucle principale (Loop) qui gère les déplacements et les événements aléatoires.