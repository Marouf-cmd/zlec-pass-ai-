import sqlite3
from datetime import datetime
import os
from core.config import PROJECT_DIR
from core.logger import logger
from werkzeug.security import generate_password_hash, check_password_hash

# Chemin unique vers la base de données
DB_NAME = os.path.join(PROJECT_DIR, "zlecaf.db")

def get_db_path():
    """Retourne le chemin de la base de données (compatibilité)"""
    return DB_NAME

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table des commerçants (existante)
    c.execute('''CREATE TABLE IF NOT EXISTS commercants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE NOT NULL,
        score INTEGER DEFAULT 0
    )''')
    # Table des certifications (existante)
    c.execute('''CREATE TABLE IF NOT EXISTS certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        commercant_id INTEGER,
        produit TEXT,
        grade TEXT,
        origine TEXT,
        destination TEXT,
        economie TEXT,
        hash_signature TEXT,
        horodatage TEXT,
        FOREIGN KEY (commercant_id) REFERENCES commercants(id)
    )''')
    # Table des utilisateurs (nouvelle)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'commercant'
    )''')
    init_default_users()
    conn.commit()
    conn.close()

def add_user(username, password, role='commercant'):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hashed = generate_password_hash(password)
    try:
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)", (username, hashed, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        logger.error(f"Utilisateur {username} existe déjà")
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password_hash, role FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and check_password_hash(row[0], password):
        return {"username": username, "role": row[1]}
    return None
def init_default_users():
    """Crée les utilisateurs par défaut (admin et douane) s'ils n'existent pas."""
    from core.database import verify_user, add_user  # éviter les imports circulaires
    if not verify_user('admin', 'admin123'):
        add_user('admin', 'admin123', 'admin')
    if not verify_user('douane', 'douane123'):
        add_user('douane', 'douane123', 'douane')

def ajouter_commercant(nom):
    conn = sqlite3.connect(DB_NAME)   # modifié
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO commercants (nom) VALUES (?)", (nom,))
        conn.commit()
    except Exception as e:
        logger.error(f"Erreur base de données : {e}")
    finally:
        conn.close()

def incrementer_score(nom):
    conn = sqlite3.connect(DB_NAME)   # modifié
    c = conn.cursor()
    c.execute("UPDATE commercants SET score = score + 1 WHERE nom = ?", (nom,))
    conn.commit()
    conn.close()

def enregistrer_certification(nom_commercant, produit, grade, origine, destination, economie, hash_signature):
    conn = sqlite3.connect(DB_NAME)   # modifié
    c = conn.cursor()
    # Récupérer l'id du commerçant (ou le créer)
    c.execute("SELECT id FROM commercants WHERE nom = ?", (nom_commercant,))
    row = c.fetchone()
    if row is None:
        c.execute("INSERT INTO commercants (nom) VALUES (?)", (nom_commercant,))
        commercant_id = c.lastrowid
    else:
        commercant_id = row[0]
    horodatage = datetime.now().isoformat()
    c.execute('''INSERT INTO certifications (commercant_id, produit, grade, origine, destination, economie, hash_signature, horodatage)
                 VALUES (?,?,?,?,?,?,?,?)''',
              (commercant_id, produit, grade, origine, destination, economie, hash_signature, horodatage))
    conn.commit()
    conn.close()
    # Incrémenter le score
    incrementer_score(nom_commercant)

def get_top_commercants(limit=10):
    conn = sqlite3.connect(DB_NAME)   # modifié
    c = conn.cursor()
    c.execute("SELECT nom, score FROM commercants ORDER BY score DESC LIMIT ?", (limit,))
    data = c.fetchall()
    conn.close()
    return data

def get_certifications():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''SELECT c.produit, c.grade, c.origine, c.destination, c.economie, c.horodatage, cm.nom
                 FROM certifications c JOIN commercants cm ON c.commercant_id = cm.id
                 ORDER BY c.horodatage DESC''')
    data = c.fetchall()
    conn.close()
    return data