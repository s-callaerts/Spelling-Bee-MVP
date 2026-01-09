from flask import Blueprint, render_template
from auth import login_required, teacher_required, check_authority

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('dashboard_student')
@login_required
def dashboard():
    return render_template('dashboard_student.html')

@main_bp.route('dashboard_teacher')
@login_required
@teacher_required
def dashboard_teacher():
    return render_template('dashboard_teacher.html')