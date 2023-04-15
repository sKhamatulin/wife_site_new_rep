import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from telegram_bot import send_message
from dotenv import load_dotenv

load_dotenv()
ADMIN_URL = os.getenv('ADMIN_URL')
DATA_BASE_URL = os.getenv('DATA_BASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATA_BASE_URL
app.config['SECRET_KEY'] = SECRET_KEY
app.config['ALLOWED_HOSTS'] = ['www.mariaevent.pythonanywhere.com',
                               'mariaevent.pythonanywhere.com']
db = SQLAlchemy(app)


class RequestForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    event_date = DateField('Дата мероприятия', validators=[DataRequired()])
    text = TextAreaField('Текст сообщения', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route('/')
def index():
    form = RequestForm()
    return render_template('index.html', form=form)


@app.route('/submit_request', methods=['POST'])
def request_form():
    form = RequestForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        event_date = form.event_date.data
        text = form.text.data
        new_request = Request(name=name, phone=phone,
                              event_date=event_date, text=text)
        db.session.add(new_request)
        db.session.commit()
        try:
            send_message(name, phone, event_date, text)
        except Exception as e:
            return f'Ошбика при отправке уведомления в телеграм {e}'
        return redirect(url_for('success'))
    else:
        print(form.errors)
        return redirect(url_for('index'))


@app.route('/success')
def success():
    return render_template('success.html')


@app.route(ADMIN_URL)
def last_ten_requests():
    requests = Request.query.order_by(-Request.id).all()
    return render_template('last_requests.html', requests=requests)


@app.route('/<int:id>/delete')
def request_delete(id):
    request = Request.query.get_or_404(id)
    try:
        db.session.delete(request)
        db.session.commit()
        return redirect(ADMIN_URL)
    except Exception:
        return 'При удалении заявки произошла ошибка'


if __name__ == '__main__':
    app.run(debug=True)
