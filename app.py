from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
from wtforms import validators, StringField, TextAreaField, SubmitField
#from wtforms.validators import InputRequired
from flask_wtf import FlaskForm

app = Flask(__name__)
app.secret_key = 'Ra#.m@45'
bootstrap = Bootstrap(app)


class Frm1(FlaskForm):
    title = 'Badic Informatin'
    fname = StringField('Student\'s first name', validators=[validators.InputRequired()])
    lname = StringField('Student\'s Last name')
    submit = SubmitField('Next')


class Frm2(FlaskForm):
    title = 'Contact Information'
    email = StringField('Email', validators=[validators.InputRequired()])
    mobile = StringField('Mobile', validators=[validators.Length(min=10,max=10), validators.optional()]) ##, validators.NumberRange(min=6000000000, max=9999999999)])
    submit = SubmitField('Next')


class Frm3(FlaskForm):
    title = 'Address'
    address = TextAreaField('Address', validators=[validators.InputRequired()])
    submit = SubmitField('Next')


class Frm4(FlaskForm):
    title = 'Class/Grade information'
    grade = StringField('Grade', validators=[validators.InputRequired()])
    submit = SubmitField('Finish')


@app.route('/')
def index():
    return redirect(url_for('sforms', fpos=1))


@app.route('/sforms/<int:fpos>', methods=['GET', 'POST'])
def sforms(fpos):
    forms = {
        1: Frm1(),
        2: Frm2(),
        3: Frm3(),
        4: Frm4(),
    }

    form = forms.get(fpos, 1)

    if request.method == 'POST':
        if form.validate_on_submit():
            # Save form data to session
            session['pos{}'.format(fpos)] = form.data
            if fpos < len(forms):
                # Redirect to next step
                return redirect(url_for('sforms', fpos=fpos+1))
            else:
                # Redirect to finish
                return redirect(url_for('finish'))

    # If form data for this step is already in the session, populate the form with it
    if 'pos{}'.format(fpos) in session:
        form.process(data=session['pos{}'.format(fpos)])

    content = {
        'progress': int(fpos / len(forms) * 100),
        'fpos': fpos, 
        'form': form,
    }
    return render_template('mpfrms.html', **content)


@app.route('/finish')
def finish():
    data = {}
    for key in session.keys():
        if key.startswith('pos'):
            data.update(session[key])
    session.clear()
    return render_template('lastf.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

