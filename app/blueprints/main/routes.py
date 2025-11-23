from flask import render_template
from . import main_bp


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/about')
def about():
    return render_template('main/index.html')


@main_bp.route('/help')
def help_page():
    return render_template('main/index.html')


@main_bp.route('/health')
def health():
    """Health check endpoint for deployment platforms"""
    return {'status': 'healthy', 'message': 'Syllabus Tracker is running'}
