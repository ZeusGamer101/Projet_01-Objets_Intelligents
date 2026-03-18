# READ ME - TP1 du cours de *Développement d'objets intelligents*
<br>
<br>

## 1. Architecture du projet
<br>
<br>

## 2. Covention de topics
**Préfixe unique:** ahuntsic/aec-iot/b3/equipe_blondel_martin/piBM

**Télémetrie JSON:** ahuntsic/aec-iot/b3/equipe_blondel_martin/piBM/sensors/temperature

**Valeur brute:** ahuntsic/aec-iot/b3/ equipe_blondel_martin/piBM /sensors/temperature/value

**Commande DEL:** ahuntsic/aec-iot/b3/ equipe_blondel_martin/piBM /actuators/led/cmd

**État DEL:** ahuntsic/aec-iot/b3/ equipe_blondel_martin/piBM /actuators/led/state

**Présence:** ahuntsic/aec-iot/b3/ equipe_blondel_martin/piBM /status/online
<br>
<br>

## 3. Exemples de JSON
**JSON pour la mesure de la température du CPU:** 
{
"device": "piBM",
"sensor": "CPU",
"value": 47.00,
"unit": "C",
"ts": "2026-02-25T19:22:10.123Z"
}

**JSON pour l'état de la DEL:**
{
"device": "piBM",
"actuator": "led",
"state": "on",
"ts": "2026-02-25T19:23:01.501Z"
}
<br>
<br>

## 4. Procédure d'installation
**Étape 1:** Importer les fichiers à partir de GitHub et les mettre dans un dossier
**Étape 2:** Créer un venv dans le dossier où se trouvent les fichiers
**Étape 3:**  Dans un terminal pyhton, écrire la commande pip install -r requirement.txt
<br>
<br>

## 5. Procédure de vérification du mosquitto sub/pub
<br>
<br>

## 6. Prodcédure de vérification du MariaDB

