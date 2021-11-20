import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, app
)
from werkzeug.exceptions import abort

from clubedabengala.auth import abort_if_not_in_role, login_required
from clubedabengala.db import get_db

bp = Blueprint('usuario', __name__)

@bp.route('/usuario')
@login_required
def index():
    abort_if_not_in_role("Colaborador")
    db = get_db()
    usuarios = db.execute(
        'SELECT e.id, e.created, e.solicitacao_id, u.username'
        ' FROM emprestimos e'
        ' JOIN users u ON e.dest_user_id = u.id'
        ' ORDER BY e.created DESC'
    ).fetchall()
    return render_template('usuario/index.html', usuarios=usuarios)


@bp.route('/usuario/<int:id>')
@login_required
def details(id):
    u = get_usuario(id)
    beneficiario = "Beneficiario" in session['roles']
    return render_template('usuario/details.html', u=u, beneficiario = beneficiario)

def get_usuario(id):
    db = get_db()
    u = db.execute(
        'SELECT u.id, u.username, u.name, u.email, u.mobilenumber'
        ' FROM users u'
        ' WHERE u.id = ?',
        (id,)
    ).fetchone()

    if u is None:
        abort(404, f"Empréstimo não existe")
    
    return u

@bp.route('/usuario/<int:id>/addresses', methods=['GET', 'POST'])
@login_required
def addresses(id):
    db = get_db()
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        street = request.form['street']
        number = request.form['number']
        complement = request.form['complement']
        city = request.form['city']
        state = request.form['state']
        address_id = request.form['address_id']
        if (address_id):
            db.execute(
                'UPDATE addresses set zipcode = ?, street = ?, number = ?, complement = ?, city = ?, state = ?'
                ' WHERE id = ?',
                (zipcode, street, number, complement, city, state, address_id)
            )
            db.commit()
        else:
            db.execute(
                'INSERT INTO addresses (zipcode, street, number, complement, city, state, user_id, active)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, 1)',
                (zipcode, street, number, complement, city, state, id)
            )
            db.commit()
    
    addresses = db.execute(
        'SELECT a.id, a.zipcode, a.street, a.number, a.complement, a.city, a.state'
        ' FROM addresses a'
        ' WHERE a.user_id = ? and a.active = 1',
        (id,)
    ).fetchall()
    return render_template('usuario/addresses.html', addresses = addresses)


@bp.route('/usuario/<int:id>/addresses/<int:aid>/remove', methods=['GET', 'POST'])
@login_required
def address_remove(id, aid):
    db = get_db()
    db.execute( 'UPDATE addresses set active = 0 where id = ?', (aid, ))
    db.commit()
    return redirect(url_for('usuario.addresses', id = id))




#################
# BENEFICIARIOS #
#################

@bp.route('/usuario/<int:id>/beneficiarios', methods=['GET', 'POST'])
@login_required
def beneficiarios(id):
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        dataNascimento = datetime.datetime.strptime(request.form['dataNascimento'], '%d-%m-%Y')
        altura = request.form['altura'].replace(',', '.')
        peso = request.form['peso'].replace(',', '.')
        nrCalcado = request.form['nrCalcado']
        beneficiario_id = request.form['beneficiario_id']
        if (beneficiario_id):
            db.execute(
                'UPDATE beneficiarios set name = ?, dataNascimento = ?, altura = ?, peso = ?, nrCalcado = ?'
                ' WHERE id = ?',
                (name, dataNascimento, altura, peso, nrCalcado, beneficiario_id)
            )
            db.commit()
        else:
            db.execute(
                'INSERT INTO beneficiarios (responsavel_id, name, dataNascimento, altura, peso, nrCalcado, active)'
                ' VALUES (?, ?, ?, ?, ?, ?, 1)',
                (id, name, dataNascimento, altura, peso, nrCalcado)
            )
            db.commit()
    
    beneficiarios = db.execute(
        "SELECT b.id, b.name, strftime('%d-%m-%Y', b.dataNascimento) dataNascimento, b.altura, b.peso, b.nrCalcado"
        ' FROM beneficiarios b'
        ' WHERE b.responsavel_id = ? and b.active = 1',
        (id,)
    ).fetchall()
    return render_template('usuario/beneficiarios.html', beneficiarios = beneficiarios)

@bp.route('/usuario/<int:id>/beneficiarios/<int:bid>/remove', methods=['GET', 'POST'])
@login_required
def beneficiarios_remove(id, bid):
    db = get_db()
    db.execute( 'UPDATE beneficiarios set active = 0 where id = ?', (bid, ))
    db.commit()
    return redirect(url_for('usuario.beneficiarios', id = id))


###############
# EMPRÉSTIMOS #
###############

@bp.route('/usuario/<int:id>/emprestimos', methods=['GET', 'POST'])
@login_required
def emprestimos(id):
    db = get_db()
    emprestimos = db.execute(
        'SELECT e.id, e.created, e.status, est.status status_name,'
        ' e.solicitante_id, sol.name solicitante_name, e.beneficiario_id, ben.name beneficiario_name'
        ' FROM emprestimos e'
        ' JOIN users sol ON sol.id = e.solicitante_id'
        ' JOIN beneficiarios ben ON ben.id = e.beneficiario_id'
        ' JOIN emprestimos_status est on est.id = e.status'
        ' WHERE sol.id = ?',
        (id,)
    ).fetchall()
    return render_template('usuario/emprestimos.html', emprestimos = emprestimos)