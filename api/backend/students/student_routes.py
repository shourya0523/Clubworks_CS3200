from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

students = Blueprint('students', __name__)

@students.route('/student_login', methods=['GET'])
def student_login():
    email = request.args.get('email')
    password = request.args.get('password')
    
    if not email or not password:
        response = make_response(jsonify({
            'status': 'error',
            'message': 'Email and password are required'
        }))
        response.status_code = 400
        return response
    
    query = '''
    SELECT NUID
    FROM Students
    WHERE Email = %s AND Password = %s;
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query, (email, password))
    
    result = cursor.fetchall()
    
    if result:
        response = make_response(result[0]['NUID'])
        response.status_code = 200
    else:
        response = make_response(jsonify({
            'status': 'error',
            'message': 'Invalid email or password. Please sign up if you dont have an account.'
        }))
        response.status_code = 401
    
    return response

@students.route('/get_student_profile/<nuid>', methods=['GET'])
def get_student(nuid):
    query = f'''
    SELECT 
    s.*,
    i.ImageID,
    i.ImageLink,
    GROUP_CONCAT(ins.InterestName SEPARATOR ', ') AS Interests
    FROM 
        Students s
    JOIN 
        Images i ON s.ProfileIMG = i.ImageID
    LEFT JOIN 
        Interested ind ON ind.NUID = s.NUID
    LEFT JOIN 
        Interests ins ON ins.InterestID = ind.InterestID
    WHERE 
        s.NUID = {nuid}
    GROUP BY 
        s.NUID;'''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    the_data = cursor.fetchall()
    
    response = make_response(jsonify(the_data))

    response.status_code = 200
    
    return response

@students.route('/open_apps', methods=['GET'])
def get_open_apps():
    query = '''
    SELECT DISTINCT c.ClubName, a.NAME, a.Description AS ApplicationDescription, a.Deadline, a.ApplyLink
    FROM Applications a
        JOIN Programs p ON a.ProgramId = p.ProgramID
        JOIN Clubs c ON p.ClubID = c.ClubId
        JOIN ApplicationStatus ast ON a.Status = ast.StatusID
    WHERE ast.StatusText = 'Open'
    AND a.Deadline > NOW();'''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    the_data = cursor.fetchall()
    
    response = make_response(jsonify(the_data))

    response.status_code = 200
    
    return response

@students.route('/feedback', methods=['GET'])
def get_feedback():
    query = '''
    SELECT c.ClubName, f.Description, f.Rating
    FROM Feedback f
        JOIN Clubs c ON f.ClubID = c.ClubId;'''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    the_data = cursor.fetchall()
    
    response = make_response(jsonify(the_data))

    response.status_code = 200
    
    return response

@students.route('/followcount/<nuid>', methods=['GET'])
def get_followcount(nuid):
    query = f'''
    SELECT 
        s.NUID,
        s.FirstName,
        s.LastName,
        s.Email,
        COUNT(DISTINCT f1.FollowerID) AS Followers,
        COUNT(DISTINCT f2.FolloweeID) AS Following
    FROM    
        Students s
    LEFT JOIN 
        Follows f1 ON s.NUID = f1.FolloweeID
    LEFT JOIN 
        Follows f2 ON s.NUID = f2.FollowerID
    WHERE s.NUID = {nuid}
    GROUP BY 
        s.NUID, s.FirstName, s.LastName, s.Email
    ORDER BY 
        s.LastName, s.FirstName;
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    the_data = cursor.fetchall()
    
    response = make_response(jsonify(the_data))

    response.status_code = 200
    
    return response

@students.route('/follows/<nuid>', methods=['GET'])
def get_follows(nuid):

    followers_query = f'''
    SELECT 
        CONCAT(follower.FirstName, ' ', follower.LastName) AS FollowerName
    FROM 
        Follows f
    JOIN 
        Students follower ON f.FollowerID = follower.NUID
    WHERE 
        f.FolloweeID = {nuid}
    '''
    
    following_query = f'''
    SELECT 
        CONCAT(followee.FirstName, ' ', followee.LastName) AS FollowingName
    FROM 
        Follows f
    JOIN 
        Students followee ON f.FolloweeID = followee.NUID
    WHERE 
        f.FollowerID = {nuid}
    '''
    
    cursor = db.get_db().cursor()
    
    cursor.execute(followers_query)
    followers_data = cursor.fetchall()
    
    cursor.execute(following_query)
    following_data = cursor.fetchall()
    
    result = {
        "followers": [follower["FollowerName"] for follower in followers_data],
        "following": [following["FollowingName"] for following in following_data]
    }
    
    response = make_response(jsonify(result))
    response.status_code = 200
    
    return response

@students.route('/browseclubs', methods=['GET'])
def get_clubs():
    query = '''
SELECT 
    c.ClubName, 
    i.ImageLink, 
    c.Description, 
    AVG(f.Rating) AS Rating
    FROM Clubs c
        LEFT JOIN Images i ON c.LogoImg = i.ImageID
        LEFT JOIN Feedback f ON f.ClubID = c.ClubId
GROUP BY c.ClubName, i.ImageLink, c.Description
ORDER BY c.ClubName;
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    the_data = cursor.fetchall()
    
    response = make_response(jsonify(the_data))

    response.status_code = 200
    
    return response
