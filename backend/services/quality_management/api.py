from flask import Blueprint, request, jsonify
from backend.common.database import db
from backend.services.quality_management.models import QualityCheck, DefectReport


quality_management_bp = Blueprint('quality_management', __name__)

# GET Endpoints
@quality_management_bp.route('/quality_check/<int:id>', methods=['GET'])
def get_quality_check(id):
   """Retrieve a specific quality check by ID"""
   check = QualityCheck.query.get_or_404(id)
   return jsonify({
       'product_id': check.product_id,
       'status': check.status,
       'defects': check.defects
   })




@quality_management_bp.route('/quality_checks', methods=['GET'])
def get_all_quality_checks():
   """Retrieve all quality checks"""
   checks = QualityCheck.query.all()
   result = [{
       'id': check.id,
       'product_id': check.product_id,
       'status': check.status,
       'defects': check.defects
   } for check in checks]
   return jsonify(result), 200




@quality_management_bp.route('/defect_report/check/<int:check_id>', methods=['GET'])
def get_defect_report_by_check(check_id):
   report = DefectReport.query.filter_by(check_id=check_id).first()
   if not report:
       return jsonify({'message': 'Không tìm thấy báo cáo lỗi'}), 404
   return jsonify({
       'id': report.id,
       'check_id': report.check_id,
       'defect_type': report.defect_type,
       'description': report.description,
       'image_url': report.image_url
   })




@quality_management_bp.route('/defect_reports/product/<int:product_id>', methods=['GET'])
def get_defect_reports_by_product(product_id):
   """Retrieve all defect reports for a specific product ID through quality check relationship"""
   reports = DefectReport.query.join(QualityCheck).filter(QualityCheck.product_id == product_id).all()
   result = [{
       'check_id': report.check_id,
       'defect_type': report.defect_type,
       'description': report.description,
       'image_url': report.image_url
   } for report in reports]
   return jsonify(result), 200




# POST Endpoints
@quality_management_bp.route('/quality_check', methods=['POST'])
def create_quality_check():
   """Create a new quality check"""
   data = request.get_json()
   new_check = QualityCheck(
       product_id=data['product_id'],
       status=data['status'],
       defects=data['defects']
   )
   db.session.add(new_check)
   db.session.commit()
   return jsonify({'message': 'Đã kiểm tra chất lượng sản phẩm'}), 201




@quality_management_bp.route('/defect_report', methods=['POST'])
def create_defect_report():
   """Create a new defect report"""
   data = request.get_json()
   defect = DefectReport(
       check_id=data['check_id'],
       defect_type=data['defect_type'],
       description=data['description'],
       image_url=data['image_url']
   )
   db.session.add(defect)
   db.session.commit()
   return jsonify({'message': 'Báo cáo lỗi sản xuất đã được ghi nhận'}), 201




# PUT Endpoints
@quality_management_bp.route('/quality_check/<int:id>', methods=['PUT'])
def update_quality_check(id):
   """Update an existing quality check"""
   check = QualityCheck.query.get_or_404(id)
   data = request.get_json()


   # Update fields if provided in request, keep existing values otherwise
   check.product_id = data.get('product_id', check.product_id)
   check.status = data.get('status', check.status)
   check.defects = data.get('defects', check.defects)


   db.session.commit()
   return jsonify({'message': 'Đã cập nhật kiểm tra chất lượng'}), 200




@quality_management_bp.route('/defect_report/<int:id>', methods=['PUT'])
def update_defect_report(id):
   """Update an existing defect report"""
   report = DefectReport.query.get_or_404(id)
   data = request.get_json()


   # Update fields if provided in request, keep existing values otherwise
   report.check_id = data.get('check_id', report.check_id)
   report.defect_type = data.get('defect_type', report.defect_type)
   report.description = data.get('description', report.description)
   report.image_url = data.get('image_url', report.image_url)


   db.session.commit()
   return jsonify({'message': 'Đã cập nhật báo cáo lỗi'}), 200




# DELETE Endpoints
@quality_management_bp.route('/quality_check/<int:id>', methods=['DELETE'])
def delete_quality_check(id):
   """Delete a quality check by ID"""
   check = QualityCheck.query.get_or_404(id)
   db.session.delete(check)
   db.session.commit()
   return jsonify({'message': 'Đã xóa kiểm tra chất lượng'}), 200




@quality_management_bp.route('/defect_report/<int:id>', methods=['DELETE'])
def delete_defect_report(id):
   """Delete a defect report by ID"""
   report = DefectReport.query.get_or_404(id)
   db.session.delete(report)
   db.session.commit()
   return jsonify({'message': 'Đã xóa báo cáo lỗi'}), 200