from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, app
)
from werkzeug.exceptions import abort

from clubedabengala.auth import abort_if_not_in_role, login_required
from clubedabengala.db import get_db

bp = Blueprint('manage', __name__)

from clubedabengala.usuario import get_equip_classifications, get_emprestimos


@bp.route('/equipamentos')
@login_required
def equipamentos():
    abort_if_not_in_role("Colaborador")
    equipamentos = get_equipamentos()
    return render_template('manage/equipamentos.html', equipamentos = equipamentos)

@bp.route('/equipamentos/create', methods=['GET', 'POST'])
@login_required
def equipamentos_create():
    abort_if_not_in_role("Colaborador")

    if request.method == "POST":
        status = request.form['status']
        obs = request.form['obs']
        equip_type = request.form['equip_type']
        equip_model = request.form['equip_model']
        equip_size = request.form.get('equip_size')
        db = get_db()
        result = db.execute("""
            INSERT INTO equipamentos
            (status, obs, equip_type, equip_model, equip_size)
            VALUES (?, ?, ?, ?, ?)
            """,
            (status, obs, equip_type, equip_model, equip_size)
        )
        db.commit()
        return redirect(url_for('manage.equipamentos_details', eid = result.lastrowid))



    viewmodel = {}
    viewmodel['equip_classifications'] = get_equip_classifications()
    return render_template('manage/equipamentos_create.html', viewmodel = viewmodel)

@bp.route('/equipamentos/<int:eid>')
@login_required
def equipamentos_details(eid):
    abort_if_not_in_role("Colaborador")
    e = get_equipamentos(eid = eid)[0]
    if e is None:
        abort(404, "Equipamento não encontrado!")
    return render_template('manage/equipamentos_details.html', e = e)

def get_equipamentos(**filter):
    query = """
        SELECT
            e.id
            , est.name status
            , et.id equip_type_id
            , et.name equip_type_name
            , em.model_num equip_model_num
            , em.name equip_model_name
            , em.image equip_model_image
            , es.id equip_size_id
            , es.desc equip_size_desc
            , e.obs
        FROM equipamentos e
        JOIN equipamentos_status est on est.id = e.status
        JOIN equip_types et on et.id = e.equip_type
        JOIN equip_models em on em.equip_type_id = e.equip_type and em.model_num = e.equip_model
        LEFT JOIN equip_sizes es on es.id = e.equip_size
    """
    filter_query = []
    params = []

    filter['active'] = 1

    if 'eid' in filter:
        filter_query.append('e.id = ?')
        params.append(filter['eid'])

    if 'disponivel' in filter:
        params.append(0)
        if filter['disponivel']:
            filter_query.append('e.status = ?')
        else:
            filter_query.append('e.status != ?')

    if 'equip_type' in filter:
        filter_query.append('e.equip_type = ?')
        params.append(filter['equip_type'])

    if 'equip_model' in filter:
        filter_query.append('e.equip_model = ?')
        params.append(filter['equip_model'])

    if 'equip_size' in filter:
        filter_query.append('e.equip_size = ?')
        params.append(filter['equip_size'])

    if len(filter_query) > 0:
        query += ' WHERE ' + " AND ".join(filter_query)

    return get_db().execute(query, tuple(params)).fetchall()



#################
## EMPRÉSTIMOS ##
#################


@bp.route('/emprestimos')
@login_required
def emprestimos():
    abort_if_not_in_role("Colaborador")
    emprestimos = get_emprestimos()
    return render_template('manage/emprestimos.html', emprestimos = emprestimos)


@bp.route('/emprestimos/<int:eid>')
@login_required
def emprestimos_details(eid):
    abort_if_not_in_role("Colaborador")
    e = get_emprestimos(eid = eid)[0]

    equipamentos = []
    viewmodel = {}
    # can_approve_or_reject = False
    if e['status_id'] == 0:
        viewmodel['can_approve_or_reject'] = True
        # can_approve_or_reject = True
        equipamentos = get_equipamentos(disponivel = True, equip_type = e['equip_type_id'], equip_model = e['equip_model_num'])

        if len(equipamentos) == 0:
            flash("Você não possuí equipamentos disponíveis deste modelo")
    elif e['status_id'] in [1, 4, 3, 5]:
        # aprovado, emprestado, cancelado ou finalizado
        viewmodel['can_mark_as_retirado'] = e['status_id'] == 1
        viewmodel['can_mark_as_finalizado'] = e['status_id'] == 4
        viewmodel['equipamento'] = get_equipamentos(eid = e['equip_id'])[0]

    return render_template('manage/emprestimos_details.html',
        e = e, equipamentos = equipamentos, **viewmodel)


@bp.route('/emprestimos/<int:eid>/approve', methods = ["POST"])
@login_required
def emprestimos_approve(eid):
    abort_if_not_in_role("Colaborador")
    db = get_db()
    equip_id = request.form.get('equip_id')
    emprestimo_status = 2 # negado
    if request.form['approved'] == u"true":
        emprestimo_status = 1 # aprovado

    db.execute('UPDATE emprestimos set status = ?, equip_id = ? where id = ?', (emprestimo_status, equip_id, eid))

    equip_status = 0 # disponivel
    if emprestimo_status == 1 and equip_id:
        equip_status = 4 # reservado
        db.execute('UPDATE equipamentos set status = ? where id = ?', (equip_status, equip_id))

    db.commit()

    return redirect(url_for('manage.emprestimos_details', eid = eid))

@bp.route('/emprestimos/<int:eid>/withdrawalled', methods = ["POST"])
@login_required
def emprestimos_withdrawalled(eid):
    abort_if_not_in_role("Colaborador")
    db = get_db()

    emprestimo_status = 4 # emprestado
    db.execute('UPDATE emprestimos set status = ? where id = ?', (emprestimo_status, eid))

    equip_id = db.execute('Select equip_id from emprestimos where id = ?', (eid,)).fetchone()[0]
    equip_status = 1 # emprestado
    print(equip_status, equip_id)
    db.execute('UPDATE equipamentos set status = ? where id = ?', (equip_status, equip_id))
    db.commit()

    return redirect(url_for('manage.emprestimos_details', eid = eid))

@bp.route('/emprestimos/<int:eid>/finalized', methods = ["POST"])
@login_required
def emprestimos_finalized(eid):
    abort_if_not_in_role("Colaborador")
    db = get_db()

    emprestimo_status = 5 # finalizado
    db.execute('UPDATE emprestimos set status = ? where id = ?', (emprestimo_status, eid))

    equip_id = db.execute('Select equip_id from emprestimos where id = ?', (eid,)).fetchone()[0]
    equip_status = 0 # disponivel
    print(equip_status, equip_id)
    db.execute('UPDATE equipamentos set status = ? where id = ?', (equip_status, equip_id))
    db.commit()

    return redirect(url_for('manage.emprestimos_details', eid = eid))