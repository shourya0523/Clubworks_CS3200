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

@students.route('/feedback/<club_id>', methods=['GET'])
def get_feedback_for_club(club_id):
    query = '''
    SELECT c.ClubName, f.Description, f.Rating
    FROM Feedback f
        JOIN Clubs c ON f.ClubID = c.ClubId
    WHERE c.ClubId = %s;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (club_id,))
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
        AVG(f.Rating) AS Rating,
        -- Use GROUP_CONCAT to aggregate interest names for each club
        GROUP_CONCAT(DISTINCT intr.InterestName SEPARATOR ', ') AS Interests
    FROM
        Clubs c
    LEFT JOIN
        Images i ON c.LogoImg = i.ImageID
    LEFT JOIN
        Feedback f ON f.ClubID = c.ClubId
    -- Join with AppealsTo to link clubs to interests
    LEFT JOIN
        AppealsTo at ON c.ClubId = at.ClubId
    -- Join with Interests to get the interest names
    LEFT JOIN
        Interests intr ON at.InterestID = intr.InterestID
    GROUP BY
        -- Group by all non-aggregated columns to ensure one row per club
        c.ClubId, c.ClubName, c.Description, c.LinkTree, c.CalendarLink, c.Complete, i.ImageLink
    ORDER BY
        c.ClubName
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)

    clubs = cursor.fetchall()
    for club in clubs:
        if club['Interests']:
            club['Interests'] = [interest.strip() for interest in club['Interests'].split(',')]
        else:
            club['Interests'] = []
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

# New route to get feedback for a specific club
@students.route('/feedback/<club_id>', methods=['GET'])
def get_club_feedback(club_id):
    """Fetches anonymous feedback (rating and description) for a given club ID."""
    query = '''
    SELECT
        Rating,
        Description
    FROM
        Feedback
    WHERE
        ClubID = %s
    ORDER BY
        FeedbackId DESC; -- Show newest feedback first, or ORDER BY Rating DESC
    '''
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (club_id,))
        feedback_data = cursor.fetchall()

        if feedback_data is None:
             feedback_data = []

        response = make_response(jsonify(feedback_data))
        response.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error fetching feedback for ClubID {club_id}: {e}")
        response = make_response(jsonify({"status": "error", "message": "Failed to fetch feedback"}))
        response.status_code = 500
    finally:
        if cursor:
            cursor.close()


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

@students.route('/recommendations/<nuid>', methods=['GET'])
def get_recommendations(nuid):
    """Fetches recommended clubs/events based on interests, including interest names."""
    cursor = None
    try:
        cursor = db.get_db().cursor()

        # 1. Get student's interest IDs and Names
        interest_query = '''
        SELECT i.InterestID, i.InterestName
        FROM Interested it
        JOIN Interests i ON it.InterestID = i.InterestID
        WHERE it.NUID = %s;
        '''
        cursor.execute(interest_query, (nuid,))
        student_interests_result = cursor.fetchall()
        student_interest_ids = {row['InterestID'] for row in student_interests_result}
        student_interest_names = {row['InterestName'] for row in student_interests_result} # Use set for uniqueness

        # Prepare default empty response structure
        response_data = {
            "student_interest_names": list(student_interest_names),
            "recommended_clubs": [],
            "recommended_events": []
        }

        if not student_interest_ids:
            # Return early if the student has no interests specified
            return make_response(jsonify(response_data), 200)

        # 2. Get all Interest ID -> Name mappings (needed later)
        all_interests_query = 'SELECT InterestID, InterestName FROM Interests'
        cursor.execute(all_interests_query)
        interest_map = {row['InterestID']: row['InterestName'] for row in cursor.fetchall()}

        # 3. Get all clubs with their associated interest IDs and details
        clubs_query = '''
        SELECT
            c.ClubId, c.ClubName, c.Description, c.LinkTree, c.CalendarLink, c.Complete,
            i.ImageLink as LogoLink, AVG(f.Rating) AS Rating,
            GROUP_CONCAT(DISTINCT at.InterestID SEPARATOR ',') AS InterestIDs
        FROM Clubs c
        LEFT JOIN Images i ON c.LogoImg = i.ImageID
        LEFT JOIN Feedback f ON f.ClubID = c.ClubId
        LEFT JOIN AppealsTo at ON c.ClubId = at.ClubId
        WHERE at.InterestID IS NOT NULL  -- Ensure club has at least one interest
        GROUP BY c.ClubId, c.ClubName, c.Description, c.LinkTree, c.CalendarLink, c.Complete, i.ImageLink
        HAVING InterestIDs IS NOT NULL;
        '''
        cursor.execute(clubs_query)
        all_clubs = cursor.fetchall()

        # 4. Filter clubs based on matching interests and add interest names
        recommended_clubs = []
        recommended_club_ids = set()
        for club in all_clubs:
            club_interest_ids_str = club.pop('InterestIDs', '') # Get IDs and remove from dict
            if club_interest_ids_str:
                club_interest_ids = set(map(int, club_interest_ids_str.split(',')))
                if student_interest_ids.intersection(club_interest_ids):
                    club_interest_names = {interest_map[id] for id in club_interest_ids if id in interest_map}
                    club['interest_names'] = list(club_interest_names) # Add names list

                    if club.get('Rating') is not None:
                        club['Rating'] = float(club['Rating'])

                    recommended_clubs.append(club)
                    recommended_club_ids.add(club['ClubId'])

        response_data["recommended_clubs"] = recommended_clubs

        # 5. Get upcoming events hosted by the recommended clubs (if any)
        if recommended_club_ids:
            events_query = '''
            SELECT
                e.EventID, e.Name, e.Description, e.Location, e.StartTime, e.EndTime,
                c.ClubId, c.ClubName, i.ImageLink as PosterLink, et.EventType
            FROM Events e
            JOIN Clubs c ON e.ClubId = c.ClubId
            LEFT JOIN Images i ON e.PosterImg = i.ImageID
            LEFT JOIN EventTypes et ON e.Type = et.EventTypeId
            WHERE e.StartTime > NOW() AND e.ClubId IN %s
            ORDER BY e.StartTime ASC;
            '''
            club_ids_tuple = tuple(recommended_club_ids)
            cursor.execute(events_query, (club_ids_tuple,))
            response_data["recommended_events"] = cursor.fetchall() # Update response

        response = make_response(jsonify(response_data))
        response.status_code = 200

    except Exception as e:
        current_app.logger.error(f"Error fetching recommendations for NUID {nuid}: {e}")
        response = make_response(jsonify({"status": "error", "message": "Failed to fetch recommendations"}))
        response.status_code = 500
    finally:
        if cursor:
            cursor.close()

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
    try:
        cursor.execute(query) 
        applications = cursor.fetchall()
        response = make_response(jsonify(applications))
        response.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error fetching student applications for NUID {nuid}: {e}")
        response = make_response(jsonify({"status": "error", "message": "Failed to fetch applications"}))
        response.status_code = 500
    return response

@students.route('/all_students/<nuid>', methods=['GET'])
def get_all_other_students(nuid):
    """Fetches all students except the logged-in user."""
    query = '''
    SELECT
        NUID,
        FirstName,
        LastName,
        Email -- Consider if email should be exposed here
    FROM
        Students
    WHERE NUID != %s -- Parameterized placeholder
    ORDER BY
        LastName, FirstName;
    '''
    cursor = db.get_db().cursor()
    try:
        cursor.execute(query, (nuid,)) # Pass nuid as parameter tuple
        students_data = cursor.fetchall()
        response = make_response(jsonify(students_data))
        response.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error fetching all students (excluding {nuid}): {e}")
        response = make_response(jsonify({"status": "error", "message": "Failed to fetch students"}))
        response.status_code = 500
    finally:
        if cursor:
            cursor.close()

    return response

@students.route('/follow', methods=['POST'])
def follow_student():
    """Allows a student to follow another student."""
    data = request.get_json()
    follower_nuid = data.get('follower_nuid')
    followee_nuid = data.get('followee_nuid')

    if not follower_nuid or not followee_nuid:
        return make_response(jsonify({"status": "error", "message": "Follower and Followee NUIDs are required"}), 400)

    if follower_nuid == followee_nuid:
         return make_response(jsonify({"status": "error", "message": "Cannot follow yourself"}), 400)

    db_conn = db.get_db()
    cursor = db_conn.cursor()

    try:
        check_query = "SELECT * FROM Follows WHERE FollowerID = %s AND FolloweeID = %s"
        cursor.execute(check_query, (follower_nuid, followee_nuid))
        existing = cursor.fetchone()

        if existing:
            response = make_response(jsonify({"status": "info", "message": "Already following this student"}))
            response.status_code = 200
            return response

        insert_query = "INSERT INTO Follows (FollowerID, FolloweeID) VALUES (%s, %s)"
        cursor.execute(insert_query, (follower_nuid, followee_nuid))
        db_conn.commit()

        response = make_response(jsonify({"status": "success", "message": "Successfully followed student"}))
        response.status_code = 201
    except Exception as e:
        db_conn.rollback()
        current_app.logger.error(f"Error in /follow route ({follower_nuid} -> {followee_nuid}): {e}")
        response = make_response(jsonify({"status": "error", "message": "Failed to follow student due to server error"}))
        response.status_code = 500
    finally:
        if cursor:
            cursor.close()

    return response

@students.route('/personal_network/<nuid>', methods=['GET'])
def get_personal_network(nuid):
    """
    Returns a network of the student, clubs they belong to, and other students who share those clubs (2 degrees).
    """
    cursor = db.get_db().cursor()

    clubs_query = '''
        SELECT c.ClubId, c.ClubName
        FROM Membership m
        JOIN Clubs c ON m.ClubID = c.ClubId
        WHERE m.NUID = %s
    '''
    cursor.execute(clubs_query, (nuid,))
    clubs = cursor.fetchall()
    club_ids = [club['ClubId'] for club in clubs]

    if club_ids:
        format_strings = ','.join(['%s'] * len(club_ids))
        students_query = f'''
            SELECT DISTINCT s.NUID, s.FirstName, s.LastName, m.ClubID
            FROM Membership m
            JOIN Students s ON m.NUID = s.NUID
            WHERE m.ClubID IN ({format_strings}) AND s.NUID != %s
        '''
        cursor.execute(students_query, (*club_ids, nuid))
        students = cursor.fetchall()
    else:
        students = []

    nodes = []
    edges = []

    cursor.execute('SELECT FirstName, LastName FROM Students WHERE NUID = %s', (nuid,))
    self_info = cursor.fetchone()
    self_label = f"{self_info['FirstName']} {self_info['LastName']} (You)"
    nodes.append({"id": nuid, "label": self_label, "type": "student"})

    for club in clubs:
        nodes.append({"id": f"club_{club['ClubId']}", "label": club['ClubName'], "type": "club"})
        edges.append({"source": nuid, "target": f"club_{club['ClubId']}", "type": "membership"})

    added_students = set()
    for student in students:
        student_id = student['NUID']
        if student_id not in added_students:
            nodes.append({"id": student_id, "label": f"{student['FirstName']} {student['LastName']}", "type": "student"})
            added_students.add(student_id)
        edges.append({"source": student_id, "target": f"club_{student['ClubID']}", "type": "membership"})

    response = make_response(jsonify({"nodes": nodes, "edges": edges}))
    response.status_code = 200
    return response

@students.route('/attendance/<nuid>', methods=['GET'])
def get_student_attendance(nuid):
    """
    Returns all events attended by the student, including event name, club name, and start time.
    """
    query = '''
    SELECT 
        e.Name,
        e.StartTime,
        c.ClubName
    FROM Attendance a
    JOIN Events e ON a.EventID = e.EventID
    JOIN Clubs c ON e.ClubId = c.ClubId
    WHERE a.NUID = %s
    ORDER BY e.StartTime DESC
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (nuid,))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

@students.route('/club_interests/<clubid>', methods=['GET'])
def get_club_interests(clubid):
    """
    Returns a comma-separated string of interest names for the given club.
    """
    query = '''
    SELECT GROUP_CONCAT(i.InterestName SEPARATOR ', ') AS Interests
    FROM AppealsTo a
    JOIN Interests i ON a.InterestID = i.InterestID
    WHERE a.ClubId = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (clubid,))
    data = cursor.fetchone()
    if data and data['Interests']:
        return jsonify({'Interests': data['Interests']})
    else:
        return jsonify({'Interests': ''})