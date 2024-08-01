#Импорт
from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(100), nullable = False)


#Запуск страницы с контентом
@app.route('/')
def index_before_redirect():
    return redirect('/index_before')

@app.route('/index_before')
def index_before():
    return render_template('index_before.html')

#Динамичные скиллы
@app.route('/index', methods=['GET','POST'])
def process_form():
    button_python = None
    button_discord = None
    button_html = None
    button_db = None

    if request.method == 'POST':
        button_python = request.form.get('button_python')
        button_discord = request.form.get('button_discord')
        button_html = request.form.get('button_html')
        button_db = request.form.get('button_db')

    return render_template('index.html', button_python=button_python, button_discord=button_discord, button_html=button_html, button_db=button_db)


# Форма обратной связи
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    good = ''
    if request.method == 'POST':
        email = request.form['email']
        text = request.form['text']
        # Обработать данные обратной связи (например, сохранить в базу данных или отправить на email)
        print(f"Получен отзыв от {email}: {text}")
        with open('feedback.txt', 'a', encoding='utf-8') as file:
            file.write(f'Email: {email}\n')
            file.write(f'Text: {text}\n\n')
        # После отправки формы можно перенаправить пользователя на другую страницу или показать сообщение об успешной отправке
        good = 'Спасибо за Ваше сообщение. Оно было успешно отправлено.'
        return render_template('index_before.html', good = good)
    
    return render_template('feedback.html', good = good)


# Регистрационные поля
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
        users_db = User.query.all()
        for user in users_db:
            if form_login == user.email and form_password == user.password:
                return redirect('/index')
        error = 'Неверный логин или пароль!'
        return render_template('sign_in.html', error = error)
    else:
        return render_template('sign_in.html')
    
@app.route('/reg', methods = ['GET', 'POST'])
def reg():
    user_have = ''
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        
        existing_user = User.query.filter_by(email=login).first()
        if existing_user:
            user_have = 'Такой пользователь уже существует!'
            return render_template('register.html', user_have=user_have)
        else:
            user = User(email = login, password = password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
        
    return render_template('register.html')
    


if __name__ == "__main__":
    app.run(debug=True)