import os

from flask import Flask, session, redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'clubedabengala.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    # @app.route('/')
    # def index():
    #     return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import emprestimos
    app.register_blueprint(emprestimos.bp)
    # app.add_url_rule('/', endpoint="index")

    # from . import solicitacoes
    # app.register_blueprint(solicitacoes.bp)

    from . import usuarios
    app.register_blueprint(usuarios.bp)

    @app.route('/')
    def index():
        uid = session.get('user_id')
        if uid is None:
            return redirect(url_for('auth.login'))

        if auth.user_in_role("Colaborador"):
            return redirect(url_for('emprestimos.index'))
        
        app.logger.debug("Benefic")
        return redirect(url_for('usuarios.details', id = uid))

    return app