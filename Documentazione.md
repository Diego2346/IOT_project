

**Progetto IOTBSS**

Diego Calabretta 1000012346

Il progetto consiste in un bot Telegram chiamato @capbot2021\_bot, scritto in Python, che permette di

ricevere alert di eventi critici, in particolare, di terremoti, alluvioni e incendi. Gli alert derivano da messaggi

CAP (Comunication Alert Protocol), un formato xml pensato per avvisi pubblici di emergenza, inviati ai

rispettivi topics.

Il bot, connesso ad un broker, al comando start permette di scegliere la tipologia di evento, di cui si vuole

essere avvertiti.

E’, inoltre possibile inviare la propria posizione e un raggio di azione per limitare le notifiche ad avvenimenti

entro una certa distanza. (In mancanza di questi parametri il bot notificherà di eventi indipendentemente

dalla loro posizione).

E’ possibile aggiungere o rimuovere eventi con il comando /mieiTopics e l’interfaccia a pulsanti che ne

consegue.





E’ possibile rimuovere la posizione e il raggio, qualora siano stati già inseriti, con il comando /miaPosizione

e il pulsante ‘RIMUOVI POSIZIONE E RAGGIO’

Ogni evento verrà notificato come di seguito, quindi con: un’immagine, nome evento, nome mittente,

entità, data e ora, descrizione, istruzioni, posizione dell’evento.





Nella cartella sono presenti: il codice Python (CAPBOT.PY), 4 esempi di messaggi CAP

(Terremoto\_Catania.xml, Terremoto\_Milano.xml, Alluvione\_Catania.xml, Incendio\_Messina.xml) e

README.txt

