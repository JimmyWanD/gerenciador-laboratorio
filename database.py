"""
Database module for Laboratorio Gerenciador
Handles SQLite database creation and operations
"""

import sqlite3
import os
from datetime import datetime

# Database path - will be in the same directory as the executable
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'laboratorio.db')


def get_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Initialize the database with all required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables for each category
    
    # Incidentes Colaboradores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidentes_colaboradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colaborador TEXT NOT NULL,
            tipo_incidente TEXT NOT NULL,
            descricao TEXT,
            data_hora DATETIME
        )
    ''')
    
    # Incidentes Amostra
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidentes_amostra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_amostra TEXT NOT NULL,
            tipo_problema TEXT NOT NULL,
            responsavel TEXT,
            descricao TEXT,
            data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Temperaturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temperaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bancada TEXT NOT NULL,
            temperatura REAL NOT NULL,
            data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Manutenção Equipamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manutencao_equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipamento TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('Controle', 'Calibração')),
            responsavel TEXT,
            descricao TEXT,
            data_manutencao DATETIME NOT NULL,
            proxima_manutencao DATETIME
        )
    ''')
    
    # Gerenciamento de Riscos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gerenciamento_riscos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            nivel TEXT CHECK(nivel IN ('Baixo', 'Médio', 'Alto')),
            acoes TEXT,
            data_identificacao DATETIME
        )
    ''')
    
    # Troca de Almotolias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS troca_almotolias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bancada TEXT NOT NULL,
            data_troca DATETIME NOT NULL,
            lote_reagente TEXT NOT NULL,
            proxima_troca DATETIME NOT NULL
        )
    ''')
    
    # Análise de Pendências
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analise_pendencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            prioridade TEXT CHECK(prioridade IN ('Baixa', 'Média', 'Alta')),
            data_limite DATETIME NOT NULL,
            status TEXT DEFAULT 'Pendente' CHECK(status IN ('Pendente', 'Concluído', 'Em Andamento')),
            data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def get_all_records(table_name):
    """Get all records from a specific table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if table has data_hora column
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = [col[1] for col in cursor.fetchall()]
    
    order_by = ''
    for col in ['data_hora', 'data_troca', 'data_manutencao', 'data_identificacao', 'data_criacao']:
        if col in columns:
            order_by = f' ORDER BY {col} DESC'
            break
    
    cursor.execute(f'SELECT * FROM {table_name}{order_by}')
    records = cursor.fetchall()
    conn.close()
    return records


def insert_record(table_name, data):
    """Insert a new record into a specific table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    values = list(data.values())
    
    query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return cursor.lastrowid


def update_record(table_name, record_id, data):
    """Update an existing record"""
    conn = get_connection()
    cursor = conn.cursor()
    
    set_clause = ', '.join([f'{key} = ?' for key in data.keys()])
    values = list(data.values())
    values.append(record_id)
    
    query = f'UPDATE {table_name} SET {set_clause} WHERE id = ?'
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def delete_record(table_name, record_id):
    """Delete a record from a specific table"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table_name} WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()


def search_records(table_name, search_term, search_field=None):
    """Search records in a table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get date column for ordering
    cursor.execute(f'PRAGMA table_info({table_name})')
    all_columns = [col[1] for col in cursor.fetchall()]
    
    order_by = ''
    for col in ['data_hora', 'data_troca', 'data_manutencao', 'data_identificacao', 'data_criacao']:
        if col in all_columns:
            order_by = f' ORDER BY {col} DESC'
            break
    
    if search_field:
        query = f'SELECT * FROM {table_name} WHERE {search_field} LIKE ?{order_by}'
        cursor.execute(query, (f'%{search_term}%',))
    else:
        # Search in all text fields
        text_columns = [col[1] for col in cursor.execute(f'PRAGMA table_info({table_name})').fetchall() if col[2] == 'TEXT']
        if text_columns:
            like_clauses = ' OR '.join([f'{col} LIKE ?' for col in text_columns])
            query = f'SELECT * FROM {table_name} WHERE {like_clauses}{order_by}'
            cursor.execute(query, tuple([f'%{search_term}%'] * len(text_columns)))
        else:
            cursor.execute(f'SELECT * FROM {table_name}{order_by}')
    
    records = cursor.fetchall()
    conn.close()
    return records


def get_table_columns(table_name):
    """Get column names for a table"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()
    return columns


if __name__ == '__main__':
    initialize_database()
    print("Database initialized successfully!")
