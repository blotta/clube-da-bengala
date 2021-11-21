# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, url_for
# )
# from werkzeug.exceptions import abort

# from clubedabengala.auth import abort_if_not_in_role, login_required
# from clubedabengala.db import get_db

# bp = Blueprint('emprestimos', __name__)

# @bp.route('/emprestimos')
# @login_required
# def index():
#     abort_if_not_in_role("Colaborador")
#     db = get_db()
#     emprestimos = db.execute(
#         'SELECT e.id, e.created, e.status, est.status status_name,'
#         ' e.solicitante_id, sol.name solicitante_name, e.beneficiario_id, ben.name beneficiario_name'
#         ' FROM emprestimos e'
#         ' JOIN users sol ON sol.id = e.solicitante_id'
#         ' JOIN beneficiarios ben ON ben.id = e.beneficiario_id'
#         ' JOIN emprestimos_status est on est.id = e.status'
#         ' ORDER BY e.created DESC'
#     ).fetchall()
#     return render_template('emprestimos/index.html', emprestimos=emprestimos)


# @bp.route('/emprestimos/<int:id>')
# @login_required
# def details(id):
#     abort_if_not_in_role("Colaborador")
#     e = get_emprestimo(id)
#     return render_template('emprestimos/details.html', emprestimo=e)

# def get_emprestimo(id):
#     db = get_db()
#     emprestimo = db.execute(
#         'SELECT e.id, e.created, e.status, est.status status_name,'
#         ' e.solicitante_id, sol.name solicitante_name, e.beneficiario_id, ben.name beneficiario_name'
#         ' FROM emprestimos e'
#         ' JOIN users sol ON sol.id = e.solicitante_id'
#         ' JOIN beneficiarios ben ON ben.id = e.beneficiario_id'
#         ' JOIN emprestimos_status est on est.id = e.status'
#         ' WHERE e.id = ?',
#         (id,)
#     ).fetchone()

#     if emprestimo is None:
#         abort(404, f"Empréstimo não existe")
    
#     return emprestimo

# @bp.route('/emprestimos/create')
# @login_required
# def create():
#     return render_template('emprestimos/create.html')