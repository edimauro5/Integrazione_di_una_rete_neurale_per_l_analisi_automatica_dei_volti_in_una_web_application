Si riportano di seguito i passi necessari per il corretto funzionamento del portale web

# INSTALLAZIONI:

`python 3.7`

Successivamente utilizzare pip install ...

* `tensorflow==1.14.0`
* `keras==2.3.1`
* `numpy==1.16.4 (non necessario)`
* `opencv-python`
* `h5py==2.10.0`
* `django`
* `psycopg2`
* `pillow`
* `django-mathfilters`

# PROCEDIMENTO PER PREDISPORRE CORRETTAMENTE IL PORTALE:

1. creare un database sul sistema PostgreSQL chiamato `IC` con amministratore `www` e password `tsw2021`

2. eseguire su pgAdmin per il database creato:

    * script di crezione delle tabelle `creazionedb.sql`
	* script di creazione dei trigger `trigger_prestazioni.sql`

3. muoversi nel prompt nella cartella `Web_Portal` e digitare in sequenza:

	> ***ATTENZIONE***: una volta finiti i passaggi non chiudere il prompt

	* `py manage.py makemigrations`
	* `py manage.py migrate ImageClassifier --fake`
	* `py manage.py migrate`
	* `py manage.py createsuperuser` (inserendo i campi richiesti)

4. eseguire su pgAdmin lo script di popolamento del database `popolamento.sql`

5. nel prompt utilizzato nel passaggio tre digitare il comando `py manage.py runserver`

6. visualizzare il portale digitando sul browser l'indirizzo "http://localhost:8000/ImageClassifier/Homepage"

## *NOTE IMPORTANTI*:

1. è possibilie accedere alla sezione relativa all'admin tramite il seguente URL: "http://localhost:8000/admin/" accedendo con il superuser creato precedentemente

2. nei successivi accessi al portale dopo averlo configurato nel modo sopra descritto, è possibile aprirlo e runnare il server facendo doppio clic su `Avvia con Chrome.bat` o `Avvia con Edge.bat` posizionati nella cartella `Web_Portal`









 