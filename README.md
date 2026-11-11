# Moteur pixel (Shorts et films IslamArcade)

Ce dépôt contient tout ce qu'il faut pour fabriquer les vidéos pixel art sur n'importe quel ordinateur Windows :

| Dossier | Contenu |
|---|---|
| `_MOTEUR_PIXEL/` | le moteur (Python), les scénarios, les voix déjà générées, les fiches de sources, le mode d'emploi `LISEZMOI_MOTEUR.txt` |
| `_MUSIQUES/`, `_BRUITAGES/` | les musiques de fond et les bruitages utilisés par le moteur |
| `skills/` | les skills Claude `video-pixel` et `film-pixel` (les consignes de fabrication) |
| `moteur.ps1` | installer, envoyer, recevoir |

Ne sont **pas** dans le dépôt : les vidéos rendues (`.mp4`), les planches de contrôle, les dossiers `FILM`,
`SHORTS A PUBLIER` et `_MOTEUR` (sauvegardes zip). Ils restent sur l'ordinateur où ils ont été faits.

## Installer sur un nouvel ordinateur

Il faut : Windows 10 ou 11, [Python 3.10 ou plus récent](https://www.python.org/downloads/) (cocher « Add python.exe
to PATH »), [Git](https://git-scm.com/download/win) et Claude (application de bureau).

```powershell
git clone https://github.com/bichop67/moteur-pixel.git "$env:USERPROFILE\Desktop\VIDEO YOUTUBE"
cd "$env:USERPROFILE\Desktop\VIDEO YOUTUBE"
powershell -ExecutionPolicy Bypass -File moteur.ps1 installe
```

`installe` installe les bibliothèques Python (dont ffmpeg), copie les deux skills dans `%USERPROFILE%\.claude\skills`
en y écrivant le chemin du moteur de cet ordinateur, vérifie les polices Windows et fabrique une image d'essai.
Le dossier peut s'appeler autrement et se trouver ailleurs : le moteur retrouve ses musiques et ses bruitages
à partir de son propre emplacement.

Ce qui ne voyage pas avec le dépôt et se règle une fois sur chaque ordinateur, dans Claude :
le connecteur ElevenLabs (voix), l'extension Claude dans Chrome (vérification des sources, publication) et la
connexion aux comptes YouTube / TikTok.

## Passer d'un ordinateur à l'autre

Avant de quitter un ordinateur :

```powershell
powershell -ExecutionPolicy Bypass -File moteur.ps1 envoie
```

En arrivant sur l'autre :

```powershell
powershell -ExecutionPolicy Bypass -File moteur.ps1 recois
```

`envoie` range aussi les skills de cet ordinateur dans le dépôt (registre des sujets faits, résultats, pièges) ;
`recois` les remet dans Claude. Toujours faire `recois` avant de commencer et `envoie` en partant : deux ordinateurs
qui modifient le même fichier sans se synchroniser créent un conflit que `recois` refusera.

## Limites connues

- Windows seulement : le moteur utilise les polices de Windows (Tahoma, Verdana, Segoe UI Black, Arial, Segoe Print).
- Les anciens scripts `vop06.py`, `serie.py` (Shorts « Valable ou pas ») et les petits outils datés de
  `scenarios/outils_duo_*` et `outils_film/` gardent des chemins du PC d'origine : ils servent d'archives.
- Les sources des films (dossier `FILM`) ne sont pas dans ce dépôt.
