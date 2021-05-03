#posts_routes.py
from flask import ( render_template,url_for,flash,
                    redirect,request,abort,  Blueprint)
from flask_login import current_user,login_required
from App import db
from App.models import Post
from App.posts.forms import PostForm

posts = Blueprint('posts', __name__)


#new post
@posts.route("/post/new" , methods= ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data ,author =  current_user)
        db.session.add(post)
        db.session.commit()
        flash("your post has been created" , 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='New Post',form =form ,legend= 'New Post')


# getting to the post via post_id and displaying indiviuallly
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) #give me the id or return 404 if id doesnot exixts
    return render_template('post.html' , title = post.title , post=post)

# Updating the post 
@posts.route("/post/<int:post_id>/update",methods= ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #403 response is for http response for forbidden route 
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() #directly commiting as it is already in data bases
        flash("your post has been updated ", 'success')
        print("Post updated")
        return redirect(url_for('posts.post',post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post',form =form , legend= 'Update Post')
    
#Deelete post route
@posts.route("/post/<int:post_id>/delete",methods= ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #403 response is for http response for forbidden rou
    db.session.delete(post)
    db.session.commit()
    flash('Your post hass been deleted', 'success')
    return redirect(url_for('main.home'))
