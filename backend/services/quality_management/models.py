from backend.common.database import db

class QualityCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # "pass" hoặc "fail"
    defects = db.Column(db.String(255), nullable=True)

class DefectReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey('quality_check.id'), nullable=False)
    defect_type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
