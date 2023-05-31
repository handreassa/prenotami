# Prenotami schedule helper
Python bot to log into [prenot@mi](prenotami.esteri.it) and schedule citizenship/passport using Selenium.

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
