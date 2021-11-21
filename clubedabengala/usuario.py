import datetime
import json
from typing import Dict

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


###############
## ENDEREÇOS ##
###############

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
    
    beneficiarios = get_beneficiarios(uid = id)
    return render_template('usuario/beneficiarios.html', beneficiarios = beneficiarios)

@bp.route('/usuario/<int:id>/beneficiarios/<int:bid>/remove', methods=['GET', 'POST'])
@login_required
def beneficiarios_remove(id, bid):
    db = get_db()
    db.execute( 'UPDATE beneficiarios set active = 0 where id = ?', (bid, ))
    db.commit()
    return redirect(url_for('usuario.beneficiarios', id = id))


def get_beneficiarios(**filter):
    query = """
        SELECT
            b.id
            , b.name
            , strftime('%d-%m-%Y', b.dataNascimento) dataNascimento
            , b.altura
            , b.peso
            , b.nrCalcado
        FROM beneficiarios b
    """
    filter_query = []
    params = []

    filter['active'] = 1

    if 'uid' in filter:
        filter_query.append('b.responsavel_id = ?')
        params.append(filter['uid'])

    if 'active' in filter:
        filter_query.append('b.active = ?')
        params.append(filter['active'])

    if len(filter_query) > 0:
        query += ' WHERE ' + " AND ".join(filter_query)

    return get_db().execute(query, tuple(params)).fetchall()
    

# @bp.route('/usuario/<int:id>/becomebeneficiario', methods=['GET', 'POST'])
# @login_required
# def become_beneficiario(id):
#     pass





###############
# EMPRÉSTIMOS #
###############

@bp.route('/usuario/<int:id>/emprestimos', methods=['GET'])
@login_required
def emprestimos(id):
    emprestimos = get_emprestimos(uid = id)
    return render_template('usuario/emprestimos.html', emprestimos = emprestimos)

@bp.route('/usuario/<int:id>/emprestimos/<int:eid>', methods=['GET', 'POST'])
@login_required
def emprestimos_details(id, eid):
    e = get_emprestimos(eid = eid)[0]
    if e is None:
        abort(404, "Empréstimo não existe")
    return render_template('usuario/emprestimos_details.html', e = e)

def get_emprestimos(**filter):
    db = get_db()
    query = """
        SELECT
            e.id
            , e.created
            , est.id status_id
            , est.status
            , u.id solicitante_id
            , u.name solicitante_name
            , b.id beneficiario_id
            , b.name beneficiario_name
            , a.id address_id
            , a.street || ' ' || cast(a.number as varchar) || ' ' || a.complement || ' - ' || a.city || ' ' || a.state address
            , strftime('%d/%m/%Y', e.data_inicio) data_inicio
            , strftime('%d/%m/%Y', e.data_fim) data_fim
            , e.motivo
            , e.obs
            , et.id equip_type_id
            , et.name equip_type_name
            , em.model_num equip_model_num
            , em.name equip_model_name
            , em.image equip_model_image
            , es.id equip_size_id
            , es.desc equip_size_desc
        FROM emprestimos e
        JOIN emprestimos_status est on est.id = e.status
        JOIN users u on u.id = e.solicitante_id
        JOIN beneficiarios b on b.id = e.beneficiario_id
        JOIN addresses a on a.id = e.address_id
        JOIN equip_types et on et.id = e.equip_type
        JOIN equip_models em on em.model_num = e.equip_model and em.equip_type_id = et.id
        LEFT JOIN equip_sizes es on es.id = e.equip_size
    """

    filter_query = []
    params = []

    if 'eid' in filter:
        filter_query.append('e.id = ?')
        params.append(filter['eid'])
    if 'uid' in filter:
        filter_query.append('e.solicitante_id = ?')
        params.append(filter['uid'])
    
    if len(filter_query) > 0:
        query += ' WHERE ' + " AND ".join(filter_query)

    return db.execute(query, tuple(params)).fetchall()


@bp.route('/usuario/<int:id>/emprestimos/create', methods=['GET', 'POST'])
@login_required
def emprestimos_create(id):
    db = get_db()

    if request.method == "POST":
        beneficiario_id = request.form['beneficiario_id']
        address_id = request.form['address_id']
        dataInicio = datetime.datetime.strptime(request.form['dataInicio'], '%d/%m/%Y')
        dataFim = datetime.datetime.strptime(request.form['dataFim'], '%d/%m/%Y')
        motivo = request.form['motivo']
        obs = request.form['obs']
        equip_type = request.form['equip_type']
        equip_model = request.form['equip_model']
        equip_size = request.form.get('equip_size')
        result = db.execute(
            'INSERT INTO emprestimos'
            ' (status, solicitante_id, beneficiario_id, address_id, data_inicio, data_fim, motivo, obs, equip_type, equip_model, equip_size)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (0, id, beneficiario_id, address_id, dataInicio, dataFim, motivo, obs, equip_type, equip_model, equip_size)
        )
        db.commit()
        return redirect(url_for('usuario.emprestimos_details', id = id, eid = result.lastrowid))


    viewmodel = {}
    viewmodel['beneficiarios'] = get_user_beneficiarios(id)
    viewmodel['addresses'] = get_user_addresses(id)
    viewmodel['equip_classifications'] = get_equip_classifications()

    if (len(viewmodel['beneficiarios']) == 0):
        flash(f"Você não possui beneficiários cadastrados. <a href='{url_for('usuario.beneficiarios', id = id)}'>Cadastre aqui</a>")

    if (len(viewmodel['addresses']) == 0):
        flash(f"Você não possui um endrereço cadastrado. <a href='{url_for('usuario.addresses', id = id)}'>Cadastre aqui</a>")

    # print(json.dumps(get_equip_classifications()))

    return render_template('usuario/emprestimos_create.html', viewmodel = viewmodel)



def get_user_beneficiarios(id):
    db = get_db()
    a = db.execute(
        "SELECT b.id, b.name, strftime('%d-%m-%Y', b.dataNascimento) dataNascimento, b.altura, b.peso, b.nrCalcado"
        ' from beneficiarios b where responsavel_id = ? and b.active = 1'
        , (id,)).fetchall()
    return a


def get_user_addresses(id):
    db = get_db()
    a = db.execute('SELECT * FROM addresses where user_id = ? and active = 1', (id,)).fetchall()
    return a

def get_equip_classifications():
    db = get_db()
    ret = []
    types = db.execute('SELECT id, name FROM equip_types').fetchall()
    for type in types:
        t = {'id': type['id'], 'name': type['name'], 'models': []}
        models = db.execute('SELECT * from equip_models where equip_type_id = ?', (type['id'],)).fetchall()
        for model in models:
            m = {'num': model['model_num'], 'name': model['name'], 'image': url_for('static', filename="images/" + model['image']), 'sizes': None}
            sizes = db.execute('SELECT * from equip_sizes where equip_type_id = ? and equip_model_num = ?', (type['id'], model['model_num'])).fetchall()
            m['sizes'] = [{'desc': s['desc'], 'id': s['id']} for s in sizes]
            t['models'].append(m)

        ret.append(t)

    return ret

def get_equip_classifications_2():
    db = get_db()
    ret = []
    results = db.execute(
        'SELECT m.equip_type_id type_id, t.name type_name, m.model_num, m.name model_name, s.desc size FROM equip_types t'
        ' JOIN equip_models m on m.equip_type_id = t.id'
        ' LEFT JOIN equip_sizes s on s.equip_type_id = t.id and s.equip_model_num = m.model_num'
        ' ORDER BY t.id, m.model_num'
    ).fetchall()
    print(results)

    return results

