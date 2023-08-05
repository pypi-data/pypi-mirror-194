# ADMCO_TP2

## Objectif

L'objectif de ce projet est de créer un Package robot. Le but va être de faire déplacer un robot, modéliser par un "1" dans un grille de 0. L'initialisation de la grille ainsi que les méthode de déplacement de ce robot sont instanciées dans la classe Grid dans le fichier Map.py.  
### Cahier des charges 
Les limites de de projets sont :  
- On ne peut pas créer une grille de plus de 10x10.  
- On ne peut pas faire sortir le robot de la grille.  

### Arborescence du projet 
```bash
.
├── Package_Test
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   └── test.cpython-36-pytest-7.0.1.pyc
│   └── test.py
├── Package_robot
│   ├── Map.py
│   ├── __init__.py
│   └── __pycache__
│       ├── Map.cpython-36.pyc
│       ├── Map.cpython-38.pyc
│       ├── __init__.cpython-36.pyc
│       └── __init__.cpython-38.pyc
├── README.md
├── TP2_Robot_EBERMEYER_Tom.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── dist
│   └── TP2_Robot_EBERMEYER_Tom-0.0.1.tar.gz
└── setup.py
```

## Packages à insaller 

### Rappels utilisation venv 
Il est important d'utiliser un environnement virtuel pour nos éxécutions. En effet, nur nos machines de nombreux packages de python sont déja installer. Il est important d'en créer un et d'ajouter seulement les modules nécessaires à l'éxécution. Cela permet aux futurs utilisateurs, d'utiliser notre code sur leurs machines.  
Autre problème : Où déclarer cet environnement virtuel ?  
Dans mon cas, j'ai choisit de l'instancier dans un dossier en dehors de l'emplacement de mon projet, car je pourrais perdre les fichiers que je crérais dans le dossier de l'environnement virtuel. Dans mon cas il va me permettre d'éxécuter les fichiers d'un autre dossier que le sien.  
Les lignes de commandes sont :  
création du venv : `python3 -m venv NOM-DE-L-ENVIRONNEMENT`  
activation : `source NOM-DE-L-ENVIRONNEMENT/bin/activate`  

### Lignes de commandes : installation des packages 

Numpy : `pip install numpy`  
Black : `pip install black`  
Pylint : `pip install pylint`  
Twine : `pip install twine` (Remarque : cela ne fonctionnait pas et on devait installer en temps que Package : `python -m pip install -U pip`  ) 
Bien penser à redéfinir le chemin pour les éxécutions :`export PYTHONPATH=$PYTHONPATH:'.`  
 

## Phase de Test : Unittest et logging
### Unittest
On crée une classe Unittest dans le fichier Package_Test/test.py. On a deux classes : une classe : **TestValidMouvement** qui va tester que le programme ne plante pas quand le robot arrive sur les bords de la Map. Pour ce fait on a quatre tests pour les deplacements respectifs. Et une autre classe **TestBadInputsGrid** qui test les valeurs pour initialisé la grille (soit trop grand ou pas des entiers).  
![Alt text](img/pytest.png "Optional title")
### Logging 
Les loggings sont très important sur de gros projets. En effet sur de gros projets on peut mettre différents niveaux de visibilité : debug,     info, warning, error et critical. Dans le fichier Package_Test/test.py, on a en début de notre fichier après l'import, `logging.basicConfig(level = logging.CRITICAL)` qui permet de définir le niveau de vibilité lors du lancement du programme. Ici on utilise les logging pour vérifier que nos tests passent bien avec un petit affichage. On utilise deux niveaux de visibilités : _WARNING_ pour vérifier le bon fonctionnement des déplacements et _CRITICAL_ pour vérifier le bon fonctionnement de mauvais inputs pour la création de la grille. Ici _CRITICAL_ qui est un niveau plus haut à été choisit car il est juger plus important un bon création de grille que des fonctionnement de déplacements. 
![Alt text](img/critical.png "Optional title")  
Si on veut afficher tous les logs il faut écrire : `logging.basicConfig(level = logging.WARNING)`.   
![Alt text](img/warning.png "Optional title")  
## Création du Package
Package à télécharger : `pip install TP2-Robot-EBERMEYER-Tom==0.0.1` 
## Etapes d'intégration continue 

## Version 1.0

## Extensions 

## TODO 

Problème rencontré lors de l'installation de twine, correction : ` python -m pip install -U pip`  



logging : utilisation de critical pour les raisesErrors en inputs, et warning pour les fonctions de déplacements.  

faire des versions avec des tag : ex tag 1 V1, etc ...  

retirer les fichiers inutiles.  
pip freeze : 
astroid==2.11.7
attrs==22.2.0
black==22.8.0
bleach==4.1.0
certifi==2022.12.7
cffi==1.15.1
charset-normalizer==2.0.12
click==8.0.4
colorama==0.4.5
cryptography==39.0.1
dataclasses==0.8
dill==0.3.4
docutils==0.18.1
idna==3.4
importlib-metadata==4.8.3
importlib-resources==5.4.0
iniconfig==1.1.1
isort==5.10.1
jeepney==0.7.1
keyring==23.4.1
lazy-object-proxy==1.7.1
mccabe==0.7.0
mypy-extensions==1.0.0
numpy==1.19.5
packaging==21.3
pathspec==0.9.0
pkg_resources==0.0.0
pkginfo==1.9.6
platformdirs==2.4.0
pluggy==1.0.0
py==1.11.0
pycparser==2.21
Pygments==2.14.0
pylint==2.13.9
pylist==1.4.0
pyparsing==3.0.9
pytest==7.0.1
readme-renderer==34.0
requests==2.27.1
requests-toolbelt==0.10.1
rfc3986==1.5.0
SecretStorage==3.3.3
six==1.16.0
tomli==1.2.3
TP2-Robot-EBERMEYER-Tom==0.0.1
tqdm==4.64.1
twine==3.8.0
typed-ast==1.5.4
typing_extensions==4.1.1
urllib3==1.26.14
webencodings==0.5.1
wrapt==1.14.1
zipp==3.6.0






