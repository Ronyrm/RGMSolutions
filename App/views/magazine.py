from flask import jsonify, request, render_template

def get_magazine():

    return render_template('layouts/magazine/mainmagazine.html')