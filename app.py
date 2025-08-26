from flask import Flask,render_template,url_for,request, redirect, send_from_directory, session, flash
from flask_migrate import Migrate
from forms import EmotionFormPre, EmotionFormPost, DemographicInfo, TankForm, ReasonForm
import os
import pymysql
from models import db, Data

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')   
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = "iloveeurus"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()

def handle_form_submission(form, session_key, next_page):
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token', None)
        session[session_key] = data
        return redirect(next_page)
    return None

ACTION_DELTAS = {
    "A": ( +0.5, +0.5),  # Close Loop
    "B": ( -0.5, -0.5),  # Vent
    "C": ( +1.0, -1.0),  # Inject & Scrub
    "D": ( -1.0, +1.0),  # Recycle
}

@app.route('/', methods=['GET', 'POST'])
def index():
    session.pop("oxygen", None)
    session.pop("co2", None)
    session.pop("history_data", None)
    session['result'] = None
    form = DemographicInfo()
    response = handle_form_submission(form, 'index_data', 'emo_pre')
    if response:  
        return response
    return render_template('index.html',form=form)


@app.route('/emo_pre', methods=['GET', 'POST'])
def emo_pre():
    form = EmotionFormPre()
    response = handle_form_submission(form, 'emo_pre_data', 'system_intro')
    if response:  
        return response
    return render_template('emo_pre.html', form=form)



# p9
@app.route('/emo_post', methods=['GET', 'POST'])
def emo_post():
    form = EmotionFormPost()

    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token', None)
        session['emo_post_data'] = data

        index_data = session.get('index_data')
        tank_practice_data = session.get('tank_practice_data')
        history_data = session.get('history_data')
        history_str = ",".join(history_data)
        emo_pre_data = session.get('emo_pre_data')
        emo_post_data = session.get('emo_post_data')
        result_data = session.get('result')

        combined_data = {**index_data,**tank_practice_data, "history": history_str, "result":result_data,
                         **emo_pre_data, **emo_post_data}
        data = Data(**combined_data)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for("ending")) 
    return render_template('emo_post.html',form=form)

# # p9
# @app.route('/appraisal', methods=['GET', 'POST'])
# def appraisal():
#     form = AppraisalForm()

#     if form.validate_on_submit():
#         data = form.data
#         data.pop('csrf_token', None)
#         session['appraisal_data'] = data

#         index_data = session.get('index_data')
#         tank_practice_data = session.get('tank_practice_data')
#         # tank_reason_data = session.get('tank_reason_data')
#         step_data = session.get('')
#         history_data = session.get('history_data')
#         emo_data = session.get('emo_data')
#         appraisal_data = session.get('appraisal_data')

#         combined_data = {**index_data,**tank_practice_data, **history_data, 
#                          **emo_data, **appraisal_data}
#         data = Data(**combined_data)
#         db.session.add(data)
#         db.session.commit()
#         return redirect(url_for("ending")) 
#     return render_template('appraisal.html',form=form)

# P1
@app.route('/system_intro')
def system_intro():
    return render_template('system_intro.html')

# P2
@app.route('/tank_check', methods=['GET', 'POST'])
def tank_check():
    form = TankForm()
    CORRECT_ANSWER = "B"

    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            data.pop('csrf_token', None)
            session['tank_practice_data'] = data
            user_answer = request.form.get("tank_practice") 
            # Instead of sending a message, just send a boolean flag
            session['is_correct'] = (user_answer == CORRECT_ANSWER)
            session.modified = True
            return redirect(url_for("tank_check"))  # Reload the same page
    return render_template('tank_check.html', form = form)

# P3
@app.route('/ship_situation')
def ship_situation():
    return render_template('ship_situation.html')

# P4
@app.route('/day_choice')
def day_choice():
    return render_template('day_choice.html')

# P5
@app.route('/alarm_day')
def alarm_day():
    return render_template('alarm_day.html')

@app.route('/tank_reason', methods=['GET', 'POST'])
def tank_reason():
    session.setdefault("oxygen", 19.0)
    session.setdefault("co2", 0.6)
    session.setdefault("history_data", [])

    form = ReasonForm()

    # Success state (use session values)
    success = (20.0 <= session["oxygen"] <= 22.0) and (0.4 <= session["co2"] <= 0.8)
    step_number = len(session["history_data"])
    failed = step_number >= 6 and not success  # fail if you hit 6 steps without success

    if request.method == "POST":
        # If already successful, don't validate (no radios present) — just continue to result
        if success:
            # step_number=len(history)
            return redirect(url_for("result_success"))
        if failed:
            return redirect(url_for("result_fail"))

        # Otherwise, we expect a radio choice; validate and apply action
        if form.validate_on_submit():
            action = form.tank_reason.data
            d_o2, d_co2 = ACTION_DELTAS[action]

            trial_o2 = round(session["oxygen"] + d_o2, 1)
            trial_co2 = round(session["co2"] + d_co2, 1)

            if trial_o2 < 0 or trial_co2 < 0:
                form.tank_reason.errors.append(
                    "Invalid action: a gas level would drop below 0%."
                )
            else:
                session["oxygen"] = trial_o2
                session["co2"] = trial_co2
                # record action in history
                history = session.get("history_data", [])
                history.append(action)   # just the action name (A/B/C/D)
                session["history_data"] = history
                return redirect(url_for("tank_reason"))
        else:
            # No selection submitted (e.g., user clicked Continue without choosing)
            # Only add this error when not in success mode.
            if not form.tank_reason.data:
                form.tank_reason.errors.append("Please select an action.")

    actions = session.get("history_data", [])
    step_number = len(actions)
    actions_str = ", ".join(actions) if actions else "None"

    return render_template(
        "tank_reason.html",
        form=form,
        oxygen=session["oxygen"],
        co2=session["co2"],
        success=success,
        failed=failed,
        step_number=step_number,
        actions_str=actions_str,
    )
    # response = handle_form_submission(form, 'tank_reason_data', 'result')
    # if response:
    #     return response
    # return render_template('tank_reason.html',form = form)

# P7
@app.route('/result_success')
def result_success():
    session['result']='success'  # record the result
    return render_template('result_success.html')

# P8
@app.route('/result_fail')
def result_fail():
    session['result']='fail'  # record the result
    return render_template('result_fail.html')

# end page
@app.route('/ending')
def ending():
    return render_template('ending.html')

if __name__ == "__main__":
    app.run(debug=True)