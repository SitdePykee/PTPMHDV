from flask import Blueprint, request, jsonify
from backend.common.database import db
from backend.services.material_management.models import Material, StockTransaction
from backend.services.material_management.dcom import read_excel_data
import os

material_management_bp = Blueprint('material_management', __name__)

@material_management_bp.route('/material', methods=['GET'])
def get_all_materials():
    materials = Material.query.all()
    material_list = [{"id": m.id, "name": m.name, "quantity": m.quantity, "supplier_id": m.supplier_id} for m in materials]
    return jsonify(material_list), 200


@material_management_bp.route('/material', methods=['POST'])
def add_material():
    data = request.get_json()
    new_material = Material(name=data['name'], quantity=data['quantity'], supplier_id=data['supplier_id'])
    db.session.add(new_material)
    db.session.commit()
    return jsonify({'message': 'Nguyên vật liệu đã được thêm'}), 201

@material_management_bp.route('/material/<int:id>', methods=['GET'])
def get_material(id):
    material = Material.query.get_or_404(id)
    return jsonify({'name': material.name, 'quantity': material.quantity, 'supplier_id': material.supplier_id})

@material_management_bp.route('/stock_transaction', methods=['POST'])
def add_stock_transaction():
    data = request.get_json()
    transaction = StockTransaction(material_id=data['material_id'], type=data['type'], quantity=data['quantity'], date=data['date'])
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Giao dịch kho đã được ghi nhận'}), 201

@material_management_bp.route('/read_excel_data', methods=['POST'])
def read_excel_dcom():
    """ API nhận đường dẫn file Excel trên máy chủ và đọc dữ liệu qua DCOM """
    try:
        data = request.get_json()
        file_path = data.get("file_path")
        remote_server = request.args.get("remote_server")

        if not file_path:
            return jsonify({"error": "Không tìm thấy đường dẫn file Excel"}), 400

        # Đọc dữ liệu từ file Excel qua DCOM
        excel_data = read_excel_data(file_path, remote_server=remote_server)

        if "error" in excel_data:
            return jsonify({"error": excel_data["error"]}), 500

        return jsonify({"message": "Dữ liệu đọc thành công!", "data": excel_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@material_management_bp.route('/fetch_excel_data', methods=['POST'])
def fetch_excel_data():
    """ API trên server để gọi đến máy chủ DCOM và đọc dữ liệu Excel """
    try:
        data = request.get_json()
        file_path = data.get("file_path")
        remote_server = data.get("remote_server")

        if not file_path:
            return jsonify({"error": "⚠ Vui lòng nhập đường dẫn file Excel trên máy chủ!"}), 400

        # Gọi hàm xử lý DCOM từ `dcom.py`
        excel_data = read_excel_data(file_path, remote_server=remote_server)

        if "error" in excel_data:
            return jsonify({"error": excel_data["error"]}), 500

        return jsonify({"message": "✅ Dữ liệu đã được tải từ máy chủ DCOM!", "data": excel_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
