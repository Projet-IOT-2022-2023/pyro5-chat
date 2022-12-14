# ANSWERS

---

## Prise en main

### 1. Comment s'appelle cette topologie ?

> C'est une topologie en étoile.


### 2. Que remarquez-vous dans les logs ?
```log
Bind on 127.0.0.1:66666
INFO:ChatServer:Register a new user foo with callback handler <Pyro5.client.Proxy at 0x7ff5bcb10e50; not connected; for PYRO:obj_3994b89f083b413fadbddb758802b215@localhost:40299; owner 140693330720320>
DEBUG:ChatServer:User list : ['foo']
INFO:ChatServer:Register a new user fool with callback handler <Pyro5.client.Proxy at 0x7ff5bcb11360; not connected; for PYRO:obj_ecafdd3e1bf94353bd9db2b01137de98@localhost:46121; owner 140693407303232>
DEBUG:ChatServer:User list : ['foo', 'fool']
INFO:ChatServer:foo send message : hello
INFO:ChatServer:message send to fool
INFO:ChatServer:fool send message : ok
INFO:ChatServer:message send to foo
INFO:ChatServer:foo send message : salut
INFO:ChatServer:message send to fool
```
> D'après les logs du serveur, on remarque que pour chaque utilisateur créé,
le serveur ajoute l'id associé dans un tableau contenant celui de tous les utilisateurs connectés. 
> Le log enregistre également chaque message envoyé avec son émetteur et son contenu.
On remarque aussi que les messages apparaissent en clair sur le serveur.



### 3. Pourquoi est-ce un problème et quel principe cela viole-t-il ?
> Cela viole le principe <span style="color:pink;"><u><b>d'authentification</b></u></span> pour la connexion mais aussi viole le principe de <span style="color:pink;"><u><b>confidentialité</b></u></span>.



### 4. Quelle solution la plus simple pouvez-vous mettre en place pour éviter cela ? Détaillez votre réponse.
> La méthode la plus simple est d'ajouter un chiffrement <span style="color:red">AES</span> entre les clients afin d'éviter des attaques `Man In The Middle` et de respecter le principe de confidentialité.

## Chiffrement
### 1. Est ce que urandom est un bon choix pour de la cryptographie ? Pourquoi ?
> Urandom est un bon choix car il permet de générer des nombres aléatoires de manière sécurisée. Il est utilisé pour générer des clés de chiffrement. Attention, cette méthode ne génère pas du true random mais des nombres pseudo-aléatoires.


### 2. Pourquoi utiliser ses primitives cryptographiques peut être dangereux?
> Il est déconseillé d'utiliser ses propres primitives cryptographiques pour les 3 raisons suivantes :
> - le concepteur peut ne pas avoir les compétences mathématiques et pratiques suffisantes pour maitriser tous les aspects de la conception d'une nouvelle primitive cryptographique
> - la conception d'une nouvelle primitive cryptographique est extrêmement longue et très sujette aux erreurs
> - Les algorithmes qui la définissent ne doivent pas seulement être solidement conçus mais aussi être intensivement testés par la communauté des chercheurs en cryptologie afin de déceler la présence éventuelle d'erreurs.

### 3. Pourquoi malgré le chiffrement un serveur malveillant peut il nous nuire encore ? 
> Le serveur peut altérer les messages envoyés, il n'y a pas de garantie que le message envoyé par un utilisateur soit bien celui reçu par l'autre.

### 4. Quelle propriété manque t-il ici?
> Il manque la propriété d'intégrité.

## Authenticated Symetric Encryption

### 1. Pourquoi Fernet est moins risqué que le précédent chapitre en terme d'implémentation ?
> Fernet est moins risqué que le précédent chapitre car il utilise des primitives cryptographiques déjà existantes et testées par la communauté des chercheurs en cryptologie. De plus, il utilise un HMAC construit à partir d'un hash du vecteur d'initialisation, du timestamp et du message chiffré pour garantir l'intégrité des messages.

### 2. Un serveur malveillant peut néanmoins attaquer avec des faux messages, déjà utilisé dans le passé. Comment appel t-on cette attaque  ?
> Ce type d'attaque est nommé <b>"attaque de l'homme du milieu"</b> (de l'anglais <b><i>man-in-the-middle attack</i></b>)

### 3. Quelle méthode simple permet de s'en affranchir ?
> Le <b>TTL</b> (Time to Live) permet d'éviter ce genre de problèmes en définissant et contrôlant le cycle de vie d'un message. Par exemple, on a Alice qui veut envoyer un message à Bob. Pour simplifier dans notre exemple, le TTL sera de 1, le message passe directement de Alice à Bob. Si Paul intercepte le message entre temps et le modifie, cela incrémenterait le TTL de 1 et Bob saura que le message aura été touché par un tier.

## TTL
### 1. Remarquez vous une différence avec le chapitre précédent ?
> Non, il n'y a pas de différence notable avec le chapitre précédent.

### 2. Maintenant soustrayez 45 au temps lors de l'émission. Que se passe t-il et pourquoi ? 
> Le message est refusé car le TTL est inférieur à 0.

### 3. Est-ce efficace pour se protéger de l'attaque du précédent chapitre ? 
> Cette solution est efficace pour se protéger de l'attaque du précédent chapitre en comparant le temps entre l'émission et la réception.

### 4. Quelle(s) limite(s) cette solution peut rencontrer dans la pratique ?
> Cette solution peut rencontrer des problèmes dans la pratique car il faut que les deux utilisateurs aient une horloge synchronisée. De plus, il faut que le TTL soit suffisamment grand pour que le message puisse être envoyé et reçu dans les temps.


## Regard critique
### J'ai pris des raccourcis, pris des décisions arbitraires et utilisé des bibliothèques tiers. Ai-je laissé des vulnérabilités ? 

### A vous maintenant de trouver ce qui ne va pas, de justifier votre propos et de proposer une alternative. Ce n'est pas tant la quantité de point que vous trouverez que la pertinence de votre analyse qui vous permettera de décrocher des points.


> 1. possibilité de mettre une longueur de message ou d'utilisateur infinie
> 
> Pour corriger ce problème, il faut rajouter au début du programme du serveur :
> ```python 
> import Pyro5
> Pyro5.config.MAX_MESSAGE_SIZE = 4092 # 4 ko
> ```
>
> 2. possibilité de ne pas respecter le format d'envoi
>
> Vérifier du côté du serveur si on a bien des données encodés en base64 dans un dictionnaire sous la forme `{"data": Donnée en base64 , "encoding": "base64"}`.
>
> 3. possibilité de se connecter plusieurs fois avec le même nom
>
> Vérifier du côté du serveur si le nom est déjà utilisé, si oui, le serveur refuse la connexion. On peut ajouter dans la fonction `register` du serveur :
> ```python
> if user in self._buffer:
>            raise ValueError("user already registered")
> ```
>
> 4. This is a “Hazardous Materials” module -> https://cryptography.io/en/latest/hazmat/primitives/index.html -> contiens des vulnérabilités
>
> Ne pas utiliser des fonctions provenant de `cryptography.hazmat` mais plutôt de `cryptography.fernet` par exemple. (Ce problème a été corrigé dans fernet_gui.py et time_fernet_gui.py)
> 
> 5. Le serveur qui est démarré en mode debug
> 
> Enlever le mode debug du serveur 
> 
> 6. Pas de synchronisation du timestamp entre les deux utilisateurs
> 
> Le serveur peut envoyer som timestamp lors de la connexion à l'utilisateur pour que celui-ci puisse synchroniser son horloge

> 7. Pas de vérification de l'authenticité du message, l'en-tête peut être modifié (qui contient le username) car il est envoyé en clair
> 
> Utiliser les méthodes de chiffrement/signature SSL/TLS intégrées à Pyro5 pour s'assurer de l'authenticité du message. Cela permet d'éviter les attaques de l'homme du milieu entre le client et le serveur. Cependant, si on ne trust pas le serveur, il faut utiliser un certificat auto-signé pour chaque utilisateur pour s'assurer de l'authenticité du message. L'utilisateur enverra son certificat à l'autre utilisateur par un autre biais pour qu'il puisse vérifier l'authenticité du message.
