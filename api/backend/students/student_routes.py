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
    SELECT DISTINCT c.ClubName,
                    a.NAME,
                    a.Description AS ApplicationDescription,
                    a.Deadline,
                    a.ApplyLink,
                    ast.StatusText AS Status
    FROM Applications a
        JOIN Programs p ON a.ProgramId = p.ProgramID
        JOIN Clubs c ON p.ClubID = c.ClubId
        JOIN ApplicationStatus ast ON a.Status = ast.StatusID
    WHERE a.Deadline > NOW();'''
        
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

@students.route('/clubs', methods=['GET'])
def get_all_clubs():
    query = '''
    SELECT 
        c.ClubId,
        c.ClubName, 
        c.Description,
        c.LinkTree,
        c.CalendarLink,
        c.Complete,
        i.ImageLink as LogoLink,
        AVG(f.Rating) AS Rating
    FROM 
        Clubs c
    LEFT JOIN 
        Images i ON c.LogoImg = i.ImageID
    LEFT JOIN 
        Feedback f ON f.ClubID = c.ClubId
    GROUP BY 
        c.ClubId, c.ClubName, c.Description, c.LinkTree, c.CalendarLink, c.Complete, i.ImageLink
    ORDER BY 
        c.ClubName
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    clubs = cursor.fetchall()
    
    response = make_response(jsonify(clubs))
    response.status_code = 200
    
    return response

@students.route('/programs', methods=['GET'])
def get_all_programs():
    query = '''
    SELECT 
        p.ProgramID,
        p.ProgramName,
        p.ProgramDescription,
        p.InfoLink,
        c.ClubId,
        c.ClubName
    FROM 
        Programs p
    JOIN 
        Clubs c ON p.ClubID = c.ClubId
    ORDER BY 
        p.ProgramName
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    programs = cursor.fetchall()
    
    response = make_response(jsonify(programs))
    response.status_code = 200
    
    return response

@students.route('/program_applications/<program_id>', methods=['GET'])
def get_program_applications(program_id):
    query = f'''
    SELECT 
        a.ApplicationID,
        a.NAME,
        a.Description,
        a.Deadline,
        a.ApplyLink,
        ast.StatusText AS Status
    FROM 
        Applications a
    LEFT JOIN 
        ApplicationStatus ast ON a.Status = ast.StatusID
    WHERE 
        a.ProgramId = {program_id}
        AND a.Deadline > NOW()
    ORDER BY 
        a.Deadline ASC
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    applications = cursor.fetchall()
    
    response = make_response(jsonify(applications))
    response.status_code = 200
    
    return response

@students.route('/events', methods=['GET'])
def get_all_events():
    query = '''
    SELECT 
        e.EventID,
        e.Name,
        e.Description,
        e.Location,
        e.StartTime,
        e.EndTime,
        c.ClubId,
        c.ClubName,
        i.ImageLink as PosterLink,
        et.EventType
    FROM 
        Events e
    JOIN 
        Clubs c ON e.ClubId = c.ClubId
    LEFT JOIN 
        Images i ON e.PosterImg = i.ImageID
    LEFT JOIN 
        EventTypes et ON e.Type = et.EventTypeId
    ORDER BY 
        e.StartTime ASC
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    events = cursor.fetchall()
    
    response = make_response(jsonify(events))
    response.status_code = 200
    
    return response

@students.route('/attend_event', methods=['POST'])
def attend_event():
    data = request.get_json()
    
    nuid = data['nuid']
    event_id = data['event_id']
    
    check_query = '''
    SELECT * FROM Attendance
    WHERE NUID = %s AND EventID = %s
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(check_query, (nuid, event_id))
    existing = cursor.fetchone()
    
    if existing:
        response = make_response(jsonify({
            'status': 'info',
            'message': 'You have already RSVP\'d to this event'
        }))
        response.status_code = 200
        return response
    
    insert_query = '''
    INSERT INTO Attendance (NUID, EventID)
    VALUES (%s, %s)
    '''
    
    cursor.execute(insert_query, (nuid, event_id))
    db.get_db().commit()
    
    response = make_response(jsonify({
        'status': 'success',
        'message': 'Successfully RSVP\'d to event'
    }))
    response.status_code = 201
    return response

@students.route('/interests', methods=['GET'])
def get_all_interests():
    query = '''
    SELECT 
        InterestID,
        InterestName
    FROM 
        Interests
    ORDER BY 
        InterestName
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    interests = cursor.fetchall()
    
    response = make_response(jsonify(interests))
    response.status_code = 200
    
    return response

@students.route('/student_interests/<nuid>', methods=['GET'])
def get_student_interests(nuid):
    query = f'''
    SELECT 
        i.InterestID,
        i.InterestName
    FROM 
        Interested ind
    JOIN 
        Interests i ON ind.InterestID = i.InterestID
    WHERE 
        ind.NUID = {nuid}
    ORDER BY 
        i.InterestName
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    data = cursor.fetchall()
    
    response = make_response(jsonify(data))
    response.status_code = 200
    
    return response

@students.route('/recommended_clubs/<nuid>', methods=['GET'])
def get_recommended_clubs(nuid):
    query = f'''
    SELECT DISTINCT
        c.ClubId,
        c.ClubName,
        c.Description,
        img.ImageLink as LogoLink
    FROM 
        Clubs c
    JOIN 
        AppealsTo at ON c.ClubId = at.ClubId
    JOIN 
        Interested intr ON at.InterestID = intr.InterestID
    LEFT JOIN 
        Images img ON c.LogoImg = img.ImageID
    WHERE 
        intr.NUID = {nuid}
    ORDER BY 
        c.ClubName
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    clubs = cursor.fetchall()
    
    response = make_response(jsonify(clubs))
    response.status_code = 200
    
    return response

@students.route('/memberships/<nuid>', methods=['GET'])
def get_memberships(nuid):
    query = f'''
    SELECT c.ClubId, c.ClubName, c.Description, c.LinkTree, c.CalendarLink, 
           i.ImageLink as LogoLink,
           e.Position
    FROM Clubs c
    JOIN Membership m ON c.ClubId = m.ClubId
    LEFT JOIN Images i ON c.LogoImg = i.ImageID
    LEFT JOIN Executives e ON (m.NUID = e.NUID AND m.ClubId = e.ClubId)
    WHERE m.NUID = {nuid}
    ORDER BY c.ClubName
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    the_data = cursor.fetchall()
    
    response = make_response(jsonify(the_data))
    response.status_code = 200
    
    return response

@students.route('/upcoming_events/<nuid>', methods=['GET'])
def get_upcoming_events(nuid):
    query = f'''
    SELECT e.EventID, e.Name, e.Description, e.Location, e.StartTime, e.EndTime,
           c.ClubId, c.ClubName, 
           i.ImageLink as PosterLink,
           et.EventType
    FROM Events e
    JOIN Clubs c ON e.ClubId = c.ClubId
    JOIN Attendance a ON e.EventID = a.EventID
    LEFT JOIN Images i ON e.PosterImg = i.ImageID
    LEFT JOIN EventTypes et ON e.Type = et.EventTypeId
    WHERE a.NUID = {nuid}
    ORDER BY e.StartTime ASC
    '''
        
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    the_data = cursor.fetchall()
    
    response = make_response(jsonify(the_data))
    response.status_code = 200
    
    return response

@students.route('/apply_to_app', methods=['POST'])
def apply_to_app():
    data = request.get_json()
    
    nuid = data['nuid']
    application_name = data['application_name']
    
    app_query = '''
    SELECT ApplicationID
    FROM Applications
    WHERE NAME = %s
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(app_query, (application_name,))
    app_result = cursor.fetchone()
    
    if not app_result:
        response = make_response(jsonify({
            'status': 'error',
            'message': 'Application not found'
        }))
        response.status_code = 404
        return response
    
    application_id = app_result['ApplicationID']
    
    check_query = '''
    SELECT * FROM StudentApplication
    WHERE NUID = %s AND ApplicationID = %s
    '''
    
    cursor.execute(check_query, (nuid, application_id))
    existing = cursor.fetchone()
    
    if existing:
        response = make_response(jsonify({
            'status': 'info',
            'message': 'You have already applied to this program'
        }))
        response.status_code = 200
        return response
    
    insert_query = '''
    INSERT INTO StudentApplication (NUID, ApplicationID)
    VALUES (%s, %s)
    '''
    

    cursor.execute(insert_query, (nuid, application_id))
    db.get_db().commit()
    
    response = make_response(jsonify({
        'status': 'success',
        'message': 'Successfully applied to program'
    }))
    response.status_code = 201
    return response

@students.route('/applications/<nuid>', methods=['GET'])
def get_student_applications(nuid):
    query = f'''
    SELECT 
        a.ApplicationID,
        a.NAME as application_name,
        a.Description as application_description,
        a.Deadline,
        a.ApplyLink,
        c.ClubName as club_name,
        ast.StatusText as status
    FROM 
        StudentApplication sa
    JOIN 
        Applications a ON sa.ApplicationID = a.ApplicationID
    JOIN 
        Programs p ON a.ProgramId = p.ProgramID
    JOIN 
        Clubs c ON p.ClubID = c.ClubId
    LEFT JOIN 
        ApplicationStatus ast ON a.Status = ast.StatusID
    WHERE 
        sa.NUID = {nuid}
    ORDER BY 
        a.Deadline ASC
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    applications = cursor.fetchall()
    
    response = make_response(jsonify(applications))
    response.status_code = 200
    
    return response
