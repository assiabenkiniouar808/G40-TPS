Application de chat :
1. Que font les deux scripts ?

Le script server.py joue le rôle de serveur UDP. Il crée une socket, l’associe à une adresse et à un port, puis reste en attente de messages provenant d’un client. Lorsqu’il reçoit un message, il l’affiche et renvoie une réponse au client indiquant le nombre d’octets reçus.

Le script client.py joue le rôle de client UDP. Il crée une socket, construit un message contenant la date et l’heure actuelles, puis envoie ce message au serveur. Ensuite, il attend la réponse du serveur et l’affiche à l’écran.

En résumé, les deux scripts réalisent une communication client/serveur en utilisant le protocole UDP.

2. Quelles sont les différentes fonctions utilisées dans les deux programmes ?
Dans server.py
socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
crée une socket réseau en IPv4 avec le protocole UDP.
sock.bind(('127.0.0.1', port))
associe la socket du serveur à une adresse IP et à un port.
sock.getsockname()
retourne l’adresse et le port utilisés par la socket.
sock.recvfrom(MAX_BYTES)
reçoit les données envoyées par un client, ainsi que son adresse.
data.decode('utf-8')
transforme les octets reçus en chaîne de caractères.
reponse.encode('utf-8')
transforme la réponse texte en octets pour pouvoir l’envoyer.
sock.sendto(data, address)
envoie la réponse au client.
Dans client.py
socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
crée une socket UDP.
datetime.now()
récupère la date et l’heure actuelles.
text.encode('utf-8')
convertit le message texte en octets.
sock.sendto(data, ('127.0.0.1', port))
envoie le message au serveur.
sock.getsockname()
affiche l’adresse locale utilisée par le client.
sock.recvfrom(MAX_BYTES)
reçoit la réponse du serveur.
data.decode('utf-8')
convertit les octets reçus en texte lisible.

Aller plus loin — N clients

1. Si on a plusieurs clients (N clients), proposer des modifications pour qu’un client A puisse discuter directement avec un client B:

Si le système comporte plusieurs clients, le serveur doit maintenir une liste ou un dictionnaire des clients connectés. Chaque client peut être identifié par un nom, un pseudo, ou une adresse réseau. Lorsqu’un client A veut envoyer un message à un client B, il doit préciser le destinataire dans son message. Le serveur lit ce destinataire puis retransmet le message uniquement au client B au lieu de l’envoyer à tous les autres clients.

2. Quels sont les inconvénients de cette architecture ?


Cette architecture présente plusieurs inconvénients.
D’abord, le serveur est un point central unique : s’il tombe en panne, toute la communication s’arrête.
Ensuite, quand le nombre de clients augmente, le serveur doit gérer davantage de messages et peut devenir lent.
De plus, avec UDP, les messages ne sont pas garantis : ils peuvent être perdus, dupliqués ou arriver dans le désordre.
Enfin, cette architecture demande au serveur de conserver les informations de tous les clients, ce qui complique la gestion du système.

Exercice Tableau :

Pour résoudre le problème sans utiliser la division, on calcule pour chaque élément le produit des éléments situés à gauche et à droite. On stocke ces produits dans deux tableaux intermédiaires, puis on multiplie les valeurs correspondantes pour obtenir le résultat final. Cette méthode permet d’obtenir une solution efficace en temps linéaire.
