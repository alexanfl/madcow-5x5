from flask import Flask, render_template
app = Flask(__name__)

WEIGHT_INCREMENT = 0.125

def get_primary_day(starting_rm5, exercise_type):
    weights = []
    for k in reversed(range(3 + exercise_type)):
        weights.append(starting_rm5*(1 - k*WEIGHT_INCREMENT))

@app.route('/')
def index():
    return render_template('index.html', title='Madcow 5x5')

@app.route('/prog')
def program():
    return render_template('prog.html', data=data)
