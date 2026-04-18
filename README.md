<div align="center">

```
 ██████╗ ██████╗  █████╗ ███████╗███████╗
██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
██║   ██║██████╔╝███████║███████╗███████╗
██║▄▄ ██║██╔═══╝ ██╔══██║╚════██║╚════██║
╚██████╔╝██║     ██║  ██║███████║███████║
 ╚══▀▀═╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
```

# 🔐 QPass — Secure CLI Password Manager

**Encrypt. Store. Retrieve. Sleep easy.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas%20Ready-green?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-qpass-orange?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/qpass)
[![Cryptography](https://img.shields.io/badge/Encryption-PBKDF2%20%2B%20Fernet-red?style=flat-square&logo=letsencrypt&logoColor=white)](https://cryptography.io)

</div>

---

## ✨ What is QPass?

**QPass** is a lightweight, terminal-first password manager that keeps your credentials safe using industry-standard encryption — all stored securely in MongoDB. No browser plugins. No cloud accounts. Just you, your terminal, and your encrypted vault.

> 💡 Built for developers and power users who live in the terminal.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🔒 **Military-grade encryption** | PBKDF2 key derivation + Fernet symmetric encryption |
| 🖥️ **Interactive CLI** | Clean, intuitive command-line interface |
| 🔑 **Session-based auth** | Login once per session — no repeated prompts |
| 🗄️ **MongoDB storage** | Scalable, reliable backend for your vault |
| 🧩 **Simple commands** | Minimal syntax, maximum productivity |
| 🌍 **Cross-platform** | Works on Linux, macOS, and Windows |

---

## 📦 Installation

```bash
pip install qpass
```

> Requires Python 3.8+ and a running MongoDB instance (local or Atlas).

---

## ⚡ Quick Start

```bash
# Launch QPass
qpass

# Register / login to your vault
ulogin

# Add a credential
add github MyS3cur3P@ss!

# Retrieve it anytime
get_site github

# View your entire vault
get_vault

# Logout safely
ulogout
```

---

## 🛠️ Commands

```
┌────────────────────────────────────────────────────────┐
│                    QPASS COMMANDS                      │
├──────────────────────┬─────────────────────────────────┤
│  ulogin              │  Authenticate into your vault   │
│  ulogout             │  End your current session       │
│  add <site> <pass>   │  Save encrypted credentials     │
│  delete <site>       │  Remove a saved entry           │
│  get_vault           │  List all stored sites          │
│  get_site <site>     │  Retrieve a specific password   │
└──────────────────────┴─────────────────────────────────┘
```

---

## 🔐 How Encryption Works

QPass uses a **two-layer security model**:

```
Master Password
      │
      ▼
  PBKDF2-HMAC-SHA256
  (100,000 iterations + salt)
      │
      ▼
  256-bit Derived Key
      │
      ▼
  Fernet Symmetric Encryption
      │
      ▼
  Encrypted Ciphertext → MongoDB
```

1. Your master password is **never stored** — only a salted hash.
2. Every password is encrypted using **Fernet** before touching the database.
3. Decryption only happens **in memory**, during an active session.

---

## 🧱 Tech Stack

```
┌─────────────────────────────────────────┐
│  Language     →  Python 3.8+            │
│  Database     →  MongoDB                │
│  Encryption   →  cryptography (Fernet)  │
│  CLI          →  cmd / argparse         │
│  Auth         →  PBKDF2-HMAC-SHA256     │
└─────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
qpass/
├── qpass/
│   ├── __init__.py
│   ├── cli.py          # CLI entry point & command loop
│   ├── auth.py         # Session & user authentication
│   ├── crypto.py       # Encryption / decryption logic
│   ├── db.py           # MongoDB connection & queries
│   └── vault.py        # Vault operations (add/get/delete)
├── README.md
├── LICENSE
├── setup.py / pyproject.toml
└── requirements.txt
```

---

## 🔧 Requirements

```
pymongo
cryptography
```

Install them manually:

```bash
pip install pymongo cryptography
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch: `git checkout -b feature/cool-thing`
3. 💾 Commit your changes: `git commit -m "Add cool thing"`
4. 📤 Push and open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

<div align="center">

Made with 🔐 and ☕ by **Aditya**

*"Security is not a product, but a process."* — Bruce Schneier

</div>
