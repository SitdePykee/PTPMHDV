from flask import Blueprint, request, jsonify
from backend.common.database import db
from backend.services.quality_management.models import QualityCheck, DefectReport

quality_management_bp = Blueprint('quality_management', __name__)

@quality_management_bp.route('/quality_check', methods=['POST'])
def create_quality_check():
    data = request.get_json()
    new_check = QualityCheck(product_id=data['product_id'], status=data['status'], defects=data['defects'])
    db.session.add(new_check)
    db.session.commit()
    return jsonify({'message': 'Đã kiểm tra chất lượng sản phẩm'}), 201

@quality_management_bp.route('/quality_check/<int:id>', methods=['GET'])
def get_quality_check(id):
    check = QualityCheck.query.get_or_404(id)
    return jsonify({'product_id': check.product_id, 'status': check.status, 'defects': check.defects})

@quality_management_bp.route('/defect_report', methods=['POST'])
def create_defect_report():
    data = request.get_json()
    defect = DefectReport(check_id=data['check_id'], defect_type=data['defect_type'], description=data['description'], image_url=data['image_url'])
    db.session.add(defect)
    db.session.commit()
    return jsonify({'message': 'Báo cáo lỗi sản xuất đã được ghi nhận'}), 201

