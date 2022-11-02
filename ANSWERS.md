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
### 1. Est ce que urandom est un bon choix pour de la cryptographie ? Pouquoi ?

### 2. Pourquoi utiliser ses primitives cryptographiques peut être dangereux?

### 3. Pourquoi malgré le chiffrement un serveur malveillant peut il nous nuire encore ? 

### 4. Quelle propriété manque t-il ici?

## Authenticated Symetric Encryption

### 1. Pourquoi Fernet est moins risqué que le précédent chapitre en terme d'implémentation ?

### 2. Un serveur malveillant peut néanmoins attaqué avec des faux messages, déjà utilisé dans le passé. Comment appel t-on cette attaque  ?

### 3. Quelle méthode simple permet de s'en affranchir ?

## TTL
### 1. Remarquez vous une différence avec le chapitre précédent ?

### 2. Maintenant soustrayez 45 au temps lors de l'émission. Que se passe t-il et pourquoi ? 

### 3. Est-ce efficace pour se protéger de l'attaque du précédent chapitre ? 

### 4. Quelle(s) limite(s) cette solution peut rencontrer dans la pratique ?

## Regard critique
### J'ai pris des raccourcis, pris des décisions arbitraires et utilisé des bibliothèques tiers. Ai-je laissé des vulnérabilités ? 

### A vous maintenant de trouver ce qui ne va pas, de justifier votre propos et de proposer une alternative. Ce n'est pas tant la quantité de point que vous trouverez que la pertinence de votre analyse qui vous permettera de décrocher des points.





