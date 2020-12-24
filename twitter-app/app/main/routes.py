from datetime import datetime
from flask import render_template, request, current_app, redirect, url_for, flash, g
from flask_login import login_required, current_user
from app.main.forms import PostForm, SearchForm, EmptyForm, EditProfileForm, MessageForm
from app.main import bp
from app.models import User, Post, Message
from app import db


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = 'en'
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index', _external=True))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num, _external=True) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num, _external=True) \
        if posts.has_prev else None
    return render_template('main/index.html', title='Home',
                           form=form, posts=posts.items,
                           prev_url=prev_url,
                           next_url=next_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num, _external=True) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num, _external=True) \
        if posts.has_prev else None
    return render_template('main/index.html', title='Explore',
        posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore', _external=True))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page+1, _external=True) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page-1, _external=True) \
        if page > 1 else None
    return render_template('main/search.html', title='Search', posts=posts, next_url=next_url,
        prev_url=prev_url)


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('main.user', username=recipient, _external=True))
    return render_template('main/send_message.html', title='Send Message',
        form=form, recipient=recipient)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num, _external=True) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num, _external=True) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('main/user.html', user=user, posts=posts.items,
        next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.edit_profile', _external=True))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', title='Edit Profile',
        form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f"User {username} not found.")
            return redirect(url_for('main.index', _external=True))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username, _external=True))
        current_user.follow(user)
        db.session.commit()
        flash(f"You are following {username}")
    return redirect(url_for('main.index', _external=True))


@bp.route('/unfollow/username', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f"User {username} not found")
            return redirect(url_for('main.index', _external=True))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username, _external=True))
        current_user.unfollow(user)
        db.session.commit()
        flash(f"You are not following {username}")
    return redirect(url_for('main.index', _external=True))
