# base-ramses

## Infos utiles

#### Url de connexion a la base locale
> 


### Commandes utiles
1. Lancer la base de donnée:
> docker-compose up -d ramses-db

### Poetry
1. Demarrer l'environnement: poetry shell
2. Installer toutes les dependances: poetry install
3. Ajouter une dependence: poetry add ma_lib
4. 





# Project structure

## Extractors
These are python classes which all inherit a base abstract class BaseExtractor.  
The main goal of an extractor is to specify an implementation for a given data source.  


## Models
A collection of python classes which define each database table through sqlalchemy models.  