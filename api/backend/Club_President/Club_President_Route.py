########################################################
# club_president blueprint of endpoints
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Creating a new Blueprint object, which is a collection of 
# routes.
club_president = Blueprint('club_president', __name__)

#------------------------------------------------------------
# Get all Attendance from the system
@club_president.route('/club_president', methods=['GET'])
def get_attendancecount():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT e.Name AS EventName, COUNT(a.NUID) AS AttendanceCount
    FROM Events e
    LEFT JOIN Attendance a ON e.EventID = a.EventID
    WHERE e.ClubId = 2 -- Replace with Tyla's ClubID (2 for Business Society)
    GROUP BY e.Name
    ORDER BY AttendanceCount DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response
