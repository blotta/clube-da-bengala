import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from clubedabengala.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        mobilenumber = request.form['mobilenumber']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO users (username, name, mobilenumber, email, password)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (username, name, mobilenumber, email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError as e:
                error = f"Usuário inválido"
                if (str(e).find("mobilenumber")):
                    error = f"Número {mobilenumber} já existe {str(e)}"
                elif (str(e).find("username")):
                    error = f"Usuário {username} já existe {str(e)}"
                elif (str(e).find("email")):
                    error = f"Email {email} já existe {str(e)}"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Usuário inválido'
        elif not check_password_hash(user['password'], password):
            error = 'Senha inválida'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            roles = get_user_roles(user['id'])
            session['roles'] = roles
            if "Colaborador" in roles:
                return redirect(url_for('emprestimos.index'))
            return redirect(url_for('usuarios.details', id = user['id']))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
        g.roles = None
    else:
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        g.roles = get_user_roles(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def get_user_roles(user_id):
    roles = get_db().execute(
        'SELECT role FROM roles r'
        ' JOIN user_roles ur on ur.role_id = r.id'
        ' WHERE user_id = ?', (user_id,)
    ).fetchall()
    return [ r['role'] for r in roles]

def user_in_role(role):
    return role in session.get('roles')

def abort_if_not_in_role(role, update_roles = False):
    if update_roles:
        session['roles'] = get_user_roles(session.get('user_id'))
    if not user_in_role(role):
        abort(403, "Você não pode acessar este recurso")


# @app.route('/')
# def index():
#     uid = session.get('user_id')
#     if uid is None:
#         return redirect(url_for('auth.login'))

#     if user_in_role("Colaborador"):
#         return redirect(url_for('emprestimos.index'))
    
#     return redirect(url_for('usuarios.details', id = uid))