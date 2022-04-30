from flask import render_template, request


def index(currentuser):
    return render_template('layouts/index.html',currentuser=currentuser)