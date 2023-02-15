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
    touch .env
    ```

- Modify the parameters.yaml file to fit your specific needs.

- Add username and password to log in to prenota in the .env file.

- Add a file called residencia.pdf under the files folder to be uploaded in the scheduling process. For passport there is also a need to add the identity file in the same folder, named identidade.pdf.

---

Feel free to contribute/ make your changes to the code.