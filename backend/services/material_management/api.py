from flask import Blueprint, request, jsonify
from backend.common.database import db
from backend.services.material_management.models import Material, StockTransaction
from backend.services.material_management.dcom import read_excel_data, update_excel_data
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

@material_management_bp.route('/update_excel_data', methods=['POST'])
def update_excel():
    """API cập nhật dữ liệu Excel trên máy chủ DCOM và đồng bộ với CSDL"""
    try:
        data = request.get_json()
        file_path = data.get("file_path")
        remote_server = data.get("remote_server")
        updated_data = data.get("updated_data")

        if not file_path or not updated_data:
            return jsonify({"error": "⚠ Thiếu đường dẫn file hoặc dữ liệu cập nhật!"}), 400

        # Cập nhật file Excel trên máy chủ DCOM
        result = update_excel_data(file_path, updated_data, remote_server)
        if "error" in result:
            return jsonify({"error": result["error"]}), 500

        # Đọc lại dữ liệu mới từ file Excel
        new_excel_data = read_excel_data(file_path, remote_server=remote_server)
        if "error" in new_excel_data:
            return jsonify({"error": new_excel_data["error"]}), 500

        for row in new_excel_data:
            name = row.get("name")
            quantity = row.get("quantity")
            supplier_id = row.get("supplier_id")

            if not name or supplier_id is None:
                return jsonify({
                    "error": "❌ Lỗi: File Excel thiếu thông tin quan trọng (name, supplier_id)!"
                }), 400

            # Tìm dữ liệu trong CSDL để cập nhật
            material = Material.query.filter_by(name=name, supplier_id=supplier_id).first()

            if material:
                material.quantity = quantity
            else:
                return jsonify({
                    "error": f"❌ Không tìm thấy dữ liệu: {name} (supplier_id={supplier_id}) trong CSDL!"
                }), 404  # Trả về lỗi nếu không có trong CSDL

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "✅ Dữ liệu đã được cập nhật thành công!"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"❌ Lỗi khi cập nhật dữ liệu: {str(e)}"}), 500
@material_management_bp.route('/stock_transaction', methods=['GET'])
def get_all_stock_transactions():
    transactions = StockTransaction.query.all()
    transaction_list = [{
        "id": t.id,
        "material_id": t.material_id,
        "type": t.type,
        "quantity": t.quantity,
        "date": t.date.strftime('%Y-%m-%d')
    } for t in transactions]
    return jsonify(transaction_list), 200

@material_management_bp.route('/stock_transaction/<int:id>', methods=['GET'])
def get_stock_transaction(id):
    transaction = StockTransaction.query.get_or_404(id)
    return jsonify({
        "material_id": transaction.material_id,
        "type": transaction.type,
        "quantity": transaction.quantity,
        "date": transaction.date.strftime('%Y-%m-%d')
    })

@material_management_bp.route('/stock_transaction/<int:id>', methods=['PUT'])
def update_stock_transaction(id):
    data = request.get_json()
    transaction = StockTransaction.query.get(id)

    if not transaction:
        return jsonify({"error": "❌ Giao dịch kho không tồn tại!"}), 404

    # Cập nhật thông tin giao dịch
    transaction.material_id = data.get('material_id', transaction.material_id)
    transaction.type = data.get('type', transaction.type)
    transaction.quantity = data.get('quantity', transaction.quantity)
    transaction.date = data.get('date', transaction.date)

    db.session.commit()

    return jsonify({'message': '✅ Giao dịch kho đã được cập nhật!'}), 200

@material_management_bp.route('/stock_transaction/<int:id>', methods=['DELETE'])
def delete_stock_transaction(id):
    transaction = StockTransaction.query.get(id)

    if not transaction:
        return jsonify({"error": "❌ Giao dịch kho không tồn tại!"}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'message': '✅ Giao dịch kho đã được xóa!'}), 200

@material_management_bp.route('/stock_transaction', methods=['POST'])
def add_stock_transaction():
    data = request.get_json()
    transaction = StockTransaction(
        material_id=data['material_id'],
        type=data['type'],
        quantity=data['quantity'],
        date=data['date']
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Giao dịch kho đã được ghi nhận'}), 201
