from flask import render_template, Blueprint

app_view = Blueprint('app_view', __name__, template_folder='templates', static_folder='static')


@app_view.route('/')
def home():
    return render_template('home.html')
