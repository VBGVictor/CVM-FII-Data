from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['PASTA_DADOS'] = 'output/dados_projeto'

    from app.routes.fii import fii_bp  
    app.register_blueprint(fii_bp)  

    return app
