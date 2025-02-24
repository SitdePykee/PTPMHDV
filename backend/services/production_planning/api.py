from flask import Blueprint, request, jsonify
from backend.common.database import db
from backend.services.production_planning.models import ProductionPlan

production_planning_bp = Blueprint('production_planning', __name__)

@production_planning_bp.route('/plan', methods=['POST'])
def create_plan():
    data = request.get_json()
    new_plan = ProductionPlan(order_id=data['order_id'], material_needs=data['material_needs'], schedule=data['schedule'], status=data['status'])
    db.session.add(new_plan)
    db.session.commit()
    return jsonify({'message': 'Kế hoạch sản xuất đã được tạo'}), 201

@production_planning_bp.route('/plan/<int:id>', methods=['GET'])
def get_plan(id):
    plan = ProductionPlan.query.get_or_404(id)
    return jsonify({'order_id': plan.order_id, 'material_needs': plan.material_needs, 'schedule': plan.schedule, 'status': plan.status})
