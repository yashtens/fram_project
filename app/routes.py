from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app import db
from app.models import Field, Crop, Labour, LabourRecord, CostRecord
from datetime import datetime
from sqlalchemy import func

# Create blueprints
main_bp = Blueprint('main', __name__)
crops_bp = Blueprint('crops', __name__, url_prefix='/crops')
labour_bp = Blueprint('labour', __name__, url_prefix='/labour')
costs_bp = Blueprint('costs', __name__, url_prefix='/costs')
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

# ===================== MAIN ROUTES =====================
@main_bp.route('/')
def index():
    total_fields = Field.query.count()
    total_crops = Crop.query.count()
    active_crops = Crop.query.filter_by(status='Growing').count()
    total_labours = Labour.query.count()
    
    # Calculate total revenue and costs
    harvested_crops = Crop.query.filter_by(status='Harvested').all()
    total_revenue = sum(crop.get_revenue() for crop in harvested_crops)
    total_costs = sum(crop.get_total_cost() + crop.get_total_labour_cost() for crop in Crop.query.all())
    
    stats = {
        'total_fields': total_fields,
        'total_crops': total_crops,
        'active_crops': active_crops,
        'total_labours': total_labours,
        'total_revenue': f"{total_revenue:.2f}",
        'total_costs': f"{total_costs:.2f}",
        'gross_profit': f"{(total_revenue - total_costs):.2f}"
    }
    
    return render_template('dashboard.html', stats=stats)

# ===================== FIELD ROUTES =====================
@main_bp.route('/fields')
def view_fields():
    fields = Field.query.all()
    return render_template('fields.html', fields=fields)

@main_bp.route('/field/add', methods=['GET', 'POST'])
def add_field():
    if request.method == 'POST':
        new_field = Field(
            name=request.form['name'],
            area=float(request.form['area']),
            location=request.form.get('location', '')
        )
        db.session.add(new_field)
        db.session.commit()
        flash('Field added successfully!', 'success')
        return redirect(url_for('main.view_fields'))
    return render_template('add_field.html')

@main_bp.route('/field/<int:field_id>/edit', methods=['GET', 'POST'])
def edit_field(field_id):
    field = Field.query.get_or_404(field_id)
    if request.method == 'POST':
        field.name = request.form['name']
        field.area = float(request.form['area'])
        field.location = request.form.get('location', '')
        db.session.commit()
        flash('Field updated successfully!', 'success')
        return redirect(url_for('main.view_fields'))
    return render_template('edit_field.html', field=field)

@main_bp.route('/field/<int:field_id>/delete')
def delete_field(field_id):
    field = Field.query.get_or_404(field_id)
    db.session.delete(field)
    db.session.commit()
    flash('Field deleted successfully!', 'success')
    return redirect(url_for('main.view_fields'))

# ===================== CROP ROUTES =====================
@crops_bp.route('/')
def view_crops():
    crops = Crop.query.all()
    return render_template('crops.html', crops=crops)

@crops_bp.route('/add', methods=['GET', 'POST'])
def add_crop():
    fields = Field.query.all()
    if request.method == 'POST':
        new_crop = Crop(
            field_id=int(request.form['field_id']),
            crop_type=request.form['crop_type'],
            variety=request.form.get('variety', ''),
            seeding_date=datetime.strptime(request.form['seeding_date'], '%Y-%m-%d'),
            expected_harvest_date=datetime.strptime(request.form['expected_harvest_date'], '%Y-%m-%d') if request.form.get('expected_harvest_date') else None,
            quantity_seeded=float(request.form['quantity_seeded']),
            expected_yield=float(request.form.get('expected_yield', 0)) if request.form.get('expected_yield') else None,
            notes=request.form.get('notes', '')
        )
        db.session.add(new_crop)
        db.session.commit()
        flash('Crop added successfully!', 'success')
        return redirect(url_for('crops.view_crops'))
    return render_template('add_crop.html', fields=fields)

@crops_bp.route('/<int:crop_id>')
def view_crop_detail(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    labour_records = LabourRecord.query.filter_by(crop_id=crop_id).all()
    cost_records = CostRecord.query.filter_by(crop_id=crop_id).all()
    
    crop_data = {
        'crop': crop,
        'labour_records': labour_records,
        'cost_records': cost_records,
        'total_cost': crop.get_total_cost(),
        'total_labour_cost': crop.get_total_labour_cost(),
        'revenue': crop.get_revenue(),
        'gross_profit': crop.get_gross_profit()
    }
    return render_template('crop_detail.html', **crop_data)

@crops_bp.route('/<int:crop_id>/edit', methods=['GET', 'POST'])
def edit_crop(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    fields = Field.query.all()
    
    if request.method == 'POST':
        crop.field_id = int(request.form['field_id'])
        crop.crop_type = request.form['crop_type']
        crop.variety = request.form.get('variety', '')
        crop.seeding_date = datetime.strptime(request.form['seeding_date'], '%Y-%m-%d')
        crop.expected_harvest_date = datetime.strptime(request.form['expected_harvest_date'], '%Y-%m-%d') if request.form.get('expected_harvest_date') else None
        crop.quantity_seeded = float(request.form['quantity_seeded'])
        crop.expected_yield = float(request.form.get('expected_yield', 0)) if request.form.get('expected_yield') else None
        crop.status = request.form['status']
        crop.notes = request.form.get('notes', '')
        
        if request.form.get('actual_harvest_date'):
            crop.actual_harvest_date = datetime.strptime(request.form['actual_harvest_date'], '%Y-%m-%d')
        if request.form.get('actual_yield'):
            crop.actual_yield = float(request.form['actual_yield'])
        
        db.session.commit()
        flash('Crop updated successfully!', 'success')
        return redirect(url_for('crops.view_crop_detail', crop_id=crop_id))
    
    return render_template('edit_crop.html', crop=crop, fields=fields)

@crops_bp.route('/<int:crop_id>/delete')
def delete_crop(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    db.session.delete(crop)
    db.session.commit()
    flash('Crop deleted successfully!', 'success')
    return redirect(url_for('crops.view_crops'))

# ===================== LABOUR ROUTES =====================
@labour_bp.route('/')
def view_labours():
    labours = Labour.query.all()
    return render_template('labours.html', labours=labours)

@labour_bp.route('/add', methods=['GET', 'POST'])
def add_labour():
    if request.method == 'POST':
        new_labour = Labour(
            name=request.form['name'],
            designation=request.form.get('designation', ''),
            contact=request.form.get('contact', ''),
            daily_wage=float(request.form['daily_wage'])
        )
        db.session.add(new_labour)
        db.session.commit()
        flash('Labour added successfully!', 'success')
        return redirect(url_for('labour.view_labours'))
    return render_template('add_labour.html')

@labour_bp.route('/<int:labour_id>/edit', methods=['GET', 'POST'])
def edit_labour(labour_id):
    labour = Labour.query.get_or_404(labour_id)
    if request.method == 'POST':
        labour.name = request.form['name']
        labour.designation = request.form.get('designation', '')
        labour.contact = request.form.get('contact', '')
        labour.daily_wage = float(request.form['daily_wage'])
        labour.status = request.form['status']
        db.session.commit()
        flash('Labour updated successfully!', 'success')
        return redirect(url_for('labour.view_labours'))
    return render_template('edit_labour.html', labour=labour)

@labour_bp.route('/<int:labour_id>/delete')
def delete_labour(labour_id):
    labour = Labour.query.get_or_404(labour_id)
    db.session.delete(labour)
    db.session.commit()
    flash('Labour deleted successfully!', 'success')
    return redirect(url_for('labour.view_labours'))

# ===================== LABOUR RECORD ROUTES =====================
@labour_bp.route('/record/add', methods=['GET', 'POST'])
def add_labour_record():
    crops = Crop.query.all()
    labours = Labour.query.filter_by(status='Active').all()
    
    if request.method == 'POST':
        new_record = LabourRecord(
            crop_id=int(request.form['crop_id']),
            labour_id=int(request.form['labour_id']),
            work_date=datetime.strptime(request.form['work_date'], '%Y-%m-%d'),
            hours_worked=float(request.form['hours_worked']),
            work_type=request.form['work_type'],
            notes=request.form.get('notes', '')
        )
        db.session.add(new_record)
        db.session.commit()
        flash('Labour record added successfully!', 'success')
        return redirect(url_for('labour.view_labour_records'))
    
    return render_template('add_labour_record.html', crops=crops, labours=labours)

@labour_bp.route('/records')
def view_labour_records():
    records = LabourRecord.query.all()
    return render_template('labour_records.html', records=records)

@labour_bp.route('/record/<int:record_id>/delete')
def delete_labour_record(record_id):
    record = LabourRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    flash('Labour record deleted successfully!', 'success')
    return redirect(url_for('labour.view_labour_records'))

# ===================== COST ROUTES =====================
@costs_bp.route('/')
def view_costs():
    costs = CostRecord.query.all()
    return render_template('costs.html', costs=costs)

@costs_bp.route('/add', methods=['GET', 'POST'])
def add_cost():
    crops = Crop.query.all()
    
    if request.method == 'POST':
        new_cost = CostRecord(
            crop_id=int(request.form['crop_id']),
            category=request.form['category'],
            description=request.form.get('description', ''),
            amount=float(request.form['amount']),
            transaction_date=datetime.strptime(request.form['transaction_date'], '%Y-%m-%d') if request.form.get('transaction_date') else datetime.utcnow(),
            notes=request.form.get('notes', '')
        )
        db.session.add(new_cost)
        db.session.commit()
        flash('Cost record added successfully!', 'success')
        return redirect(url_for('costs.view_costs'))
    
    return render_template('add_cost.html', crops=crops)

@costs_bp.route('/<int:cost_id>/delete')
def delete_cost(cost_id):
    cost = CostRecord.query.get_or_404(cost_id)
    db.session.delete(cost)
    db.session.commit()
    flash('Cost record deleted successfully!', 'success')
    return redirect(url_for('costs.view_costs'))

# ===================== REPORTS ROUTES =====================
@reports_bp.route('/')
def view_reports():
    all_crops = Crop.query.all()
    
    total_revenue = sum(crop.get_revenue() for crop in all_crops)
    total_costs = sum(crop.get_total_cost() + crop.get_total_labour_cost() for crop in all_crops)
    total_profit = total_revenue - total_costs
    
    # Crop-wise profit
    crop_profits = []
    for crop in all_crops:
        if crop.status == 'Harvested':
            crop_profits.append({
                'crop_type': crop.crop_type,
                'field': crop.field.name,
                'revenue': crop.get_revenue(),
                'cost': crop.get_total_cost() + crop.get_total_labour_cost(),
                'profit': crop.get_gross_profit(),
                'yield': crop.actual_yield
            })
    
    # Labour cost summary
    labour_costs = db.session.query(Labour.name, func.sum(LabourRecord.hours_worked * (Labour.daily_wage / 8)).label('total_cost')).join(LabourRecord).group_by(Labour.id, Labour.name).all()
    
    reports = {
        'total_revenue': f"{total_revenue:.2f}",
        'total_costs': f"{total_costs:.2f}",
        'total_profit': f"{total_profit:.2f}",
        'crop_profits': crop_profits,
        'labour_costs': labour_costs
    }
    
    return render_template('reports.html', reports=reports)

@reports_bp.route('/api/crop-stats')
def api_crop_stats():
    crops = Crop.query.all()
    data = {
        'labels': [crop.crop_type for crop in crops],
        'revenue': [crop.get_revenue() for crop in crops],
        'costs': [crop.get_total_cost() + crop.get_total_labour_cost() for crop in crops],
        'profit': [crop.get_gross_profit() for crop in crops]
    }
    return jsonify(data)
