#main_routesss
from flask import Blueprint , render_template,request
from App.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home") #home page route
def home():
    page = request.args.get('page',1,type=int)
    posts =  Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    #order by helps to show the latest post first
    return render_template('home.html',posts=posts)

#About Page route
@main.route("/about")
def about():
    return render_template('about.html',title='About')
