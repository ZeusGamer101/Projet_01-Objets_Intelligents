# READ ME - TP1 du cours de *Développement d'objets intelligents*
<br>
<br>

## 1. Architecture du projet
<br>
<br>

## 2. Covention de topics
**Préfixe unique:** ahuntsic/aec-iot/b3/equipe_blondel_martin/piBM<br>

**Télémetrie JSON:** ahuntsic/aec-iot/b3/equipe_blondel_martin/piBM/sensors/temperature<br>

**Valeur brute:** ahuntsic/aec-iot/b3/ equipe_blondel_martin/piBM /sensors/temperature/value<br>

**Commande DEL:** ahuntsic/aec-iot/b3/ equipe_blondel_martin/piBM /actuators/led/cmd<br>

**État DEL:** ahuntsic/aec-iot/b3/ equipe_blondel_martin/piBM /actuators/led/state<br>

**Présence:** ahuntsic/aec-iot/b3/ equipe_blondel_martin/piBM /status/online<br>
<br>
<br>

## 3. Exemples de JSON
**JSON pour la mesure de la température du CPU:** <br>
{
"device": "piBM",<br>
"sensor": "CPU",<br>
"value": 47.00,<br>
"unit": "C",<br>
"ts": "2026-02-25T19:22:10.123Z"<br>
}

**JSON pour l'état de la DEL:** <br>
{
"device": "piBM",<br>
"actuator": "led",<br>
"state": "on",<br>
"ts": "2026-02-25T19:23:01.501Z"<br>
}
<br>
<br>

## 4. Procédure d'installation
**Étape 1**: Installer Mosquitto (broker) et les clients avec cette ligne de commande: *sudo apt install -y mosquitto mosquitto-clients*<br>
**Étape 2**: Démarrer le service avec cette ligne de commande: *sudo systemctl enable --now mosquitto*<br>
**Étape 3**: Vérifier que le servoce tourne avec cette ligne de commande: *systemctl status mosquitto --no-pager*<br>
**Étape 4**: Vérifier le port MQTT avec cette ligne de commande: *sudo ss -lntp | grep 1883*<br>
**Étape 5:** Importer les fichiers à partir de GitHub et les mettre dans un dossier<br>
**Étape 6:** Créer un venv dans le dossier où se trouvent les fichiers<br>
**Étape 7:**  Dans un terminal python, écrire la commande pip install -r requirement.txt<br>
<br>
<br>

## 5. Procédure de vérification du mosquitto sub/pub
Pour tester le **publisher**, il faut mettre cette ligne de code dans un terminal: *mosquitto_pub -h localhost -t 'test/hello' -m 'Bonjour MQTT'* <br>
Pour tester le **subscriber**, il faut mettre cette ligne de code dans un autre terminal: *mosquitto_sub -h localhost -t 'test/hello' -v*
<br>
<br>

## 6. Prodcédure de vérification du MariaDB

