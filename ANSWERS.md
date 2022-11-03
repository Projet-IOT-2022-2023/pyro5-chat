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
> 

### 4. Quelle(s) limite(s) cette solution peut rencontrer dans la pratique ?
>


## Regard critique
### J'ai pris des raccourcis, pris des décisions arbitraires et utilisé des bibliothèques tiers. Ai-je laissé des vulnérabilités ? 

### A vous maintenant de trouver ce qui ne va pas, de justifier votre propos et de proposer une alternative. Ce n'est pas tant la quantité de point que vous trouverez que la pertinence de votre analyse qui vous permettera de décrocher des points.





