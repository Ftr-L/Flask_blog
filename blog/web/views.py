from flask import request, render_template, Blueprint, redirect, url_for

# 编码解码
from back.models import Article, ArticleType

web_blue = Blueprint('web', __name__)


# 跳转主页
@web_blue.route('/', methods=['GET'])
def blog():
    return render_template('web/index.html')


# 主页
@web_blue.route('/blog_index/', methods=['GET', 'POST'])
def blog_index():
    articles = Article.query.limit(10).all()
    return render_template('web/index.html', articles=articles)


# 博客日记
@web_blue.route('/blog_diary/', methods=['GET', 'POST'])
def blog_diary():
    article = ArticleType.query.limit(10).all()
    articles = Article.query.limit(10).all()
    return render_template('web/list.html', article=article, articles=articles)


# 优秀个人博客
@web_blue.route('/blog_good/', methods=['GET', 'POST'])
def blog_good():
    if request.method == 'GET':
        return render_template('web/daohang.html')


# 关于我
@web_blue.route('/blog_about/', methods=['GET', 'POST'])
def blog_about():
    if request.method == 'GET':
        return render_template('web/about.html')


# 添加文章
@web_blue.route('/return_back/', methods=['GET', 'POST'])
def return_back():
    return redirect(url_for('back.admin_login'))


# 内容
@web_blue.route('/blog_content/<int:id>/', methods=['GET', 'POST'])
def blog_content(id):
    if request.method == 'GET':
        # 标签云 取标签id
        article = ArticleType.query.limit(10).all()
        # 通过标签 取对应id文章内容
        content_id = Article.query.filter_by(id=id).first()
        # 点击排名 文章显示
        articles = Article.query.limit(10).all()
        # 通过id 取 > id值 的第一个文章id
        up = Article.query.filter(Article.id > id).first()
        # 通过id 取 < id值 的第一个文章id
        down = Article.query.filter(Article.id < id).first()
        return render_template('web/info.html', content_id=content_id, article=article, articles=articles, up=up, down=down)
