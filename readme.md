# Brief-IA-Parle-moi-plus

## Procédure d'installation 

1 ) Cloner le repo git :    
```
git clone https://github.com/rpdev63/git-ia-parle-moi
```

2 ) Créer un environnement virtuel 
```
cd Brief-ia-parle-moi/
python -m venv env
```
  
3 ) Activer l'environnement virtuel
```
source env/Scripts/activate
```
  
4 ) Lire le fichier requirements.txt pour installer les librairies python
```
pip install -r requirements.txt
```

## Lancer l'application :

5 ) Renseigner les variables d'environnements ( clé API sdk azure et clé API OpenAi ) dans le fichier .env 

6 ) Lancer l'application depuis la racine du projet
```
python run.py
```
