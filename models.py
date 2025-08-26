from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    id= db.Column(db.String(20))
    gender=db.Column(db.String(1))
    age = db.Column(db.Integer)

    tank_practice = db.Column(db.String(10))
    
    history = db.Column(db.String(255), nullable=False)

    emo1_competence = db.Column(db.Integer)
    emo1_joy = db.Column(db.Integer)
    emo1_pride = db.Column(db.Integer)
    emo1_boredom = db.Column(db.Integer)
    emo1_irritation = db.Column(db.Integer)
    emo1_anxiety = db.Column(db.Integer)
    emo1_shame = db.Column(db.Integer)

    emo2_competence = db.Column(db.Integer)
    emo2_joy = db.Column(db.Integer)
    emo2_pride = db.Column(db.Integer)
    emo2_boredom = db.Column(db.Integer)
    emo2_irritation = db.Column(db.Integer)
    emo2_anxiety = db.Column(db.Integer)
    emo2_shame = db.Column(db.Integer)

    feedback1 = db.Column(db.Text)
    feedback2 = db.Column(db.Text)

    result = db.Column(db.String(10))



    # so the names here will be in the database