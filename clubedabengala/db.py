import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from werkzeug.security import check_password_hash, generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
def populate_db():
    db = get_db()
    db.execute(
        "INSERT INTO users (id, username, password, name, mobilenumber, email) VALUES (?, ?, ?, ?, ?, ?)",
        (1, 'lucas', generate_password_hash('123'), "Lucas Blotta", '11996786683', 'lucas@example.com'),
    )
    db.execute( "INSERT INTO user_roles (user_id, role_id) VALUES (1, 0)") # Colaborador

    db.execute(
        "INSERT INTO users (id, username, password, name, mobilenumber, email) VALUES (?, ?, ?, ?, ?, ?)",
        (2, 'roy', generate_password_hash('123'), "Roy Raynalds", '11996786684', 'roy@example.com'),
    )
    db.execute(
        'INSERT INTO addresses (user_id, zipcode, street, number, complement, city, state, active)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (2, '05652000', 'Av Roberto Marinho', 5219, 'C3', 'São Paulo', 'SP', 1),
    )
    # db.execute( "INSERT INTO user_roles (user_id, role_id) VALUES (2, 0)")

    # db.execute( "INSERT INTO solicitacoes (status, solicitante_id) VALUES (0, 1)")
    # db.execute( "INSERT INTO emprestimos (status, dest_user_id) VALUES (0, 1)")
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    populate_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)