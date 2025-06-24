Hallo Herr Prof. Haase,

Ich hab selbst noch nicht mit Jupyter Notebook gearbeitet habe ihnen aber mal die Notebook Datei erstellt. Es funktioniert wahrscheinlich nur mit der richtigen Desktop Anwendung von Jupyter (ich konnte nicht das gesamte Projekt in die Browserbasierte Variante laden)
Darüber sollte man wenn man die 2 Zeilen ausführt folgendes bekommen (kann möglicherweise ein paar Sekunden dauernd um die Module zu indexen und zu konfigurieren):
- mein UserInterface direkt in JupyterNotebook (jedenfalls passiert das bei mir so)
- einen Link in der Ausgabekonsole von Jupyter (bei mir direkt über dem UI) dass sollte in etwas so aussehen:
* Running on local URL:  http://127.0.0.1:7860
* To create a public link, set `share=True` in `launch()`.
wenn sie auf den Link gehen sollte sich ihr Browser öffnen mit dem UI, ich vermute das läuft etwas stabiler als die Variante in Jupyter. 

Falls das gar nicht funktioniert, könnten sie noch python 3.12 rein installieren und es über die Konsole ausführen, es sollte aber mit Jupyter laufen. 
Falls das Programm Fehlermeldungen produziert liegt es vermutlich am Export des Enviroments, schreiben sie mir in dem Fall gern.

----UserInterface-----

Im UI ist ein Button mit "Simulation starten", wenn man die Ausgangsparameter im UI ändert muss man da clicken um die Diagramme zu updaten.

Die Parameter in der obersten Zeile sind ja laut idealer Gasgleichung voneinader abhängig, man kann daneben im Dropdown den Parameter auswählen, 
den man selbst nicht verändert und dann die anderen beiden beliebig setzen, die simulation berechnet dann den dritten Parameter.

Ansonsten ist es hoffe ich selbsterklärend, falls nicht geben sie mir da auch gern eine Rückmeldung, da kann die eigene Einschätzung ja schnell täuschen wenn man es selbst baut.

Vielen Dank für ihre Zeit und Flexibilität!

Mit freundlichen Grüßen, Joe Leonhardt