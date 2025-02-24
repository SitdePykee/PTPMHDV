from backend.common.database import db

class ProductionPlan(db.Model):
    __tablename__ = 'production_plan'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    material_needs = db.Column(db.String(255), nullable=False)
    schedule = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, order_id, material_needs, schedule, status):
        self.order_id = order_id
        self.material_needs = material_needs
        self.schedule = schedule
        self.status = status
