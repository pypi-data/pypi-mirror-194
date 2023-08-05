#mqtt_Thread <br />

Connexion à un server mqtt via un thread <br />
Envoi et réception des messages mqtt en Python <br />
Sauvegarde des données reçues au format csv <br />

INSTALLATION :<br />
		py -m pip mqtt_thread<br />
		ou <br />
		py -m pip mqtt_thread==x.x.x (mettre numéro de version)<br />

exemple :<br />
Trace de graphe mathPlotlib temps réel<br />

---------------------<br />

....................<br />
m = MQTT.MQTT_Thread("mqtt.url.fr",443,"username","pwd")        # crée le thread <br />
m.selectTopic(["node_iot2020/#","FABLAB/contes/bureau/temperature/out/"])  # topics auxquels on s'abonne <br />
#m.selectTopic(["node_iot2020/#"])  # topics auquel on s'abonne <br />
m.selectKey([["ecl","temps"],["temp","pression"]]) # selection des clés des données voulues , les données seront dans m.data[0][], m.data[1][],... <br />
# le dernier élement de m.data[i] est le temps de réception du messageen secondes (donné par python avec la fonction time) <br />
m.messageArrived = messageArrived # personnalisation fonction qui sera appelée à chaque réception de message <br />
m.nomFichier = "donnees" # nom du fichier csv sans extension qui enregistrera les données <br />
m.record = False # enregistre les données dans un fichier csv <br />
m.eraseFile = False # efface le fichier csv avant d'enregistrer les données <br />
m.verbose = True # affiche les messages MQTT <br />
m.start()                  # démarre le thread, (exécution indépendante du programme principal) <br />
time.sleep(1) <br />
#m.client.publish("node_iot2020/test/in",payload="{\"pression\":1024}",qos=0)#publication d'un message vers MQTT  <br />

# Appelle la fonction animation périodiquement <br />
#m.data[0][1] est une liste !!!<br />
ani = animation.FuncAnimation(fig, acquisition, fargs=(m.data[1][2], m.data[1][0]), frames=20,interval=1000,repeat=True)# intervall temps en ms entre 2 animations <br />
    #ani.save('video1.mp4', dpi=200, fps=15) <br />
plt.show() <br />

