from flask import Flask,render_template,url_for,request, redirect, send_from_directory, session, flash
from flask_migrate import Migrate
from forms import EmotionFormPre, EmotionFormPost, DemographicInfo, TankForm, ReasonForm, FollowForm
import os
import pymysql
from models import db, Data

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')   
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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


@app.route('/', methods=['GET', 'POST'])
def index():
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

        emo_pre_data = session.get('emo_pre_data')
        emo_post_data = session.get('emo_post_data')

        combined_data = {**index_data,**tank_practice_data,**emo_pre_data, **emo_post_data}
        data = Data(**combined_data)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for("ending")) 
    return render_template('emo_post.html',form=form)


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
    session.setdefault("modal_shown", False)
    form = ReasonForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Instead of redirecting directly, mark modal as ready
            session["modal_shown"] = True
            return redirect(url_for("tank_reason"))

    show_modal = session.pop("modal_shown", False)  # read & clear flag

    return render_template(
        "tank_reason.html",
        form=form,
        show_modal=show_modal
    )


# P7
@app.route('/result_success')
def result_success():
    return render_template('result_success.html')


@app.route('/guided', methods=['GET', 'POST'])
def guided():
    form = FollowForm()
    if form.validate_on_submit():
        return redirect(url_for("result_success"))
    return render_template('guided.html',form=form)

# end page
@app.route('/ending')
def ending():
    return render_template('ending.html')

if __name__ == "__main__":
    app.run(debug=True)