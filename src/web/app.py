from flask import Flask, render_template, jsonify, request, flash, make_response, redirect, url_for
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


def get_primary_day(rm5, exercise_type):
    starting_rm5 = rm5 - 10
    weights_and_reps = [[], []]
    for k in reversed(range(4 + exercise_type)):
        weights_and_reps[0].append(myround(starting_rm5*(1 - k*WEIGHT_INCREMENT)))
        weights_and_reps[1].append(5)

    return weights_and_reps


def get_secondary_day(rm5, exercise_type):
    weights_and_reps = get_primary_day(rm5, exercise_type)

    weights_and_reps[0][-1] += 2.5
    weights_and_reps[0].append(weights_and_reps[0][2])

    weights_and_reps[1][-1] = 3
    weights_and_reps[1].append(8)

    return weights_and_reps


def get_tertiary_day(rm5, exercise_type):
    weights_and_reps = get_primary_day(rm5, exercise_type)

    weights_and_reps[0].pop()
    weights_and_reps[1].pop()

    weights_and_reps[0][-1] = weights_and_reps[0][-2]
    weights_and_reps[1][-1] = weights_and_reps[1][-2]

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


def get_madcow(rm_5s):
    squat_5rm = float(rm_5s["squat"]) 
    bench_5rm = float(rm_5s["bench"])
    dl_5rm = float(rm_5s["dl"])
    ohp_5rm = float(rm_5s["ohp"])
    row_5rm = float(rm_5s["row"])

    program = {}

    program["squat_primary"] = get_12weeks(get_primary_day(squat_5rm, 1))
    program["bench_primary"] = get_12weeks(get_primary_day(bench_5rm, 1))
    program["row_primary"] = get_12weeks(get_primary_day(row_5rm, 1))

    program["dl_primary"] = get_12weeks(get_primary_day(dl_5rm, 0))
    program["ohp_primary"] = get_12weeks(get_primary_day(ohp_5rm, 0))
    program["squat_tertiary"] = get_12weeks(get_tertiary_day(squat_5rm, 1))

    program["squat_secondary"] = get_12weeks(get_secondary_day(squat_5rm, 1))
    program["bench_secondary"] = get_12weeks(get_secondary_day(bench_5rm, 1))
    program["row_secondary"] = get_12weeks(get_secondary_day(row_5rm, 1))

    return program


def set_cookies_from_dict(rm_5s):
    c = get_columns()
    p = get_madcow(rm_5s)
    resp = make_response(render_template("madcow.html", data=p, columns=c))
    resp.set_cookie("squat", rm_5s["squat"])
    resp.set_cookie("bench", rm_5s["bench"])
    resp.set_cookie("dl", rm_5s["dl"])
    resp.set_cookie("ohp", rm_5s["ohp"])
    resp.set_cookie("row", rm_5s["row"])

    return resp

def get_cookies_as_dict():
    rm_5s = dict(squat=request.cookies.get("squat"),
                 bench=request.cookies.get("bench"),
                 dl=request.cookies.get("dl"),
                 ohp=request.cookies.get("ohp"),
                 row=request.cookies.get("row")
                 )

    for key, val in rm_5s.items():
        if val == None or val == "":
            return None
        else:
            return rm_5s


@app.route("/", methods=["GET", "POST"])
def index():
    rm_5s = get_cookies_as_dict()

    if rm_5s:
        c = get_columns()
        p = get_madcow(rm_5s)

        return render_template("madcow.html", data=p, columns=c)
    else:
        print("No cookies stored.")

    form = RMForm(request.form)

    if request.method == "POST":
        rm_5s = dict(squat=request.form["squat"],
                     bench=request.form["bench"],
                     dl=request.form["dl"],
                     ohp=request.form["ohp"],
                     row=request.form["row"]
                     )
    if form.validate_on_submit():
        resp = set_cookies_from_dict(rm_5s)
        return resp
    else:
        print(form.errors)

    return render_template("index.html", title="5x5", form=form)


@app.route("/clear", methods=["GET", "POST"])
def clear_cookies():
    form = RMForm(request.form)

    if request.method == "POST":
        rm_5s = dict(squat=request.form["squat"],
                     bench=request.form["bench"],
                     dl=request.form["dl"],
                     ohp=request.form["ohp"],
                     row=request.form["row"]
                     )
    if form.validate_on_submit():
        resp = set_cookies_from_dict(rm_5s)
        return resp
    else:
        print(form.errors)

    return render_template("index_clear.html", title="5x5", form=form)
