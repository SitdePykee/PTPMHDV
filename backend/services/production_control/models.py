from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, Text

from backend.common.database import db

class NhanVien(db.Model):
    __tablename__ = 'NhanVien'
    MaNhanVien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Ho = db.Column(db.String(100), nullable=False)
    Ten = db.Column(db.String(100), nullable=False)
    ChucVu = db.Column(db.String(100))
    MucLuong = db.Column(db.DECIMAL(10, 2))
    NgayTuyendung = db.Column(db.Date)

    phan_congs = db.relationship('PhanCongNhanVien', back_populates='nhan_vien')


class QuyTrinhSanXuat(db.Model):
    __tablename__ = 'QuyTrinhSanXuat'
    MaQuyTrinh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TenQuyTrinh = db.Column(db.String(255), nullable=False)
    MoTa = db.Column(db.Text)
    ThoiGianHoanThanh = db.Column(db.Integer)

    buoc_quy_trinhs = db.relationship('BuocQuyTrinh', back_populates='quy_trinh')
    san_phams = db.relationship('SanPham', back_populates='quy_trinh')
    phan_congs = db.relationship('PhanCongNhanVien', back_populates='quy_trinh')


class NguyenVatLieu(db.Model):
    __tablename__ = 'NguyenVatLieu'
    MaNguyenVatLieu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TenNguyenVatLieu = db.Column(db.String(255), nullable=False)
    DonViTinh = db.Column(db.String(50))
    SoLuongTon = db.Column(db.Integer)

    san_phams = db.relationship('SanPham', back_populates='nguyen_vat_lieu')


class SanPham(db.Model):
    __tablename__ = 'SanPham'  # Optionally, define the table name if it differs
    MaSanPham = db.Column(db.Integer, primary_key=True)
    TenSanPham = db.Column(db.String(255), nullable=False)
    LoaiSanPham = db.Column(db.String(100))
    MaNguyenVatLieu = db.Column(db.Integer, db.ForeignKey('NguyenVatLieu.MaNguyenVatLieu'))
    MaQuyTrinh = db.Column(db.Integer, db.ForeignKey('QuyTrinhSanXuat.MaQuyTrinh'))
    SoLuongSanXuat = db.Column(db.Integer)

    # Define relationships
    nguyen_vat_lieu = db.relationship('NguyenVatLieu', back_populates='san_phams')
    quy_trinh = db.relationship('QuyTrinhSanXuat', back_populates='san_phams')


class BuocQuyTrinh(db.Model):
    __tablename__ = 'BuocQuyTrinh'
    MaBuoc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaQuyTrinh = db.Column(db.Integer, db.ForeignKey('QuyTrinhSanXuat.MaQuyTrinh'), nullable=False)
    ThuTu = db.Column(db.Integer, nullable=False)
    TenBuoc = db.Column(db.String(255), nullable=False)
    MoTaBuoc = db.Column(db.Text, nullable=False)
    ThoiGianUocTinh = db.Column(db.Integer)

    quy_trinh = db.relationship('QuyTrinhSanXuat', back_populates='buoc_quy_trinhs')


class PhanCongNhanVien(db.Model):
    __tablename__ = 'PhanCongNhanVien'
    MaPhanCong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaNhanVien = db.Column(db.Integer, db.ForeignKey('NhanVien.MaNhanVien'))
    MaQuyTrinh = db.Column(db.Integer, db.ForeignKey('QuyTrinhSanXuat.MaQuyTrinh'))
    VaiTro = db.Column(db.String(100))

    nhan_vien = db.relationship('NhanVien', back_populates='phan_congs')
    quy_trinh = db.relationship('QuyTrinhSanXuat', back_populates='phan_congs')
