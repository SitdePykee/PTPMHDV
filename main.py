import os
from flask import Flask
from flask_cors import CORS
from backend.common.database import db
from backend.services.production_planning.api import production_planning_bp
from backend.services.production_control.api import production_control_bp
from backend.services.quality_management.api import quality_management_bp
from backend.services.material_management.api import material_management_bp

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:8000"])

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'mssql+pymssql://sa:admin@localhost/production_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Đăng ký các blueprint sau khi khởi tạo app
    app.register_blueprint(production_planning_bp, url_prefix='/api/production_planning')
    app.register_blueprint(material_management_bp, url_prefix='/api/material_management')
    app.register_blueprint(production_control_bp, url_prefix='/api/production_control')
    app.register_blueprint(quality_management_bp, url_prefix='/api/quality_management')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
