# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from webapp.extensions import login_manager
from webapp.public import articles
from webapp.public.forms import LoginForm
from webapp.user.forms import RegisterForm
from webapp.user.models import User
from webapp.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    #article = get_todays_news()

    #articles.get_article("http://www.letemps.ch/economie/2016/06/16/bns-ne-croit-brexit-s-y-prepare")
    article = articles.get_article("http://www.letemps.ch/sciences/2016/06/18/traversee-atlantique-bertrand-piccard")

    user_recommendations = get_user_recommendations()

    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    recommendations = article.get_system_recommendations()
    return render_template(
        'public/home.html',
        form=form,
        article=article,
        system_recommendations=recommendations,
        user_recommendations=user_recommendations
    )

def get_user_recommendations():
    return [
        {
            "date" : "date",
            "newspaper" : "newspaper",
            "title" : "title",
            "comment" : "comment"
        },
    ]

def get_archive_from_id(id, page, keywords):
    return {
        "url" : "http://www.letempsarchives.ch/page/%s/%s/%s" % (id, page, keywords)
    }

@blueprint.route('/compare', methods=['GET'])
def compare():

    article1_id = request.args.get('source_id')
    article2_id = request.args.get('destination_id')

    article1 = articles.get_article(article1_id)
    article2 = articles.get_article(article2_id)
    #article1 = scrapeArticle(article1.url)
    #article2 = []#get_archive_from_id("JDG_1923_07_08", 10, "conference%20de%20lausanne")
    
    recommendations = article1.get_system_recommendations()

    user_recommendations = get_user_recommendations()

    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template(
        'public/compare.html',
        form=form,
        article1=article1,
        article2=article2,
        system_recommendations=recommendations,
        user_recommendations=user_recommendations
    )



@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)
