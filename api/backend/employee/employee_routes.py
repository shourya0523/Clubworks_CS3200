from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict


employees = Blueprint ('employees', __name__)


@employees.route('/employees', methods = ['GET'])
def get_all_employees():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT id, last_name, first_name, email_address, job_title
    FROM employees;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response