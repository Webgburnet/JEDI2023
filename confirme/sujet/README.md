---
title: JEDI 2023 — atelier confirmé
author: M. Liedloff et N. Ollinger
date: 1er juin 2023
---
# JEDI 2023 — atelier confirmé
> Le plus court chemin n'est pas toujours la ligne droite, il faut savoir contourner la montagne. *<p style='text-align: right;'>— Ch. Regimbeau</p>*

<p align="center"><img src="demo.jpg"></p>

## 0. Découverte de l'environnement de travail

### 0.1 Environnement de programmation

Dans cette activité, nous vous proposons une promenade en dehors du confort habituel des notebooks. Cette activité *— autour de l'algorithme de Dijkstra de calcul des plus courts chemins et des files de priorité —* est aussi un prétexte pour coder dans un environnement de développement intégré (IDE). C'est aussi une occasion de manipuler un peu de programmation objet, de parler de structure de données abstraite et de typage.

Dans les salles de TP du bâtiment 3IA, nous vous proposons de réaliser cette activité avec l'IDE [VSCodium](https://vscodium.com). Vous pouvez bien entendu opter pour toutes sortes d'alternatives sur vos machines personnelles (y compris [Vim](https://www.vim.org) 🤩).

Une fois l'archive extraite (*mais c'est déjà fait puisque vous lisez ce texte, non ?*), vous pouvez ouvrir une fenêtre de l'IDE avec la commande `codium` :
```
$ unzip sujet.zip
$ codium sujet
```

**À vous de jouer !** Pour une séance agréable, ré-organisez la fenêtre en 3 colonnes :
 - à gauche l'explorateur de fichiers ;
 - au centre le fichier en cours d'édition ;
 - à droite la prévisualisation de `README.md`.

 L'environnement Python des salles de TP du bâtiment 3IA dispose déjà des bibliothèques Python nécessaires pour l'atelier. Dans un autre contexte, vous pouvez sélectionner le fichier `requirements.txt` dans l'explorateur et demander à **VSCodium** de générer un environnement spécifique pour travailler sur ce projet.

### 0.2 Code source fourni et objectif de l'atelier

Le code fourni est un programme quasiment complet de détourage d'images en utilisant l'algorithme des ciseaux intelligents [[1, 2]](#ref1).

Le programme principal est contenu dans le fichier `yoda.py`. C'est lui qu'il faudra exécuter, avec ou sans argument, pour tester votre mise en œuvre des files de priorité et de l'algorithme de Dijkstra.

```
$ ./yoda.py -h
usage: yoda [-h] [-p {naive,simple}] [image]

Intelligent Scissors

positional arguments:
  image                 source image

optional arguments:
  -h, --help            show this help message and exit
  -p {naive,simple}, --priodict {naive,simple}
                        priority dict implementation

Don't worry, be heap.py!
```

Une fois complété, le programme permet de détourer une image sur le principe suivant :
 1. lancer le programme avec une image en paramètre : `$ ./yoda.py monimage.png` (le répertoire `data/` contient des exemples d'images) ;
 2. cliquer sur des points de contrôle successifs du contour de l'image ;
 3. terminer le contour en sélectionnant à nouveau le point de départ ;
 4. une image est générée dans le fichier `out.png` ;
 5. un clic droit permet à tout instant d'annuler le dernier point de contrôle.


### 0.3 Travail à réaliser

Les seuls fichiers que vous aurez à modifier pendant l'activité sont :
 - `dijkstra.py` qui contiendra le code générique de l'algorithme de Dijkstra ;
 - `prios/*.py` qui héberge différentes mises en œuvre des files de priorité utilisées par l'algorithme de Dijkstra. Chacune d'entre elles est enregistrée dans `prios/__init__.py`.

Le programme dispose d'un mode de débogage, activable par un bouton ou par la touche `Tab` du clavier. Le bouton **Recharger** permet de recharger les fichiers source décrits ci-dessus sans avoir besoin d'arrêter et de relancer le programme.

Il est possible, en mode débogage, de régler la vitesse de progression de l'algorithme et d'activer ou de désactiver l'affichage des éléments contenus dans la file et de l'arborescence des plus courts chemins. Cette fonctionnalité repose sur l'appel régulier de la méthode `pop_smallest` de la file de priorité lors de l'exécution de l'algorithme de Dijkstra.

En cas d'exception levée par le programme, une fenêtre surgissante vous informe du contexte de l'exception.

## 1. Première mise en œuvre de l'algorithme de Dijkstra

Pour l'instant, le programme n'est pas très intéressant : dès que l'utilisateur clique sur l'image, une exception est levée :

```
NotImplementedError: il faut coder __setitem__ !
```

### 1.1 Une file de priorité naïve

Le fichier `priodict.py` décrit les opérations attendues sur une file de priorité ainsi que leurs types.

Par défaut, le programme utilise la mise en œuvre naïve contenue dans `prios/naivedict.py`. Il s'agit d'une file de priorité codée comme une liste non ordonnée de paires (clé, priorité).

Toutes les opérations ont été codées par nos soins, à l'exception de la méthode `__setitem__(self, key: T, newprio: int) -> None` qui peut être utilisée pour :
 - insérer dans la file de priorité un nouvel élément `key` de priorité `newprio` ;
 - diminuer la priorité d'un élément `key` déjà présent dans la file pour lui donner la nouvelle valeur `newprio`.

 **À vous de jouer !** Modifiez le fichier `prios/naivedict.py` en complétant la méthode `__setitem__`.


### 1.2 Algorithme de Dijkstra générique

 Une fois la file de priorité correctement mise en œuvre, il manque encore un élément essentiel : l'algorithme de calcul de l'arborescence des plus courts chemins de Dijkstra.

 **À vous de jouer !** Modifiez dans le fichier `dijkstra.py` la méthode `__call__` pour qu'elle mette en œuvre l'algorithme à l'aide de la file de priorité `self.F`. L'algorithme produit l'arborescence codée dans `self.p` : chaque sommet parcouru y pointe sur son sommet parent. Par convention, la racine pointe sur `None`.

Pour rappel, voici l'algorithme présenté ce matin :
```
p[s] ← None
F.insérer(s, 0)
tant que F ≠ ∅ faire:
  u ← F.ExtraireMinimum()
  pour chaque sommet v ∈ Adj[u] faire
    si v ∉ p alors F.Insérer(v, ∞)
    si d[u] + w(u,v) < d[v] alors
      p[v] ← u
      d[v] ← d[u] + w(u,v)
      F.DiminuerClé(v, d[v])
```

Une fois votre code au point, vous devriez pouvoir détourer l'image par défaut et récupérer votre personnage sur fond transparent dans le fichier `out.png`.

Quelle complexité pour Dijkstra avec cette file de priorité ?

| Insérer | ExtraireMinimum | DiminuerClé |
|:-------:|:---------------:|:-----------:|
| $O(1)$   | $O(n)$         |  $O(n)$     |
| $n$ fois | $n$ fois       | $m$ fois    |

Coût total : $O(n^2 + mn)$

Ici avec $m < 8n$ : $O(n^2)$.

## 2. File de priorité avec un dictionnaire

La version naïve, sous forme de liste, de la file de priorité a le mérite d'exister mais elle n'est ni efficace ni concise (52 lignes).

Un dictionnaire qui associe à une clé sa priorité est quasiment une file de priorité : il ne lui manque que l'opération `pop_smallest`.

**À vous de joueur !** Modifiez le fichier `prios/simpledict.py` pour en faire une file de priorité naïve mais concise (ça se fait en 11 à 12 lignes sans astuce).

*Pour tester votre code, n'oubliez pas de sélectionner la bonne version de la file de priorité dans l'interface de débogage. Vous pouvez aussi lancer le programme avec l'option `-p simple`.*

Quelle complexité (amortie) pour Dijkstra avec cette file de priorité ?

| Insérer | ExtraireMinimum | DiminuerClé |
|:-------:|:---------------:|:-----------:|
| $O(1)$   | $O(n)$         |  $O(1)$     |
| $n$ fois | $n$ fois       | $m$ fois    |

Coût total : $O(n^2 + m)$

Ici avec $m < 8n$ : $O(n^2)$.

## 3. Une meilleure complexité avec les tas binaires

Les [tas binaires](tas/tas_binaire.md) offrent une file de priorité avec une meilleure complexité. Ils sont traditionnellement utilisés pour mettre en œuvre l'algorithme de Dijkstra. Vous allez les mettre en œuvre !

**À vous de jouer !** Créez un fichier `prios/heapdict.py` qui déclare une classe `HeapDict` qui hérite de la classe `dict` (comme pour la file de priorité précédente). Pour l'instant ne codez pas la file de priorité.

**À vous de jouer !** Modifiez le fichier `prios/__init__.py` pour que cette nouvelle classe soit intégrée au programme sous le nom `"heap"`.

**À vous de jouer !** Lisez attentivement le [document sur les tas binaires](tas/tas_binaire.md) et utilisez-le pour mettre en œuvre votre file de priorité.

Chaque entrée du dictionnaire associe à une clé un index dans un tas `self.t`. Les entrées de `self.t` sont des paires (priorité, clé).

Voici le début du code (il ne manque que `__setitem__` et `pop_smallest`... qui vous prendront sans doute un peu de temps à écrire correctement).
```
class HeapDict(dict):
    def __init__(self) -> None:
        super().__init__()
        self.t = []

    def __getitem__(self, key):
        idx = super().__getitem__(key)
        return self.t[idx][0]
```

Quelle complexité pour Dijkstra avec cette file de priorité ?

| Insérer | ExtraireMinimum | DiminuerClé |
|:-------:|:---------------:|:-----------:|
| $O(\log n)$   | $O(\log n)$         |  $O(\log n)$     |
| $n$ fois | $n$ fois       | $m$ fois    |

Coût total : $O((n+m)\log n)$

Ici avec $m < 8n$ : $O(n\log n)$.

## BONUS. Plus efficace sans (trop) réinventer la roue

Coder les tas binaires en Python, c'est lent ! Pour gagner en efficacité, il faut essayer de diminuer les constantes multiplicatives devant les $O$.

### 4.1 La bibliothèque **heapq**

La bibliothèque standard de Python fourni une bibliothèque de mise en œuvre de files de priorité : [heapq](https://docs.python.org/fr/3/library/heapq.html). Celle-ci ne permet pas de modifier les priorités des éléments de la file mais la documentation décrit [une astuce pour réaliser la file de priorité dont nous avons besoin](https://docs.python.org/fr/3/library/heapq.html#priority-queue-implementation-notes) !

**À vous de jouer !** Ajoutez une file de priorité `"heapq"` mise en œuvre par une classe `HeapqDict` dans `prios/heapqdict.py`.

### 4.2 Amortir les mises à jour

La solution précédente fonctionne mais elle reste encore un peu lente. On peut faire mieux !

Au lieu de mettre à jour les éléments dans le tas, on propose de s'autoriser à garder des doublons : pour baisser la priorité d'un élément `blop` à 54, on ajoute la paire (54, blop) au tas. Lorsque la taille du tas dépasse 2 fois le nombre d'éléments stockés dans le dictionnaire, on reconstruit le tas avec `heapify` à partir du dictionnaire.

**À vous de jouer !** Ajoutez une file de priorité `"heapqopt"` mise en œuvre par une classe `HeapqoptDict` dans `prios/heapqoptdict.py`.

### 4.3 Avec des seaux

Une alternative à l'optimisation précédente est possible lorsque les poids sur les arêtes parcourent un ensemble relativement restreint de valeurs (c'est le cas ici).

Au lieu de gérer un tas qui contient tous les éléments de la file de priorité, on crée une file (par exemple avec `collections.deque`) par valeur de priorité actuellement dans la structure et on les ordonne grâce à un tas qui stocke les valeurs de priorité actuellement présentes.

**À vous de jouer !** Ajoutez une file de priorité `"bucket"` mise en œuvre par une classe `BucketDict` dans `prios/bucketdict.py`.

## Références

<a name="ref1">[1] Mortensen, E. N., & Barrett, W. A. [Intelligent scissors for image composition](https://dl.acm.org/doi/pdf/10.1145/218380.218442). In Proceedings of the 22nd annual conference on Computer graphics and interactive techniques (pp. 191-198). 1995</a>

<a name="ref2">[2] UW CSE Faculty. [Image Scissors (for Fun and Profit)](https://courses.cs.washington.edu/courses/cse455/09wi/Lects/lect4.pdf). 2009</a>
