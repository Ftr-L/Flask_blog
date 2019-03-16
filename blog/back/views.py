from flask import request, render_template, Blueprint, redirect, url_for, session
# 编码解码
from werkzeug.security import generate_password_hash, check_password_hash
from back.models import db, User, Article, ArticleType
from utils.functions import is_login

back_blue = Blueprint('back', __name__)


# 登录主页
@back_blue.route('/index/')
@is_login
def admin_index():
    return render_template('back/index.html')


# 注册账号
@back_blue.route('/register/', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        im_login = request.form.get('im_login')
        if im_login:
            return redirect(url_for('back.admin_login'))
        # 判断参数是否全部输入
        if username and password and password2:
            # 判断账号是否注册
            user = User.query.filter(User.u_name == username).first()
            if user:
                error = '该账号已注册，请重新输入！'
                return render_template('back/register.html', error=error)
            else:
                # 判断密码是否一致
                if password == password2:
                    admin = User()
                    admin.u_name = username
                    admin.u_password = generate_password_hash(password)
                    admin.u_password2 = password2
                    admin.save()
                    return redirect(url_for('back.admin_login'))
                else:
                    error = '密码不一致！'
                    return render_template('back/register.html', error=error)
        else:
            error = '确保信息输入完整'
            return render_template('back/register.html', error=error)


# 登录账号
@back_blue.route('/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            np_name = User.query.filter(User.u_name == username).first()
            if not np_name:
                error = '该账号未注册！'
                return render_template('back/login.html', error=error)
            if not check_password_hash(np_name.u_password, password):
                error = '密码错误！请重新输入！'
                return render_template('back/login.html', error=error)
            session['user_id'] = np_name.id
            return redirect(url_for('back.admin_index'))

        else:
            error = '请填写完整信息！'
            return render_template('back/login.html', error=error)


# 注销帐号
@back_blue.route('/logout/', methods=['GET'])
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.admin_login'))


# 文章分类
@back_blue.route('/a_type/', methods=['GET', 'POST'])
def a_type():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/category_list.html', types=types)


# 添加文章分类
@back_blue.route('/add_type/', methods=['GET', 'POST'])
def add_type():
    if request.method == 'GET':
        return render_template('back/category_add.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            # 保存分类信息
            art_type = ArticleType()
            art_type.t_name = atype
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.a_type'))
        else:
            error = '请填写分类信息'
            return render_template('back/category_add.html', error=error)


# 删除分类功能
@back_blue.route('/del_type/<int:id>', methods=['GET'])
def del_type(id):
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))


# 文章列表
@back_blue.route('/article_list/', methods=['GET'])
def article_list():
    articles = Article.query.all()
    return render_template('back/article_list.html', articles=articles)


# 添加文章
@back_blue.route('/article_add/', methods=['GET', 'POST'])
def article_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/article_detail.html', types=types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        if title and desc and category and content:
            # 保存
            art = Article()
            art.title = title
            art.desc = desc
            art.content = content
            art.type = category
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('back.article_list'))
        else:
            error = '请填写完整的文章信息'
            return render_template('back/article_detail.html', error=error)


# 删除文章
@back_blue.route('/article_del/<int:id>/', methods=['GET'])
def article_del(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('back.article_list'))


# 用户信息
@back_blue.route('/user_list/', methods=['GET'])
def user_list():
    users = User.query.all()
    return render_template('back/user_list.html', users=users)


# 用户删除
@back_blue.route('/user_del/<int:id>', methods=['GET'])
def user_del(id):
    users = User.query.get(id)
    db.session.delete(users)
    db.session.commit()
    return redirect(url_for('back.user_list'))


# 添加新用户
@back_blue.route('/user_add/', methods=['GET', 'POST'])
def users_add():
    if request.method == 'GET':
        return render_template('back/goods_detail.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 判断参数是否全部输入
        if username and password and password2:
            # 判断账号是否注册
            user = User.query.filter(User.u_name == username).first()
            if user:
                error = '该账号已注册，请重新输入！'
                return render_template('back/goods_detail.html', error=error)
            else:
                # 判断密码是否一致
                if password == password2:
                    admin = User()
                    admin.u_name = username
                    admin.u_password = generate_password_hash(password)
                    admin.u_password2 = password2
                    admin.save()
                    return redirect(url_for('back.user_list'))
                else:
                    error = '密码不一致！'
                    return render_template('back/goods_detail.html', error=error)
        else:
            error = '确保信息输入完整'
            return render_template('back/goods_detail.html', error=error)



