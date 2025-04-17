
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict


analyst = Blueprint ('analyst', __name__)

@analyst.route('/get_clubs', methods = ['GET'])
def get_clubs():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT *
    FROM Clubs c;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response


@analyst.route('/get_clubs_information', methods = ['GET'])
def get_clubs_information():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT c.Description, c.LogoImg, c.LinkTree, c.CalendarLink , c.ClubName
    FROM Clubs c;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response



@analyst.route('/get_performance', methods = ['GET'])
def get_club_performance():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT
    c.ClubName,
    i.InterestName,
    et.EventType,
    COUNT(DISTINCT a.NUID) AS TotalAttendance
FROM Clubs c
JOIN Events e ON c.ClubId = e.ClubId
JOIN EventTypes et ON e.Type = et.EventTypeId
LEFT JOIN Attendance a ON e.EventID = a.EventID
LEFT JOIN AppealsTo ap ON c.ClubId = ap.ClubId
LEFT JOIN Interests i ON ap.InterestID = i.InterestID
GROUP BY c.ClubName, i.InterestName, et.EventType
ORDER BY et.EventType, TotalAttendance DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response


@analyst.route('/demographics_insights', methods = ['GET'])
def demographics_insights():

    cursor = db.get_db().cursor()
    the_query = '''
SELECT s.Major, YEAR(s.GradDate) AS GraduationYear, COUNT(DISTINCT a.EventID) AS EventsAttended
FROM Students s
JOIN Attendance a ON s.NUID = a.NUID
GROUP BY s.Major, YEAR(s.GradDate)
ORDER BY EventsAttended DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@analyst.route('/active_member', methods = ['GET'])
def get_active_members():
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT 
        s.NUID, 
        s.FirstName, 
        s.LastName, 
        COUNT(DISTINCT a.EventID) AS EventsAttended, 
        c.ClubID,
        c.ClubName
    FROM Attendance a
    JOIN Students s ON a.NUID = s.NUID
    JOIN Membership m ON s.NUID = m.NUID
    JOIN Clubs c ON m.ClubID = c.ClubID
    GROUP BY s.NUID, s.FirstName, s.LastName, c.ClubID, c.ClubName
    ORDER BY EventsAttended DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@analyst.route('/retention', methods = ['GET'])
def get_retention_rate():

    cursor = db.get_db().cursor()
    the_query = '''
SELECT c.ClubName,
      COUNT(DISTINCT m.NUID) AS TotalMembers,
      COUNT(DISTINCT a.NUID) AS ActiveParticipants,
      (COUNT(DISTINCT a.NUID) / COUNT(DISTINCT m.NUID)) * 100 AS RetentionRate
FROM Clubs c
JOIN Membership m ON c.ClubId = m.ClubID
LEFT JOIN Attendance a ON m.NUID = a.NUID AND EXISTS (
   SELECT 1 FROM Events e WHERE e.ClubId = c.ClubId AND a.EventID = e.EventID
)
GROUP BY c.ClubName;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response


@analyst.route('/attendance_major', methods = ['GET'])
def get_attendance_by_major():

    cursor = db.get_db().cursor()
    the_query = '''
SELECT e.Name AS EventName, s.Major, COUNT(*) AS AttendanceCount
FROM Attendance a
JOIN Events e ON a.EventID = e.EventID
JOIN Students s ON a.NUID = s.NUID
GROUP BY e.EventID, e.Name, s.Major
ORDER BY AttendanceCount DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@analyst.route('/engagement_major', methods = ['GET'])
def get_engagement_by_major():

    cursor = db.get_db().cursor()
    the_query = '''
SELECT c.ClubName, s.Major, COUNT(a.EventID) AS EventAttendance
FROM Membership m
JOIN Students s ON m.NUID = s.NUID
JOIN Clubs c ON m.ClubID = c.ClubId
LEFT JOIN Attendance a ON m.NUID = a.NUID
GROUP BY c.ClubName, s.Major
ORDER BY EventAttendance DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@analyst.route('/performance_metrics', methods = ['GET'])
def performance_metrics():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT 
        c.ClubName,
        COUNT(DISTINCT a.NUID) AS TotalAttendance,
        AVG(f.Rating) AS AvgRating,
        COUNT(DISTINCT r.RequestID) AS FundingRequests,
        GROUP_CONCAT(DISTINCT f.Description SEPARATOR ', ') AS FeedbackDescription
    FROM Clubs c
    JOIN Feedback f ON c.ClubId = f.ClubID
    LEFT JOIN Events e ON c.ClubId = e.ClubId
    LEFT JOIN Attendance a ON e.EventID = a.EventID
    LEFT JOIN Executives ex ON ex.ClubID = c.ClubId
    LEFT JOIN Requests r ON r.ExecutiveID = ex.NUID AND r.ExecutiveClub = ex.ClubID AND r.Type = 2
    GROUP BY c.ClubName
    ORDER BY TotalAttendance DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@analyst.route('/funding_requests', methods = ['GET'])
def get_funding_request():

    cursor = db.get_db().cursor()
    the_query = '''
SELECT r.RequestID, rt.RequestType, r.Status, r.CreatedTime, c.ClubName
FROM Requests r
JOIN RequestTypes rt ON r.Type = rt.RequestTypeId
JOIN Executives e ON r.ExecutiveID = e.NUID AND r.ExecutiveClub = e.ClubID
JOIN Clubs c ON e.ClubID = c.ClubId
LEFT JOIN Events ev ON ev.ClubId = c.ClubId
LEFT JOIN Attendance a ON a.EventID = ev.EventID
LEFT JOIN Feedback f ON f.ClubID = c.ClubId
GROUP BY r.RequestID, rt.RequestType, r.Status, r.CreatedTime, c.ClubName
ORDER BY r.CreatedTime DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@analyst.route('/club_interests', methods = ['GET'])
def get_club_interest_filtering():

    cursor = db.get_db().cursor()
    the_query = '''
SELECT i.InterestName, c.ClubName
FROM Interests i
JOIN AppealsTo a ON i.InterestID = a.InterestID
JOIN Clubs c ON a.ClubID = c.ClubID;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@analyst.route('/club_engagement', methods = ['GET'])
def get_club_engagement():

    cursor = db.get_db().cursor()
    the_query = '''
SELECT 
    c.ClubName,
    COUNT(DISTINCT a.NUID) AS TotalAttendance,
    COUNT(DISTINCT f.FeedbackID) AS FeedbackCount
FROM Clubs c
LEFT JOIN Events ev ON c.ClubId = ev.ClubId
LEFT JOIN Attendance a ON ev.EventID = a.EventID
LEFT JOIN Feedback f ON c.ClubId = f.ClubID
GROUP BY c.ClubName
ORDER BY TotalAttendance DESC;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response

@analyst.route('/top_club', methods=['GET'])
def top_club():
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT * FROM (
        SELECT 
            c.ClubName,
            COUNT(DISTINCT a.NUID) AS TotalAttendance,
            COUNT(DISTINCT f.FeedbackID) AS FeedbackCount
        FROM Clubs c
        LEFT JOIN Events ev ON c.ClubId = ev.ClubId
        LEFT JOIN Attendance a ON ev.EventID = a.EventID
        LEFT JOIN Feedback f ON c.ClubId = f.ClubID
        GROUP BY c.ClubName
        ORDER BY TotalAttendance DESC
    ) AS RankedClubs
    LIMIT 3;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200  
    the_response.mimetype = 'application/json'
    return the_response



