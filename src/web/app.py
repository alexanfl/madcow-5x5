from flask import Flask, render_template, jsonify, request, flash
from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms import validators

app = Flask(__name__)
app.secret_key = "wtf is this"

WEIGHT_INCREMENT = 0.125
WEIGHT_PRECISION = 2.5
NUM_WEEKS = 12

class RMForm(FlaskForm):
    squat = DecimalField("squat", validators=[validators.DataRequired()])
    bench = DecimalField("bench", validators=[validators.DataRequired()])
    dl = DecimalField("dl", validators=[validators.DataRequired()])
    ohp = DecimalField("ohp", validators=[validators.DataRequired()])
    row = DecimalField("row", validators=[validators.DataRequired()])

def get_columns():
    columns = []
    columns.append({"field": "reps", "title": "Reps", "sortable": False}) 
    for i in range(12):
        tmp_dict = {
            "field": "week{}".format(i + 1),
            "title": i + 1,
            "sortable": False
        }

        columns.append(tmp_dict)

    return columns


def get_primary_day(starting_rm5, exercise_type):
    weights_and_reps = [[], []]
    for k in reversed(range(4 + exercise_type)):
        weights_and_reps[0].append(myround(starting_rm5*(1 - k*WEIGHT_INCREMENT)))
        weights_and_reps[1].append(5)

    return weights_and_reps


def get_secondary_day(starting_rm5, exercise_type):
    weights_and_reps = get_primary_day(starting_rm5, exercise_type)

    weights_and_reps[0][-1] += 2.5
    weights_and_reps.append(weights[0][2])

    weights_and_reps[1][-1] = 3
    weights_and_reps.append(8)

    return weights_and_reps


def get_12weeks(weights_and_reps):
    program = []
    i = 0
    for weight in weights_and_reps[0]:
        tmp_dict = {}

        tmp_dict["reps"] = weights_and_reps[1][i]

        for week in range(1, NUM_WEEKS + 1):
            key = "week{}".format(week)
            tmp_dict[key] = weight + (week - 1)*WEIGHT_PRECISION

        program.append(tmp_dict) 

        i += 1

    return program

def myround(x, prec=1, base=WEIGHT_PRECISION):
    return round(base*round(float(x)/base), prec)


def get_madcow(squat_5rm, bench_5rm, dl_5rm, ohp_5rm, row_5rm):
    program = {}

    program["squat_primary"] = get_12weeks(get_primary_day(squat_5rm, 1))
    program["bench_primary"] = get_12weeks(get_primary_day(bench_5rm, 1))
    program["row_primary"] = get_12weeks(get_primary_day(row_5rm, 1))

    return program

@app.route('/', methods=["GET", "POST"])
def index():
    form = RMForm(request.form)

    if request.method == "POST":
        squat = float(request.form["squat"])
        bench = float(request.form["bench"])
        dl = float(request.form["dl"])
        ohp = float(request.form["ohp"])
        row = float(request.form["row"])

    if form.validate_on_submit():
        c = get_columns()
        p = get_madcow(squat, bench, dl, ohp, row)

        return render_template('prog.html', data=p, columns=c)
    else:
        print(form.errors)

    return render_template('index.html', title='5x5', form=form)
