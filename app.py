from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sign.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Sign(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(40), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Article %r>' % self.id



@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        sign = Sign(text=text)
        try:
            db.session.add(sign)
            db.session.commit()
            return redirect('/db')
        except:
            return 'При добавлении в БД произошла ошибка'
    else:
        return render_template("main.html")


@app.route('/db', methods = ['POST', 'GET'])
def info():
    sign = Sign.query.order_by(Sign._id.desc()).all()
    return render_template('db.html', sign=sign)


@app.route('/info/<int:_id>/del', methods = ['POST', 'GET'])
def delete(_id):
    sign = Sign.query.get_or_404(_id)
    try:
        db.session.delete(sign)
        db.session.commit()
        return redirect('/db')
    except:
        "Ошибка удаления данных из БД"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port='8080')