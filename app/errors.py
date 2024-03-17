from app import app, db
from flask import render_template

@app.errorhandler(404)
def not_found_error(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def not_found_error(e):
    db.session.rollback()
    return render_template('errors/500.html'), 500