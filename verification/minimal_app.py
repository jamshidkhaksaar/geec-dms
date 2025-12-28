from flask import Flask, render_template, session

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'test'

@app.route('/')
def index():
    session['user_id'] = 1 # Simulate logged in
    session['role'] = 'Admin'
    session['full_name'] = 'Test User'
    return render_template('base.html', company_info={'name': 'Test Co'})

# Add dummy routes for url_for
@app.route('/dashboard')
def dashboard(): return 'dashboard'
@app.route('/create_letter')
def create_letter(): return 'create_letter'
@app.route('/letter_status')
def letter_status(): return 'letter_status'
@app.route('/user_management')
def user_management(): return 'user_management'
@app.route('/settings')
def settings(): return 'settings'
@app.route('/logout')
def logout(): return 'logout'
@app.route('/login')
def login(): return 'login'

if __name__ == '__main__':
    app.run(port=5001)
