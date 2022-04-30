from flask import Blueprint,jsonify,render_template,request
from App.views.pandas import schedules

routesschedules = Blueprint('routesschedules',__name__)


# Convert csv em json
@routesschedules.route('/pandas/get/schedules', methods=['GET'])
def get_schedules():
    page = 1
    per_page = 10
    if request.method == 'GET':
        page = request.args.get('page')
        if page == None:
            page = 1
        per_page = request.args.get('per_page')
        if per_page == None:
            per_page = 10
    return schedules.get_schedules(page,per_page)

@routesschedules.route('/pandas/download/schedules/csv')
def download_file_schedules_csv():
    return schedules.download_schedules_csv()
