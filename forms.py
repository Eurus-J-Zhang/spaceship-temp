from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea

# Prolific ID and gender and age
class DemographicInfo(FlaskForm):
    id = StringField('Prolific ID', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('M','Male'),('F','Female'),('O','Others')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=80)])

# tank check
class TankForm(FlaskForm):
    tank_practice = RadioField('Practice', choices=[('A','A. Increase oxygen by 1%'),('B','B. Decrease oxygen by 1%'),
                                                    ('C','C. Increase carbon dioxide by 0.2%'),('D','D. Decrease carbon dioxide by 0.2%')], validators=[DataRequired()])

# tank reason
class ReasonForm(FlaskForm):
    tank_reason = RadioField('Reason', choices=[('A','A. Close Loop (O₂+0.5, CO₂+0.5)'),
                                                ('B','B. Vent (O₂−0.5, CO₂−0.5)'),
                                                ('C','C. Inject & Scrub (O₂+1, CO₂−1)'),
                                                ('D','D. Recycle (O₂−1, CO₂+1)')], validators=[DataRequired()])

# Here is the first emotion check
eleven_point_scale = [(str(i), f'Opt{i}') for i in range(11)]
eleven_point_scale_change = [(str(i), f'Opt{i}') for i in range(-5, 6)]

class EmotionFormPre(FlaskForm):
    emo1_competence = RadioField('Competence', choices=eleven_point_scale, validators=[DataRequired()])
    emo1_joy = RadioField('Joy', choices=eleven_point_scale, validators=[DataRequired()])
    emo1_pride = RadioField('Pride', choices=eleven_point_scale, validators=[DataRequired()])
    emo1_boredom = RadioField('Boredom', choices=eleven_point_scale, validators=[DataRequired()])
    emo1_irritation = RadioField('Irritation', choices=eleven_point_scale, validators=[DataRequired()]) 
    emo1_anxiety = RadioField('Anxiety', choices=eleven_point_scale, validators=[DataRequired()])  
    emo1_shame = RadioField('Shame', choices=eleven_point_scale, validators=[DataRequired()])  
    
    feedback1 = StringField('',validators=[DataRequired()],widget=TextArea())

class EmotionFormPost(FlaskForm):
    emo2_competence = RadioField('Competence', choices=eleven_point_scale_change, validators=[DataRequired()])
    emo2_joy = RadioField('Joy', choices=eleven_point_scale_change, validators=[DataRequired()])
    emo2_pride = RadioField('Pride', choices=eleven_point_scale_change, validators=[DataRequired()])
    emo2_boredom = RadioField('Boredom', choices=eleven_point_scale_change, validators=[DataRequired()])
    emo2_irritation = RadioField('Irritation', choices=eleven_point_scale_change, validators=[DataRequired()]) 
    emo2_anxiety = RadioField('Anxiety', choices=eleven_point_scale_change, validators=[DataRequired()])  
    emo2_shame = RadioField('Shame', choices=eleven_point_scale_change, validators=[DataRequired()])  
    
    feedback2 = StringField('',validators=[DataRequired()],widget=TextArea())