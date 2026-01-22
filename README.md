# osint.ig – Instagram OSINT Tool

> 🕵️ Instagram OSINT Tool (No Login Required)

**osint.ig** este un tool OSINT (Instagram) (Open Source Intelligence) scris în Python, destinat colectării de informații **doar din surse publice Instagram**, fără autentificare, fără bypass-uri și fără exploatarea conturilor private.

Tool-ul este gândit pentru:

* OSINT researchers
* CTF / training
* educație
* analiză de profiluri publice

---

## ✨ Features

* 🔍 Colectare informații profil public
* ⬇️ Descărcare **toate postările publice** (imagini + video)
* 🧠 Analiză BIO (email-uri, link-uri)
* 🗓 Timeline postări (date, like-uri)
* 🎨 Hacker-style CLI (verde, cyan, typing effect)
* 💻 Compatibil Linux / Windows / Termux
* ❌ Fără login

---

## ⚠️ Disclaimer

Acest tool este creat **strict pentru scopuri educaționale și OSINT legal**.

* ❌ NU sparge conturi
* ❌ NU accesează conturi private
* ❌ NU face brute-force

Autorul nu este responsabil pentru folosirea abuzivă sau ilegală a acestui tool.

---

## 🛠 Requirements

* Python **3.8+**
* Internet connection

### Librării necesare

```bash
pip install instaloader colorama
```

---

## 🚀 Instalare

```bash
git clone https://github.com/ionutivan21/osint.ig.git
cd osint.ig
pip install -r requirements.txt
```

(sau instalare manuală a librăriilor de mai sus)

---

## ▶️ Rulare

```bash
python insta_osint.py
```

După rulare:

1. Introduci username-ul Instagram
2. Alegi opțiunea din meniu

---

## 📋 Meniu

```
[1] Profile information
[2] Download ALL public posts
[3] Bio OSINT (emails / links)
[4] Posts timeline
[0] Exit
```

---

## 📂 Unde se salvează postările?

Postările descărcate sunt salvate automat în folderul:

```text
<username>_posts/
```

Exemplu:

```text
theozeciu_posts/
├── theozeciu_2023-11-04_UTC.jpg
├── theozeciu_2023-10-28_UTC.mp4
└── ...
```

Folderul este creat **în directorul din care rulezi scriptul**.

---

## 🖥 Termux (Android)

Funcționează și pe Termux:

```bash
pkg install python
pip install instaloader colorama
python insta_osint.py
```

Recomandat:

* conexiune stabilă
* typing speed mic pentru performanță

---

## 🧩 Limitări cunoscute

* Instagram poate aplica **rate-limit** temporar
* Unele conturi mari pot necesita timp mai mare la download
* Fără login = acces doar la date publice

---

## 🧠 Tehnologii folosite

* Python 3
* instaloader
* colorama

---

## 👨‍💻 Autor

**ionutivan21**
GitHub: [https://github.com/ionutivan21](https://github.com/ionutivan21)

---

## ⭐ Contribuții

Pull requests sunt binevenite.
Idei de features:

* raport OSINT (JSON / TXT)
* hashtag intelligence
* progres bar
* structură media avansată

---

## 📜 License

MIT License
