from flask import Flask, render_template, request, url_for, flash
from flask_login.utils import logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin


import bd
import pyshorteners
import pyperclip


bd.db_create()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hgfg85thf1hr1th56t89h5fg1ht'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь, чтобы перейти к сокращателю ссылок'

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, bd)


menu = [
{'name': 'Регистрация', 'url': 'register'},
{'name': 'Авторизация', 'url': 'login'},
{'name': 'Личный кабинет', 'url': 'profile'},]



@app.route('/', methods=['POST', 'GET'])
def index(): 
    print(url_for('index'))
    links = bd.db_linkAll()
    if request.method == 'POST':
        url = request.form.get('link')
        link = pyshorteners.Shortener().tinyurl.short(url)
        pyperclip.copy(link)
        flash(f'Ваша ссылка: {link}')
    return render_template('index.html', links = links,  menu = menu) 


@app.route('/register', methods=['POST', 'GET']) 
def register(): 
    print(url_for('register'))
    if request.method == 'POST': 
        if len(request.form['password']) >= 8 and len(request.form['login'])>0:
            login = request.form['login'] 
            password = request.form['password'] 
            hash = generate_password_hash(password)
            reg = bd.db_loginId(login)
            if reg == 1:
                flash("Такой логин уже существует")
            elif reg == 0:
                bd.db_reg_user(login, hash)
                flash("Вы успешно зарегистрировались")
                return redirect(url_for('login'))
        else:
            flash('Пароль должен содержать не менее 8 символов')

    return render_template('register.html', title='Регистрация', menu = menu) 

@app.route('/login', methods=['POST', 'GET']) 
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    print(url_for('login'))
    if request.method == 'POST': 
        user = bd.getLogin(request.form['login']) 
        if user and check_password_hash(user[2], request.form['password']):
            userLogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userLogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))
            
        flash('Неверный логин или пароль')
     
    return render_template('login.html', title='Авторизация', menu = menu) 


@app.route('/profile',  methods=['POST', 'GET']) 
@login_required
def profile(): 
    try:
        user = bd.getUser(current_user.get_id())
        login = user[1]
        nameurl = request.form.get('nameurl')
        url = request.form.get('link')
        link = pyshorteners.Shortener().tinyurl.short(url)
        pyperclip.copy(link)
        bd.db_short(user[0], nameurl, link)
        flash(f'Ваша новая ссылка: {link}')
    except:
        flash('')

    links = bd.db_linkForUser(user[0])
    return render_template('profile.html', title='Личный кабинет', login = login, links = links, menu = menu)


@app.route('/<int:id>') 
def delete(id):
    user = bd.getUser(current_user.get_id())
    try:
        bd.db_deleteLink(user[0], id)
        flash('Ссылка успешно удалена')
        return redirect('/profile')
    except:
        flash('Произошла ошибка в удалении')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('login'))


if __name__ == "__main__": 
    app.run(debug=True)
