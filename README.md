# Prenotami schedule helper
Python bot to log into [prenot@mi](prenotami.esteri.it) and schedule citizenship/passport using Selenium. ***I am no longer encouraging automating the login and schedule processes and will keep this repo just for reference.*** <br>

> **ATTENTION**<br>
> Moving this repo to public archive due to the last changes/ informations published here https://conscuritiba.esteri.it/it/servizi-consolari-e-visti/servizi-per-il-cittadino-italiano/altri-servizi/informativa-sui-servizi-consolari/:
>  ```L’efficienza del sistema centralizzato, già minato dagli abusi informatici dei ben noti despachantes è reso ancor più vulnerabile dal gigantesco incremento delle domande e anche dall’aumento degli utenti che si rivolgono alle società di intermediazione.```<br>
>[...]<br>
>```Per bloccare questo meccanismo ed evitare che si inneschino ulteriori sistemi di sfruttamento illegittimo dei diritti dei cittadini e degli aventi diritto, chiediamo il supporto e la fiducia nell’impegno del Consolato che, con tutte le forze a disposizione, fornisce molteplici servizi consolari e continua ad accogliere, con attenzione e cura, i legittimi reclami formulati in forma non offensiva o insinuante.```

---

## How to use it:

- Download this repo and create a virtual env. Make use of it and install the required libs.
    ```
    git clone https://github.com/handreassa/prenotami
    cd prenotami
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    mkdir files
    echo "username=ADD_USERNAME_HERE" > .env
    echo "password=ADD_PASSWORD_HERE" >> .env
    ```

- Modify the parameters.yaml file to fit your specific needs.

- Add username and password to log in to prenota in the .env file (substitute the ADD_USERNAME_HERE used in the above code).

- Add a file called **residencia.pdf** under the files folder to be uploaded in the scheduling process. This file has to demonstrate that you live in the address that is covered by the consulate you are trying to schedule. For example it can be utility bills (phone, electricity, etc). For passport there is also a need to add the identity file in the same folder, named **identidade.pdf**. 

---

Feel free to contribute/ make your changes to the code. Any questions feel free to raise an issue!
