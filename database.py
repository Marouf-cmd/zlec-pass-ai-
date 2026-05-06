import sqlite3
import os
from datetime import datetime
from logger import logger

DB_NAME = "zlecaf.db"

def get_db_path():
    return os.path.join(os.path.dirname(__file__), DB_NAME)

def init_db():
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    # Table des commerçants
    c.execute('''CREATE TABLE IF NOT EXISTS commercants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE NOT NULL,
        score INTEGER DEFAULT 0
    )''')
    # Table des certifications
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
    conn.commit()
    conn.close()

def ajouter_commercant(nom):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO commercants (nom) VALUES (?)", (nom,))
        conn.commit()
    except Exception as e:
        logger.error(f"Erreur base de données : {e}")
    finally:
        conn.close()

def incrementer_score(nom):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute("UPDATE commercants SET score = score + 1 WHERE nom = ?", (nom,))
    conn.commit()
    conn.close()

def enregistrer_certification(nom_commercant, produit, grade, origine, destination, economie, hash_signature):
    conn = sqlite3.connect(get_db_path())
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
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute("SELECT nom, score FROM commercants ORDER BY score DESC LIMIT ?", (limit,))
    data = c.fetchall()
    conn.close()
    return data

def get_certifications():
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('''SELECT c.produit, c.grade, c.origine, c.destination, c.economie, c.horodatage, cm.nom
                 FROM certifications c JOIN commercants cm ON c.commercant_id = cm.id
                 ORDER BY c.horodatage DESC''')
    data = c.fetchall()
    conn.close()
    return data
