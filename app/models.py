from app import db
from datetime import datetime

class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    area = db.Column(db.Float, nullable=False)  # in acres
    location = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    crops = db.relationship('Crop', backref='field', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'Field({self.name}, {self.area} acres)'

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False)
    crop_type = db.Column(db.String(100), nullable=False)  # Rice, Wheat, Corn, etc.
    variety = db.Column(db.String(100))
    seeding_date = db.Column(db.DateTime, nullable=False)
    expected_harvest_date = db.Column(db.DateTime)
    actual_harvest_date = db.Column(db.DateTime)
    quantity_seeded = db.Column(db.Float, nullable=False)  # in kg
    expected_yield = db.Column(db.Float)  # in kg
    actual_yield = db.Column(db.Float)  # in kg
    status = db.Column(db.String(50), default='Growing')  # Growing, Harvested, Failed
    notes = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    labour_records = db.relationship('LabourRecord', backref='crop', lazy=True, cascade='all, delete-orphan')
    cost_records = db.relationship('CostRecord', backref='crop', lazy=True, cascade='all, delete-orphan')
    
    def get_total_cost(self):
        return sum(cost.amount for cost in self.cost_records)
    
    def get_total_labour_cost(self):
        return sum(labour.total_cost for labour in self.labour_records)
    
    def get_revenue(self):
        if self.actual_yield:
            # Assuming market price - you can modify this
            market_price = 25  # per kg
            return self.actual_yield * market_price
        return 0
    
    def get_gross_profit(self):
        revenue = self.get_revenue()
        total_cost = self.get_total_cost() + self.get_total_labour_cost()
        return revenue - total_cost
    
    def __repr__(self):
        return f'Crop({self.crop_type}, {self.status})'

class Labour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    designation = db.Column(db.String(100))  # Farmer, Labourer, etc.
    contact = db.Column(db.String(20))
    daily_wage = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Active')  # Active, Inactive
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    labour_records = db.relationship('LabourRecord', backref='labour', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'Labour({self.name}, {self.designation})'

class LabourRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    labour_id = db.Column(db.Integer, db.ForeignKey('labour.id'), nullable=False)
    work_date = db.Column(db.DateTime, nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    work_type = db.Column(db.String(100))  # Seeding, Weeding, Harvesting, etc.
    notes = db.Column(db.Text)
    
    @property
    def total_cost(self):
        if self.labour:
            return self.hours_worked * (self.labour.daily_wage / 8)  # Assuming 8 hour day
        return 0
    
    def __repr__(self):
        return f'LabourRecord({self.labour.name}, {self.work_type})'

class CostRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # Seeds, Fertilizer, Pesticide, etc.
    description = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'CostRecord({self.category}, {self.amount})'
