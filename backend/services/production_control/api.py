from flask import Blueprint, request, jsonify, render_template, session
from backend.common.database import db
from backend.services.production_control.models import (
    NhanVien, QuyTrinhSanXuat, SanPham, BuocQuyTrinh, PhanCongNhanVien
)

production_control_bp = Blueprint('production_control', __name__)


@production_control_bp.route('/')
def index():
    return render_template('Dashboard.html')


@production_control_bp.route('/api/nhan-vien', methods=['GET'])
def get_nhan_vien():
    search_term = request.args.get('search', '').strip()
    if search_term:
        nhan_viens = NhanVien.query.filter(
            db.func.concat(NhanVien.Ho, ' ', NhanVien.Ten).ilike(f'%{search_term}%')
        ).all()
    else:
        nhan_viens = NhanVien.query.all()

    return jsonify([{
        'MaNhanVien': nv.MaNhanVien,
        'Ho': nv.Ho,
        'Ten': nv.Ten,
        'ChucVu': nv.ChucVu,
        'MucLuong': float(nv.MucLuong),
        'NgayTuyendung': nv.NgayTuyendung.isoformat() if nv.NgayTuyendung else None
    } for nv in nhan_viens])


@production_control_bp.route('/api/quy-trinh-san-xuat', methods=['GET'])
def get_quy_trinh_san_xuat():
    quy_trinhs = QuyTrinhSanXuat.query.all()
    return jsonify([{
        'MaQuyTrinh': qt.MaQuyTrinh,
        'TenQuyTrinh': qt.TenQuyTrinh,
        'MoTa': qt.MoTa,
        'ThoiGianHoanThanh': qt.ThoiGianHoanThanh
    } for qt in quy_trinhs])


@production_control_bp.route('/api/search-quy-trinh', methods=['GET'])
def search_quy_trinh():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])
    results = QuyTrinhSanXuat.query.filter(
        (QuyTrinhSanXuat.TenQuyTrinh.ilike(f'%{query}%')) |
        (QuyTrinhSanXuat.MoTa.ilike(f'%{query}%'))
    ).all()
    return jsonify([{
        'MaQuyTrinh': r.MaQuyTrinh,
        'TenQuyTrinh': r.TenQuyTrinh,
        'MoTa': r.MoTa,
        'ThoiGianHoanThanh': r.ThoiGianHoanThanh
    } for r in results])


@production_control_bp.route('/api/san-pham', methods=['GET'])
def get_san_pham():
    san_phams = SanPham.query.all()
    return jsonify([{
        'MaSanPham': sp.MaSanPham,
        'TenSanPham': sp.TenSanPham,
        'LoaiSanPham': sp.LoaiSanPham,
        'MaNguyenVatLieu': sp.MaNguyenVatLieu,
        'MaQuyTrinh': sp.MaQuyTrinh,
        'SoLuongSanXuat': sp.SoLuongSanXuat
    } for sp in san_phams])


@production_control_bp.route('/api/search', methods=['GET'])
def search_product():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])
    results = SanPham.query.filter(
        (SanPham.TenSanPham.ilike(f'%{query}%')) |
        (SanPham.LoaiSanPham.ilike(f'%{query}%'))
    ).all()
    return jsonify([{
        'MaSanPham': r.MaSanPham,
        'TenSanPham': r.TenSanPham,
        'LoaiSanPham': r.LoaiSanPham
    } for r in results])


@production_control_bp.route('/api/quytrinh', methods=['POST'])
def add_quytrinh():
    data = request.get_json()
    qt = QuyTrinhSanXuat(
        TenQuyTrinh=data['name'],
        MoTa=data['description'],
        ThoiGianHoanThanh=data['completion_time']
    )
    db.session.add(qt)
    db.session.commit()
    return jsonify({'message': 'Quy trình sản xuất đã được thêm thành công!'}), 201


@production_control_bp.route('/api/buocquytrinh/<int:ma_quy_trinh>', methods=['GET'])
def get_buoc_quy_trinh(ma_quy_trinh):
    steps = BuocQuyTrinh.query.filter_by(MaQuyTrinh=ma_quy_trinh).order_by(BuocQuyTrinh.ThuTu).all()
    return jsonify([{
        'ThuTu': s.ThuTu,
        'TenBuoc': s.TenBuoc,
        'MoTaBuoc': s.MoTaBuoc
    } for s in steps])


@production_control_bp.route('/api/phan-cong', methods=['POST'])
def phan_cong_nhan_vien():
    data = request.get_json()
    pc = PhanCongNhanVien(
        MaNhanVien=data['MaNhanVien'],
        MaQuyTrinh=data['MaQuyTrinh'],
        VaiTro=data.get('VaiTro', 'Công nhân')
    )
    db.session.add(pc)
    db.session.commit()
    return jsonify({'message': 'Phân công thành công!'})


@production_control_bp.route('/api/danh-sach-phan-cong', methods=['GET'])
def danh_sach_phan_cong():
    records = db.session.query(
        PhanCongNhanVien.MaPhanCong,
        NhanVien.Ho,
        NhanVien.Ten,
        QuyTrinhSanXuat.TenQuyTrinh,
        PhanCongNhanVien.VaiTro
    ).join(NhanVien, PhanCongNhanVien.MaNhanVien == NhanVien.MaNhanVien)\
     .join(QuyTrinhSanXuat, PhanCongNhanVien.MaQuyTrinh == QuyTrinhSanXuat.MaQuyTrinh).all()

    return jsonify([{
        'MaPhanCong': r.MaPhanCong,
        'HoTen': f"{r.Ho} {r.Ten}",
        'TenQuyTrinh': r.TenQuyTrinh,
        'VaiTro': r.VaiTro
    } for r in records])


@production_control_bp.route('/api/xoa-phan-cong', methods=['POST'])
def xoa_phan_cong():
    ma_pc = request.json.get('MaPhanCong')
    pc = PhanCongNhanVien.query.get(ma_pc)
    if not pc:
        return jsonify({'message': 'Không tìm thấy phân công!'}), 404
    db.session.delete(pc)
    db.session.commit()
    return jsonify({'message': 'Đã xóa phân công thành công!'})


# Cart API giữ nguyên logic dùng session:
@production_control_bp.route('/api/cart', methods=['GET'])
def get_cart():
    return jsonify(session.get('cart', []))


@production_control_bp.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    product = request.get_json()
    product_id = product.get('MaSanPham')

    if 'cart' not in session:
        session['cart'] = []

    for item in session['cart']:
        if item['MaSanPham'] == product_id:
            item['SoLuong'] += 1
            session.modified = True
            return jsonify({'message': 'Đã cập nhật số lượng sản phẩm trong giỏ.'})

    product['SoLuong'] = 1
    session['cart'].append(product)
    session.modified = True
    return jsonify({'message': 'Đã thêm vào giỏ hàng.'})


@production_control_bp.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    product_id = request.json.get('MaSanPham')
    session['cart'] = [item for item in session.get('cart', []) if item['MaSanPham'] != product_id]
    session.modified = True
    return jsonify({'message': 'Đã xóa sản phẩm khỏi giỏ hàng.'})


@production_control_bp.route('/api/cart/update', methods=['POST'])
def update_quantity():
    data = request.get_json()
    for item in session.get('cart', []):
        if item['MaSanPham'] == data.get('MaSanPham'):
            item['SoLuong'] = data.get('SoLuong')
            session.modified = True
            return jsonify({'message': 'Đã cập nhật số lượng.'})
    return jsonify({'message': 'Không tìm thấy sản phẩm.'}), 404


@production_control_bp.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')


@production_control_bp.route('/production')
def production():
    return render_template('production.html')
