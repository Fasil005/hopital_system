# Patient Interoperability Gateway (PIGW)

## Setup & Run

### Build Docker Image

```bash
docker compose build
```

### Start Containers

```bash
docker compose up
```

Run in background:

```bash
docker compose up -d
```

### Apply Migrations

```bash
docker compose exec web python manage.py migrate
```

---

## Fernet Encryption Usage

Sensitive fields such as **SSN** and **Passport** are encrypted using **Fernet symmetric encryption** from the `cryptography` library.

### How It Works

- Encryption key is stored in `.env` as `FERNET_KEY`
- Sensitive values are encrypted before saving to the database
- Encrypted values are stored securely
- During retrieval, values are decrypted
- Before returning in the API response, values are masked

### Generate Fernet Key

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Add the generated key to your `.env` file:

```
FERNET_KEY=your_generated_key
```

---