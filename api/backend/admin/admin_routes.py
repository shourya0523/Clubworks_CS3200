from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

admin = Blueprint('admin', __name__)

@admin.route('/clubs', methods = ['GET'])
def clubs_with_incomplete_profiles():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT ClubName, Description, LinkTree, CalendarLink, Complete
    FROM Clubs c
    WHERE c.Complete = False;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    if theData:
        the_response = make_response(theData)
        the_response.status_code = 200  
        the_response.mimetype = 'application/json'
        return the_response
    else:
        return {'Status':'No Club Registrations are incomplete'}

@admin.route('/memberships', methods = ['GET'])
def membership_count():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT c.ClubName, c.Description, c.LinkTree, c.CalendarLink, c.Complete,
        COUNT(m.NUID) AS MemberCount
    FROM Clubs c
    LEFT JOIN Membership m ON c.ClubId = m.ClubID
    GROUP BY c.ClubId, c.ClubName, c.Description, c.LinkTree, c.CalendarLink, c.Complete;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/supportrequests', methods = ['GET'])
def support_requests():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT sr.SupportRequestID, st.SupportType, sr.SupportRequestDescription, s.FirstName, s.LastName
    FROM SupportRequests sr
    JOIN SupportTypes st ON sr.SupportRequestType = st.SupportTypeId
    JOIN Students s ON sr.StudentID = s.NUID;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/signups', methods = ['GET'])
def user_signups():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT NUID, FirstName, LastName, Email, JoinDate, Complete
    FROM Students
    ORDER BY JoinDate DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/executives', methods = ['GET'])
def club_exectutives():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT e.NUID, s.FirstName, s.LastName, s.Email, c.ClubName, e.Position
    FROM Executives e
    JOIN Students s ON e.NUID = s.NUID
    JOIN Clubs c ON e.ClubID = c.ClubId;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/totalstudents', methods = ['GET'])
def count_total_students():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT COUNT(*) AS TotalStudents FROM Students;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/totalclubs', methods = ['GET'])
def count_total_clubs():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT COUNT(*) AS TotalClubs FROM Clubs;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/totalevents', methods = ['GET'])
def count_total_events():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT COUNT(*) AS TotalEvents FROM Events;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/pastmonth', methods = ['GET'])
def events_in_past_month():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT COUNT(*) AS RecentEvents
    FROM Events
    WHERE StartTime >= NOW() - INTERVAL 30 DAY;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/mostattended', methods = ['GET'])
def most_attended_events():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT e.Name AS EventName, COUNT(a.NUID) AS AttendanceCount
    FROM Attendance a
    JOIN Events e ON a.EventID = e.EventID
    GROUP BY a.EventID, e.Name
    ORDER BY AttendanceCount DESC
    LIMIT 5;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/studentsincomplete', methods = ['GET'])
def students_with_incomplete_profiles():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT NUID, FirstName, Email, JoinDate
    FROM Students
    WHERE Complete = FALSE
    ORDER BY JoinDate DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    if theData:
        the_response = make_response(theData)
        the_response.status_code = 200  
        the_response.mimetype = 'application/json'
        return the_response
    else:
        return {'Status':'No Student Profiles are incomplete'}
    return the_response

@admin.route('/incompleteregistrations', methods=['GET'])
def clubs_with_incomplete_registrations():
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT ClubName, Description, LinkTree, CalendarLink
    FROM Clubs
    WHERE Complete = FALSE
    ORDER BY ClubName;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    if theData:
        the_response = make_response(theData)
        the_response.status_code = 200  
        the_response.mimetype = 'application/json'
        return the_response
    else:
        return {'Status': 'No Club Registrations are incomplete'}

@admin.route('/eventandmembers', methods = ['GET'])
def event_and_member_count():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT c.ClubName,
      (SELECT COUNT(*) FROM Events e WHERE e.ClubId = c.ClubId) AS EventCount,
      (SELECT COUNT(*) FROM Membership m WHERE m.ClubID = c.ClubId) AS MemberCount
    FROM Clubs c
    ORDER BY EventCount DESC, MemberCount DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/signupsbydate', methods = ['GET'])
def get_signups_by_date():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT 
    DATE(JoinDate) AS JoinDate,
    COUNT(*) AS StudentCount
    FROM 
        Students
    GROUP BY 
        DATE(JoinDate)
    ORDER BY 
        JoinDate DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@admin.route('/engagementnetwork', methods=['GET'])
def engagement_network():
    cursor = db.get_db().cursor()

    membership_query = """
        SELECT s.FirstName, s.NUID, c.ClubName
        FROM Students s
        JOIN Membership m ON s.NUID = m.NUID
        JOIN Clubs c ON m.ClubID = c.ClubId;
    """
    cursor.execute(membership_query)
    memberships = cursor.fetchall()

    executive_query = """
        SELECT s.FirstName, s.NUID, c.ClubName
        FROM Executives e
        JOIN Students s ON e.NUID = s.NUID
        JOIN Clubs c ON e.ClubID = c.ClubId;
    """
    cursor.execute(executive_query)
    executives = cursor.fetchall()

    nodes = set()
    edges = []

    exec_set = set((row['NUID'], row['ClubName']) for row in executives)

    for row in memberships:
        student = f"{row['FirstName']} ({row['NUID']})"
        club = row['ClubName']
        nodes.add(student)
        nodes.add(club)

        edge_type = "executive" if (row['NUID'], club) in exec_set else "member"

        edges.append({
            "source": student,
            "target": club,
            "type": edge_type
        })

    response_data = {
        "nodes": list(nodes),
        "edges": edges
    }

    response = make_response(jsonify(response_data))
    response.status_code = 200
    return response