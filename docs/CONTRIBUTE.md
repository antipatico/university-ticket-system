# Developer Guide
## Tecnologie utilizzate
* **Python 3.8**: utilizzato per lo sviluppo del backend
* **VueJS 3.0**: utilizzato per lo sviluppo responsive del frontend
* **JQuery 3.6**: utilizzato come libreria base per javascript del il frontend
* **Bootstrap 5**: layout di base css+js per sviluppo responsive e mobile friendly del frontend
* **Shibboleth2**: modulo Apache2 per l'autenticazione con il SSO UniMore.

### Dipendenze Python
* **Django=3,<4**: framework di base per lo sviluppo del frontend
* **djangorestframework~=3.12.4**: estensione di Django per l'implementazione di REST API
* **django-polymorphic**: estensione di Django che permette la creazione di modelli polimorfici.
  Questa libreria semplifica l'implementazione di proprietario del ticket, che può essere sia una
  organizzazione che un individuo.
* **django-crispy-forms~=1.11.2**: estensione di Django che permette di creareform DRY
  (Don't Repeat Yourself), con la minor quantità di codice di templating possibile.
* **crispy-bootstrap5**: estensione per bootstrap5 per django-crispy-forms.
* **django-q**: libreria utilizzata per la schedulazione degli eventi.
* **redis**: utilizzata da django-q per la comunicazione tra backend e cluster 
  di scheduling (`qcluster`).
* **croniter**: dipendenza di django-q per la schedulazione con regole cron-like.
* **django-ses**: utilizzato per l'invio di email tramite il servizio Amazon 
  AWS Simple Email Service.
* **python-docx**: libreria utilizzata per la generazione dei report `.docx`.

### Dipendenze Bootstrap
* **Bootstrap Icons 1.5**: fornisce le icone utilizzate per il frontend


## Features
* Login con SSO unimore
* Login utenti locali (debug/amministrazione) al link
https://qaticket.ing.unimore.it/s3cr3tl0g1n
* Configurazione Apache (reverse proxy + shibboleth + file statici + uploads)
* Pannello Amministrazione di base di Django
* API Rest
* Creazione e chiusura di Ticket
* Dettaglio ticket: visualizzazione e creazione di un nuovo evento
* Dettaglio ticket: possibilità di sottoscriversi ai ticket
* Eventi ticket: Apertura, Chiusura, Note, Informazioni Richieste,
Duplicato, Escalation.
* Tags
* Organizzazioni: visualizzazione e gestione delle organizzazioni
(aggiunta / rimozione utenti da parte dell'amministratore
dell'organizzazione)
* Creazione ticket come organizzazione
* Scheduling degli eventi
* Schedulazione creazione ticket
* Allegati
* Schedulazione eventi con allegati
* Schedulazione cancellazione degli allegati non utilizzati
* Invio notifiche via mail con postfix
* Invio notifiche via mail con AWS
* Schedulazione invio notifiche via mail per non impallare il server web
* Client responsive
* Index con attività recenti, ticket creati e seguiti
* Mobile friendly

## Organizzazione del codice

Il codice risiede nella cartella **[uts](/uts)**