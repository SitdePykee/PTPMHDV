from flask import Blueprint, request, jsonify
from backend.common.database import db
from backend.services.production_control.models import ProductionProcess, ProductionStep

production_control_bp = Blueprint('production_control', __name__)

@production_control_bp.route('/process', methods=['POST'])
def create_process():
    data = request.get_json()
    new_process = ProductionProcess(name=data['name'], status=data['status'], start_time=data['start_time'], end_time=data['end_time'])
    db.session.add(new_process)
    db.session.commit()
    return jsonify({'message': 'Quy trình sản xuất đã được tạo'}), 201

@production_control_bp.route('/process/<int:id>', methods=['GET'])
def get_process(id):
    process = ProductionProcess.query.get_or_404(id)
    return jsonify({'name': process.name, 'status': process.status, 'start_time': process.start_time, 'end_time': process.end_time})

@production_control_bp.route('/process/<int:id>', methods=['PUT'])
def update_process(id):
    data = request.get_json()
    process = ProductionProcess.query.get_or_404(id)
    process.status = data.get('status', process.status)
    db.session.commit()
    return jsonify({'message': 'Cập nhật tiến độ sản xuất thành công'})
