"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import redirect
from Swapify import app

@app.route('/')
@app.route('/login')
def log():
    scopes = "user-read-private user-read-email";
    my_client_id = "b167636c03db464bac2a9a61c6663685"
    my_redirect_uri = "http://localhost:5555/home"
    return redirect('https://accounts.spotify.com/authorize' +
  '?client_id=' + my_client_id +
  '&redirect_uri=' + my_redirect_uri +
  '&response_type=token')



@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page. This message is in views.py'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
