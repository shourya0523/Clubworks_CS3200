-- Drop and recreate database
DROP DATABASE IF EXISTS ClubWorks;
CREATE DATABASE IF NOT EXISTS ClubWorks;
USE ClubWorks;

-- Create Images table
CREATE TABLE IF NOT EXISTS Images (
    ImageID INT AUTO_INCREMENT NOT NULL,
    ImageLink TINYTEXT,
    PRIMARY KEY (ImageID)
);

-- Create Students table
CREATE TABLE IF NOT EXISTS Students (
    NUID CHAR(9) NOT NULL,
    FirstName VARCHAR(40) NOT NULL,
    LastName VARCHAR(40) NOT NULL,
    GradDate DATE NOT NULL,
    Active BOOL DEFAULT TRUE,
    Email VARCHAR(40) NOT NULL UNIQUE,
    Major TINYTEXT,
    AboutMe TEXT,
    JoinDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Password VARCHAR(128) NOT NULL,
    ProfileIMG INT,
    PRIMARY KEY (NUID),
    CONSTRAINT fk_imageid
        FOREIGN KEY (ProfileIMG) REFERENCES Images(ImageID) ON DELETE CASCADE,
    Complete BOOLEAN AS (AboutMe IS NOT NULL AND Major IS NOT NULL) STORED -- Chatgpt Helped
);

-- Create Follows table
CREATE TABLE IF NOT EXISTS Follows(
    FollowerID char(9) NOT NULL,
    FolloweeID char(9) NOT NULL,
    CONSTRAINT fk_follows_follower
        FOREIGN KEY (FollowerID) REFERENCES Students(NUID) ON DELETE CASCADE,
    CONSTRAINT fk_follows_followee
        FOREIGN KEY (FolloweeID) REFERENCES Students(NUID) ON DELETE CASCADE
);

-- Create Clubs table
CREATE TABLE IF NOT EXISTS Clubs (
    ClubId INT AUTO_INCREMENT NOT NULL,
    ClubName VARCHAR(40) NOT NULL UNIQUE,
    Description TEXT,
    LinkTree TEXT,
    CalendarLink TEXT,
    LogoImg INT,
    PRIMARY KEY (ClubId),
    CONSTRAINT fk_clubs_logo
        FOREIGN KEY (LogoImg) REFERENCES Images(ImageID) ON DELETE SET NULL,
    Complete BOOLEAN AS (Description IS NOT NULL OR LinkTree IS NOT NULL OR CalendarLink IS NOT NULL) STORED
);

-- Create Programs table
CREATE TABLE IF NOT EXISTS Programs (
    ProgramID INT AUTO_INCREMENT,
    ClubID INT NOT NULL,
    ProgramName VARCHAR(40) NOT NULL UNIQUE,
    ProgramDescription TEXT NOT NULL,
    InfoLink TINYTEXT NOT NULL,
    PRIMARY KEY (ProgramID),
    CONSTRAINT fk_programs_club
        FOREIGN KEY (ClubID) REFERENCES Clubs(ClubId) ON DELETE CASCADE
);

-- Create Participates table
CREATE TABLE IF NOT EXISTS Participates (
    NUID CHAR(9),
    ProgramID INT,
    PRIMARY KEY (NUID, ProgramID),
    CONSTRAINT fk_participates_student
        FOREIGN KEY (NUID) REFERENCES Students(NUID) ON DELETE CASCADE,
    CONSTRAINT fk_participates_program
        FOREIGN KEY (ProgramID) REFERENCES Programs(ProgramID) ON DELETE CASCADE
);

-- Create ApplicationStatus table
CREATE TABLE IF NOT EXISTS ApplicationStatus (
    StatusID INT AUTO_INCREMENT NOT NULL,
    StatusText varchar(40) NOT NULL,
    PRIMARY KEY (StatusID)
);

-- Create Applications table
CREATE TABLE IF NOT EXISTS Applications (
    ApplicationID INT AUTO_INCREMENT NOT NULL,
    NAME TINYTEXT NOT NULL,
    ProgramId INT NOT NULL,
    Description TEXT,
    Deadline DATETIME NOT NULL,
    ApplyLink TINYTEXT NOT NULL,
    PostedDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Status INT NOT NULL DEFAULT 1,
    PRIMARY KEY (ApplicationID),
    CONSTRAINT fk_clubid
        FOREIGN KEY (ProgramId) REFERENCES Programs(ProgramId) ON DELETE CASCADE,
    CONSTRAINT fk_applystatus
        FOREIGN KEY (Status) REFERENCES ApplicationStatus(StatusID)
);

-- Create StudentApplication table
CREATE TABLE IF NOT EXISTS StudentApplication (
    NUID CHAR(9) NOT NULL,
    ApplicationID INT NOT NULL,
    PRIMARY KEY (NUID, ApplicationID),
    CONSTRAINT fk_studentapplication_student
        FOREIGN KEY (NUID) REFERENCES Students(NUID) ON DELETE CASCADE,
    CONSTRAINT fk_studentapplication_application
        FOREIGN KEY (ApplicationID) REFERENCES Applications(ApplicationID) ON DELETE CASCADE
);

-- Create Feedback table
CREATE TABLE IF NOT EXISTS Feedback (
    FeedbackId INT AUTO_INCREMENT NOT NULL,
    Description TINYTEXT,
    Rating TINYINT UNSIGNED NOT NULL,
    NUID CHAR(9),
    ClubID INT,
    PRIMARY KEY (FeedbackId),
    CONSTRAINT fk_feedback_student
        FOREIGN KEY (NUID) REFERENCES Students(NUID) ON DELETE CASCADE,
    CONSTRAINT fk_feedback_club
        FOREIGN KEY (ClubID) REFERENCES Clubs(ClubId) ON DELETE CASCADE
);
-- Create EventTypes Table
CREATE TABLE IF NOT EXISTS EventTypes
(
    EventTypeId INT AUTO_INCREMENT NOT NULL,
    EventType   varchar(40) UNIQUE NOT NULL,
    PRIMARY KEY (EventTypeId)
);

-- Create Events table
CREATE TABLE IF NOT EXISTS Events (
    EventID INT AUTO_INCREMENT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Description TEXT,
    StartTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    EndTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ClubId INT NOT NULL,
    PosterImg INT,
    Type INT NOT NULL,
    PRIMARY KEY (EventID),
    CONSTRAINT fk_events_club
        FOREIGN KEY (ClubId) REFERENCES Clubs(ClubId) ON DELETE CASCADE,
    CONSTRAINT fk_events_poster
        FOREIGN KEY (PosterImg) REFERENCES Images(ImageID) ON DELETE CASCADE,
    CONSTRAINT fk_events_type
        FOREIGN KEY (Type) REFERENCES EventTypes(EventTypeId) ON DELETE CASCADE
);

-- Create Attendance table
CREATE TABLE IF NOT EXISTS Attendance (
    NUID CHAR(9) NOT NULL,
    EventID INT NOT NULL,
    PRIMARY KEY (NUID, EventID),
    CONSTRAINT fk_attendance_student
        FOREIGN KEY (NUID) REFERENCES Students(NUID) ON DELETE CASCADE,
    CONSTRAINT fk_attendance_events
        FOREIGN KEY (EventID) REFERENCES Events(EventID) ON DELETE CASCADE
);

-- Create Interests table
CREATE TABLE IF NOT EXISTS Interests (
    InterestID INT AUTO_INCREMENT NOT NULL,
    InterestName VARCHAR(40) UNIQUE NOT NULL,
    PRIMARY KEY (InterestID)
);

-- Create Interested table
CREATE TABLE IF NOT EXISTS Interested (
    NUID CHAR(9) NOT NULL,
    InterestID INT NOT NULL,
    PRIMARY KEY (NUID, InterestID),
    CONSTRAINT fk_interested_student
        FOREIGN KEY (NUID) REFERENCES Students(NUID) ON DELETE CASCADE,
    CONSTRAINT fk_interested_interest
        FOREIGN KEY (InterestID) REFERENCES Interests(InterestID) ON DELETE CASCADE
);

-- Create Executives table
CREATE TABLE IF NOT EXISTS Executives (
    Position VARCHAR(50) NOT NULL,
    NUID CHAR(9) NOT NULL,
    ClubID INT NOT NULL,
    PRIMARY KEY (NUID, ClubID, Position),
    CONSTRAINT fk_executives_student
        FOREIGN KEY (NUID) REFERENCES Students(NUID) ON DELETE CASCADE,
    CONSTRAINT fk_executives_club
        FOREIGN KEY (ClubID) REFERENCES Clubs(ClubId) ON DELETE CASCADE
);

-- Create AppealsTo table
CREATE TABLE IF NOT EXISTS AppealsTo (
    InterestID INT NOT NULL,
    ClubId INT NOT NULL,
    PRIMARY KEY (InterestID, ClubId),
    CONSTRAINT fk_appeals_interest
        FOREIGN KEY (InterestID) REFERENCES Interests(InterestID) ON DELETE CASCADE,
    CONSTRAINT fk_appeals_club
        FOREIGN KEY (ClubId) REFERENCES Clubs(ClubId) ON DELETE CASCADE
);

-- Create Analysts table
CREATE TABLE IF NOT EXISTS Analysts (
    AnalystID INT AUTO_INCREMENT NOT NULL,
    AnalystName VARCHAR(40) NOT NULL,
    Password VARCHAR(128) NOT NULL,
    Email VARCHAR(75) UNIQUE NOT NULL,
    PRIMARY KEY (AnalystID)
);

-- Create Membership table
CREATE TABLE IF NOT EXISTS Membership (
    NUID CHAR(9) NOT NULL,
    ClubID INT NOT NULL,
    PRIMARY KEY (NUID, ClubID),
    CONSTRAINT fk_membership_student
        FOREIGN KEY (NUID) REFERENCES Students(NUID) ON DELETE CASCADE,
    CONSTRAINT fk_membership_club
        FOREIGN KEY (ClubID) REFERENCES Clubs(ClubId) ON DELETE CASCADE
);
-- Create RequestTypes table
CREATE TABLE IF NOT EXISTS RequestTypes
(
    RequestTypeId INT AUTO_INCREMENT NOT NULL,
    RequestType   varchar(40) UNIQUE NOT NULL,
    PRIMARY KEY (RequestTypeId)
);

-- Create Requests table
CREATE TABLE IF NOT EXISTS Requests (
    RequestID INT AUTO_INCREMENT NOT NULL,
    RequestDescription TEXT NOT NULL,
    Status BOOL,
    CreatedTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Type INT NOT NULL,
    ExecutiveID char(9) NOT NULL,
    ExecutiveClub INT NOT NULL,
    ExecutivePosition VARCHAR(50) NOT NULL,
    PRIMARY KEY (RequestID),
    CONSTRAINT fk_requests_executive
        FOREIGN KEY (ExecutiveID, ExecutiveClub, ExecutivePosition) REFERENCES Executives(NUID, ClubID, Position),
    CONSTRAINT fk_requests_type
        FOREIGN KEY (Type) REFERENCES RequestTypes(RequestTypeId)
);

-- Create RequestReviews table
CREATE TABLE IF NOT EXISTS RequestReviews (
    RequestID INT NOT NULL,
    AnalystID INT NOT NULL,
    PRIMARY KEY (RequestID, AnalystID),
    CONSTRAINT fk_reviews_request
        FOREIGN KEY (RequestID) REFERENCES Requests(RequestID) ON DELETE CASCADE,
    CONSTRAINT fk_reviews_analyst
        FOREIGN KEY (AnalystID) REFERENCES Analysts(AnalystID) ON DELETE CASCADE
);

-- Create AdminTypes table
CREATE TABLE IF NOT EXISTS AdminTypes
(
    AdminTypeId INT AUTO_INCREMENT NOT NULL,
    AdminType   varchar(40) UNIQUE NOT NULL,
    PRIMARY KEY (AdminTypeId)
);
-- Create SupportTypes table
CREATE TABLE IF NOT EXISTS SupportTypes
(
    SupportTypeId INT AUTO_INCREMENT NOT NULL,
    SupportType   varchar(40) UNIQUE NOT NULL,
    PRIMARY KEY (SupportTypeId)
);

-- Create SupportRequests table
CREATE TABLE IF NOT EXISTS SupportRequests
(
    SupportRequestID          INT AUTO_INCREMENT NOT NULL,
    SupportRequestType        INT                NOT NULL,
    SupportRequestDescription TINYTEXT,
    StudentID                 char(9) NOT NULL,
    PRIMARY KEY (SupportRequestID),
    CONSTRAINT fk_student
        FOREIGN KEY (StudentID) REFERENCES Students (NUID) ON DELETE CASCADE,
    CONSTRAINT fk_supporttype
        FOREIGN KEY (SupportRequestType) REFERENCES SupportTypes (SupportTypeID)
);
-- Create Admins table
CREATE TABLE IF NOT EXISTS Admins (
    AdminId INT AUTO_INCREMENT NOT NULL,
    UserName varchar(40) UNIQUE NOT NULL,
    Password varchar(128) NOT NULL,
    TypeID INT,
    PRIMARY KEY (AdminId),
    CONSTRAINT fk_type
        FOREIGN KEY (TypeId) REFERENCES AdminTypes(AdminTypeID) ON DELETE CASCADE
);

-- Create SupportAdmins
CREATE TABLE SupportAdmins(
    AdminID INT,
    RequestID INT NOT NULL,
    PRIMARY KEY (AdminId, RequestID),
    CONSTRAINT fk_adminid
        FOREIGN KEY (AdminId) REFERENCES Admins(AdminId),
    CONSTRAINT fk_requestid
        FOREIGN KEY (RequestId) REFERENCES SupportRequests(SupportRequestID) ON DELETE CASCADE
);

USE ClubWorks;

USE ClubWorks;

-- Images table insert with 30 images
INSERT INTO Images (ImageLink) VALUES
('https://example.com/profile_pic1.jpg'),     -- ID 1
('https://example.com/profile_pic2.jpg'),     -- ID 2
('https://example.com/profile_pic3.jpg'),     -- ID 3
('https://example.com/profile_pic4.jpg'),     -- ID 4
('https://example.com/profile_pic5.jpg'),     -- ID 5
('https://example.com/profile_pic6.jpg'),     -- ID 6
('https://example.com/profile_pic7.jpg'),     -- ID 7
('https://example.com/profile_pic8.jpg'),     -- ID 8
('https://example.com/profile_pic9.jpg'),     -- ID 9
('https://example.com/profile_pic10.jpg'),    -- ID 10
('https://example.com/profile_pic11.jpg'),    -- ID 11
('https://example.com/profile_pic12.jpg'),    -- ID 12
('https://example.com/profile_pic13.jpg'),    -- ID 13
('https://example.com/profile_pic14.jpg'),    -- ID 14
('https://example.com/profile_pic15.jpg'),    -- ID 15
('https://example.com/club_logo1.png'),       -- ID 16
('https://example.com/club_logo2.png'),       -- ID 17
('https://example.com/club_logo3.png'),       -- ID 18
('https://example.com/club_logo4.png'),       -- ID 19
('https://example.com/club_logo5.png'),       -- ID 20
('https://example.com/club_logo6.png'),       -- ID 21
('https://example.com/club_logo7.png'),       -- ID 22
('https://example.com/club_logo8.png'),       -- ID 23
('https://example.com/club_logo9.png'),       -- ID 24
('https://example.com/club_logo10.png'),      -- ID 25
('https://example.com/event_poster1.jpg'),    -- ID 26
('https://example.com/event_poster2.jpg'),    -- ID 27
('https://example.com/event_poster3.jpg'),    -- ID 28
('https://example.com/event_poster4.jpg'),    -- ID 29
('https://example.com/event_poster5.jpg');    -- ID 30

-- Insert 35 students with unique NUIDs
INSERT INTO Students (NUID, FirstName, LastName, GradDate, Email, Major, AboutMe, Password, ProfileIMG, JoinDate) VALUES
('100000001', 'Lucas', 'Lane', '2025-05-15', 'lucas.lane@northeastern.edu', 'Computer Science', 'I am a CS student interested in AI.', 'hashedpassword1', 1, '2023-09-01'),
('100000002', 'Jane', 'Smith', '2024-12-20', 'jane.smith@northeastern.edu', 'Business', 'Business major with interest in entrepreneurship.', 'hashedpassword2', 2, '2023-10-01'),
('100000003', 'Tyla', 'Johnson', '2026-05-10', 'tyla.j@northeastern.edu', 'Engineering', 'Mechanical engineering student.', 'hashedpassword3', 3, '2023-11-01'),
('100000004', 'Jack', 'Williams', '2025-05-15', 'jack.w@northeastern.edu', 'Biology', 'Pre-med student.', 'hashedpassword4', 4, '2023-11-15'),
('100000005', 'Mary', 'Brown', '2024-12-20', 'mary.b@northeastern.edu', 'Psychology', 'Interested in clinical psychology.', 'hashedpassword5', 5, '2023-09-10'),
('100000006', 'David', 'Miller', '2026-05-15', 'david.miller@northeastern.edu', 'Data Science', 'Data science enthusiast, love visualization.', 'hashedpassword6', 6, '2024-01-10'),
('100000007', 'Sophia', 'Davis', '2025-12-20', 'sophia.davis@northeastern.edu', 'Marketing', 'Exploring digital marketing strategies.', 'hashedpassword7', 7, '2024-02-15'),
('100000008', 'Ethan', 'Garcia', '2025-08-15', 'ethan.garcia@northeastern.edu', 'Physics', 'Fascinated by quantum mechanics.', 'hashedpassword8', 8, '2024-03-20'),
('100000009', 'Olivia', 'Rodriguez', '2026-12-20', 'olivia.r@northeastern.edu', 'Political Science', 'Interested in international relations.', 'hashedpassword9', 9, '2024-04-25'),
('100000010', 'Noah', 'Wilson', '2025-05-10', 'noah.wilson@northeastern.edu', 'Chemical Engineering', 'Focusing on sustainable energy solutions.', 'hashedpassword10', 10, '2024-05-30'),
('100000011', 'Emma', 'Parker', '2026-05-15', 'e.parker@northeastern.edu', 'Computer Engineering', 'Passionate about robotics and embedded systems.', 'hashedpassword11', 11, '2023-09-05'),
('100000012', 'Mason', 'Thompson', '2025-12-20', 'm.thompson@northeastern.edu', 'Finance', 'Aspiring investment banker with experience in stock trading.', 'hashedpassword12', 12, '2023-10-12'),
('100000013', 'Zoe', 'Bennett', '2027-05-15', 'z.bennett@northeastern.edu', 'International Affairs', 'Interested in diplomatic relations and global policy.', 'hashedpassword13', 13, '2023-11-20'),
('100000014', 'Logan', 'Hayes', '2026-05-15', 'l.hayes@northeastern.edu', 'Mechanical Engineering', 'Car enthusiast working on sustainable vehicle design.', 'hashedpassword14', NULL, '2023-12-01'),
('100000015', 'Harper', 'Sullivan', '2025-12-20', 'h.sullivan@northeastern.edu', 'Bioengineering', 'Researching biomaterials for medical applications.', 'hashedpassword15', 14, '2024-01-15'),
('100000016', 'Caleb', 'Morgan', '2026-05-15', 'c.morgan@northeastern.edu', 'English Literature', 'Writer and poet exploring contemporary American fiction.', 'hashedpassword16', NULL, '2024-02-05'),
('100000017', 'Amelia', 'Reed', '2027-05-15', 'a.reed@northeastern.edu', 'Environmental Science', 'Focused on urban sustainability initiatives.', 'hashedpassword17', 15, '2024-03-10'),
('100000018', 'Elijah', 'Cooper', '2025-12-20', 'e.cooper@northeastern.edu', 'History', 'Specializing in European medieval history.', 'hashedpassword18', NULL, '2024-04-15'),
('100000019', 'Mia', 'Rivera', '2026-05-15', 'm.rivera@northeastern.edu', 'Linguistics', 'Studying language acquisition and bilingual education.', 'hashedpassword19', NULL, '2024-05-20'),
('100000020', 'Carter', 'Patel', '2027-05-15', 'c.patel@northeastern.edu', 'Game Design', 'Creating narrative-driven indie games.', 'hashedpassword20', NULL, '2024-06-25'),
('100000021', 'Layla', 'Kim', '2026-12-20', 'l.kim@northeastern.edu', 'Journalism', 'Aspiring investigative reporter, interned at Boston Globe.', 'hashedpassword21', NULL, '2024-07-01'),
('100000022', 'Owen', 'Nguyen', '2025-05-15', 'o.nguyen@northeastern.edu', 'Architecture', 'Interested in sustainable urban development.', 'hashedpassword22', NULL, '2024-07-15'),
('100000023', 'Aria', 'Gupta', '2026-12-20', 'a.gupta@northeastern.edu', 'Mathematics', 'Researching graph theory applications.', 'hashedpassword23', NULL, '2024-07-20'),
('100000024', 'Miles', 'Walsh', '2025-05-15', 'm.walsh@northeastern.edu', 'Philosophy', 'Exploring ethics in artificial intelligence.', 'hashedpassword24', NULL, '2024-07-25'),
('100000025', 'Scarlett', 'Chen', '2027-12-20', 's.chen@northeastern.edu', 'Music Technology', 'Composer and sound designer.', 'hashedpassword25', NULL, '2024-08-01'),
('100000026', 'Leo', 'Martin', '2026-05-15', 'l.martin@northeastern.edu', 'Biomedical Engineering', 'Developing medical imaging technologies.', 'hashedpassword26', NULL, '2024-08-05'),
('100000027', 'Grace', 'Singh', '2025-12-20', 'g.singh@northeastern.edu', 'Nursing', 'Passionate about pediatric care.', 'hashedpassword27', NULL, '2024-08-10'),
('100000028', 'Henry', 'Jones', '2026-05-15', 'h.jones@northeastern.edu', 'Film Studies', 'Documentarian focusing on social issues.', 'hashedpassword28', NULL, '2024-08-15'),
('100000029', 'Chloe', 'Martinez', '2027-12-20', 'c.martinez@northeastern.edu', 'Behavioral Neuroscience', 'Studying brain development in adolescents.', 'hashedpassword29', NULL, '2023-09-01'),
('100000030', 'Wyatt', 'Lee', '2025-05-15', 'w.lee@northeastern.edu', 'Information Science', 'Focused on data privacy and ethics.', 'hashedpassword30', NULL, '2023-09-10'),
('100000031', 'Isabella', 'Taylor', '2026-12-20', 'i.taylor@northeastern.edu', 'Biochemistry', 'Researching protein folding mechanisms.', 'hashedpassword31', NULL, '2023-09-15'),
('100000032', 'Grayson', 'Ahmed', '2025-05-15', 'g.ahmed@northeastern.edu', 'Industrial Design', 'Creating user-centered sustainable products.', 'hashedpassword32', NULL, '2023-09-20'),
('100000033', 'Lily', 'Garcia', '2027-12-20', 'l.garcia@northeastern.edu', 'Communication Studies', 'Interested in media representation and identity.', 'hashedpassword33', NULL, '2023-09-25'),
('100000034', 'Benjamin', 'Wilson', '2026-05-15', 'b.wilson@northeastern.edu', 'Cybersecurity', 'Ethical hacker and security researcher.', 'hashedpassword34', NULL, '2023-10-01'),
('100000035', 'Aubrey', 'Thompson', '2025-12-20', 'a.thompson@northeastern.edu', 'Marketing', 'Specializing in digital marketing strategies.', 'hashedpassword35', NULL, '2023-10-05');

-- Insert follows relationships
INSERT INTO Follows (FollowerID, FolloweeID) VALUES
-- Students following Lucas Lane (CS Student)
('100000002', '100000001'), -- Jane follows Lucas
('100000003', '100000001'), -- Tyla follows Lucas
('100000004', '100000001'), -- Jack follows Lucas
('100000005', '100000001'), -- Mary follows Lucas
('100000006', '100000001'), -- David follows Lucas
('100000011', '100000001'), -- Emma follows Lucas
('100000026', '100000001'), -- Leo follows Lucas
('100000030', '100000001'), -- Wyatt follows Lucas
('100000034', '100000001'), -- Benjamin follows Lucas

-- Students following Jane Smith (Business Student)
('100000001', '100000002'), -- Lucas follows Jane
('100000007', '100000002'), -- Sophia follows Jane
('100000012', '100000002'), -- Mason follows Jane
('100000035', '100000002'), -- Aubrey follows Jane
('100000028', '100000002'), -- Henry follows Jane

-- Students following Data Science enthusiasts
('100000001', '100000006'), -- Lucas follows David (Data Science)
('100000002', '100000006'), -- Jane follows David
('100000011', '100000006'), -- Emma follows David
('100000030', '100000006'), -- Wyatt follows David
('100000034', '100000006'), -- Benjamin follows David

-- Cross-major connections
('100000003', '100000027'), -- Tyla Johnson (Engineering) follows Grace Singh (Nursing)
('100000027', '100000003'), -- Grace Singh follows Tyla Johnson
('100000016', '100000028'), -- Caleb Morgan (English) follows Henry Jones (Film)
('100000028', '100000016'), -- Henry Jones follows Caleb Morgan
('100000024', '100000032'), -- Miles Walsh (Philosophy) follows Grayson Ahmed (Industrial Design)
('100000032', '100000024'), -- Grayson follows Miles
('100000029', '100000027'), -- Chloe Martinez (Behavioral Neuroscience) follows Grace Singh (Nursing)
('100000013', '100000032'), -- Zoe Bennett (International Affairs) follows Grayson Ahmed
('100000013', '100000011'), -- Zoe Bennett follows Emma Parker (Computer Engineering)

-- Club leadership connections (will match executive assignments later)
('100000017', '100000018'), -- Amelia Reed follows Elijah Cooper
('100000018', '100000017'), -- Elijah Cooper follows Amelia Reed
('100000003', '100000035'), -- Tyla Johnson follows Aubrey Thompson
('100000035', '100000003'), -- Aubrey Thompson follows Tyla Johnson
('100000011', '100000026'), -- Emma Parker follows Leo Martin
('100000026', '100000011'), -- Leo Martin follows Emma Parker
('100000013', '100000012'), -- Zoe Bennett follows Mason Thompson
('100000012', '100000013'), -- Mason Thompson follows Zoe Bennett
('100000027', '100000029'), -- Grace Singh follows Chloe Martinez
('100000029', '100000027'); -- Chloe Martinez follows Grace Singh

-- Insert clubs (10 clubs)
INSERT INTO Clubs (ClubName, Description, LinkTree, CalendarLink, LogoImg) VALUES
('Coding Club', 'A club for coding enthusiasts', 'https://linktr.ee/codingclub', 'https://calendar.google.com/codingclub', 16), -- ID 1
('Business Society', 'For future entrepreneurs', 'https://linktr.ee/businesssociety', 'https://calendar.google.com/businesssociety', 17), -- ID 2
('Engineering Club', 'For engineering students', 'https://linktr.ee/engineeringclub', NULL, 18), -- ID 3
('Sustainable Future Initiative', 'Student organization dedicated to promoting environmental sustainability on campus and beyond.', 'https://linktr.ee/sustainablefuture', 'https://calendar.google.com/sustainablefuture', 21), -- ID 4
('NeU Chess Society', 'A community for chess enthusiasts of all skill levels. Weekly matches and tournaments.', 'https://linktr.ee/neuchess', 'https://calendar.google.com/neuchess', 22), -- ID 5
('Robotics Collective', 'Building robots for competitions and research. Open to all engineering disciplines.', 'https://linktr.ee/roboticscollective', 'https://calendar.google.com/robotics', 23), -- ID 6
('International Students Association', 'Supporting international students and promoting cultural exchange.', 'https://linktr.ee/neuisa', 'https://calendar.google.com/neuisa', 24), -- ID 7
('Healthcare Leadership Forum', 'Preparing students for leadership roles in healthcare through workshops and networking.', 'https://linktr.ee/healthcareleaders', 'https://calendar.google.com/healthcareleaders', 25), -- ID 8
('Creative Writing Workshop', 'For students interested in fiction, poetry, and creative non-fiction.', 'https://linktr.ee/creativewriting', NULL, NULL), -- ID 9
('AI Ethics Coalition', 'Discussing ethical implications of artificial intelligence and machine learning.', NULL, 'https://calendar.google.com/aiethics', NULL); -- ID 10

-- Insert programs (20 programs)
INSERT INTO Programs (ClubID, ProgramName, ProgramDescription, InfoLink) VALUES
(1, 'Hackathon', 'Annual coding competition', 'https://example.com/hackathon'), -- ID 1
(1, 'Code Workshop', 'Weekly coding workshops', 'https://example.com/workshop'), -- ID 2
(2, 'Startup Incubator', 'Program for startup ideas', 'https://example.com/incubator'), -- ID 3
(3, 'Engineering Projects', 'Hands-on engineering projects', 'https://example.com/engprojects'), -- ID 4
(4, 'Campus Recycling Initiative', 'Improving recycling infrastructure on campus.', 'https://example.com/recycling'), -- ID 5
(4, 'Sustainable Food Systems', 'Exploring local food networks and reducing food waste.', 'https://example.com/sustainablefood'), -- ID 6
(5, 'Beginner Chess Training', 'Weekly lessons for novice players.', 'https://example.com/chesstraining'), -- ID 7
(5, 'Tournament Preparation', 'Strategic preparation for competitive players.', 'https://example.com/chesscomp'), -- ID 8
(6, 'Combat Robotics Team', 'Building competitive battle robots.', 'https://example.com/combatrobotics'), -- ID 9
(6, 'Autonomous Systems Group', 'Developing self-navigating robots.', 'https://example.com/autonomous'), -- ID 10
(7, 'Cultural Exchange Program', 'Sharing traditions and building cross-cultural understanding.', 'https://example.com/culturalexchange'), -- ID 11
(7, 'International Career Development', 'Resources for international students seeking jobs.', 'https://example.com/intlcareers'), -- ID 12
(8, 'Healthcare Policy Seminars', 'Understanding healthcare legislation and policy.', 'https://example.com/healthpolicy'), -- ID 13
(8, 'Medical Innovation Lab', 'Exploring emerging technologies in healthcare.', 'https://example.com/medinnovation'), -- ID 14
(9, 'Fiction Workshop', 'Weekly critique sessions for fiction writers.', 'https://example.com/fictionworkshop'), -- ID 15
(9, 'Literary Magazine', 'Student-run publication of creative writing.', 'https://example.com/litmag'), -- ID 16
(10, 'AI Ethics Roundtable', 'Monthly discussions on ethical dilemmas in AI.', 'https://example.com/aiethics'), -- ID 17
(10, 'Algorithmic Bias Research', 'Studying and mitigating bias in algorithms.', 'https://example.com/algobias'), -- ID 18
(1, 'Open Source Contribution', 'Contributing to open source projects', 'https://example.com/opensource'), -- ID 19
(2, 'Case Competition Team', 'Compete in business case competitions', 'https://example.com/casecomp'); -- ID 20

-- Insert program participants
INSERT INTO Participates (NUID, ProgramID) VALUES
-- Coding Club Programs
('100000001', 1), -- Lucas Lane in Hackathon
('100000001', 2), -- Lucas Lane in Code Workshop
('100000006', 1), -- David Miller in Hackathon
('100000006', 2), -- David Miller in Code Workshop
('100000011', 1), -- Emma Parker in Hackathon
('100000034', 19), -- Benjamin Wilson in Open Source

-- Business Society Programs
('100000002', 3), -- Jane Smith in Startup Incubator
('100000007', 3), -- Sophia Davis in Startup Incubator
('100000012', 3), -- Mason Thompson in Startup Incubator
('100000012', 20), -- Mason Thompson in Case Competition
('100000035', 20), -- Aubrey Thompson in Case Competition

-- Engineering Club Programs
('100000003', 4), -- Tyla Johnson in Engineering Projects
('100000010', 4), -- Noah Wilson in Engineering Projects
('100000014', 4), -- Logan Hayes in Engineering Projects

-- Sustainable Future Programs
('100000017', 5), -- Amelia Reed in Campus Recycling
('100000017', 6), -- Amelia Reed in Sustainable Food
('100000010', 5), -- Noah Wilson in Campus Recycling
('100000010', 6), -- Noah Wilson in Sustainable Food

-- Chess Society Programs
('100000003', 7), -- Tyla Johnson in Beginner Chess
('100000018', 7), -- Elijah Cooper in Beginner Chess
('100000001', 8), -- Lucas Lane in Tournament Prep
('100000031', 8), -- Isabella Taylor in Tournament Prep

-- Robotics Programs
('100000014', 9), -- Logan Hayes in Combat Robotics
('100000011', 9), -- Emma Parker in Combat Robotics
('100000026', 9), -- Leo Martin in Combat Robotics
('100000006', 10), -- David Miller in Autonomous Systems
('100000030', 10), -- Wyatt Lee in Autonomous Systems

-- International Students Programs
('100000013', 11), -- Zoe Bennett in Cultural Exchange
('100000012', 12), -- Mason Thompson in International Career
('100000021', 11), -- Layla Kim in Cultural Exchange

-- Healthcare Programs
('100000027', 13), -- Grace Singh in Healthcare Policy
('100000029', 13), -- Chloe Martinez in Healthcare Policy
('100000027', 14), -- Grace Singh in Medical Innovation
('100000026', 14), -- Leo Martin in Medical Innovation

-- Creative Writing Programs
('100000016', 15), -- Caleb Morgan in Fiction Workshop
('100000024', 15), -- Miles Walsh in Fiction Workshop
('100000016', 16), -- Caleb Morgan in Literary Magazine

-- AI Ethics Programs
('100000001', 17), -- Lucas Lane in AI Ethics Roundtable
('100000006', 17), -- David Miller in AI Ethics Roundtable
('100000024', 17), -- Miles Walsh in AI Ethics Roundtable
('100000001', 18), -- Lucas Lane in Algorithmic Bias Research
('100000030', 18); -- Wyatt Lee in Algorithmic Bias Research

-- Insert application status
INSERT INTO ApplicationStatus (StatusText) VALUES
('Open'),       -- ID 1
('Closed'),     -- ID 2
('Under Review'); -- ID 3

-- Insert applications
INSERT INTO Applications (NAME, ProgramId, Description, Deadline, ApplyLink, Status, PostedDate) VALUES
('Fall Hackathon Application', 1, 'Apply for our fall hackathon', '2024-10-15 23:59:59', 'https://example.com/apply/hackathon', 1, '2024-09-01 10:00:00'), -- ID 1
('Workshop Leader Application', 2, 'Apply to lead a workshop', '2024-09-20 23:59:59', 'https://example.com/apply/workshop', 3, '2024-08-15 11:00:00'), -- ID 2
('Startup Funding Application', 3, 'Apply for startup funding', '2025-01-10 23:59:59', 'https://example.com/apply/funding', 1, '2024-11-01 09:00:00'), -- ID 3
('Engineering Project Proposal', 4, 'Submit your project proposal', '2024-11-01 23:59:59', 'https://example.com/apply/project', 2, '2024-09-15 14:00:00'), -- ID 4
('Campus Sustainability Ambassador', 5, 'Lead campus recycling initiatives and educate peers on sustainable practices.', '2025-08-15 23:59:59', 'https://example.com/apply/sustainability', 1, '2024-07-01 09:00:00'), -- ID 5
('Chess Club Instructor', 7, 'Teach beginners the fundamentals of chess in weekly sessions.', '2025-09-01 23:59:59', 'https://example.com/apply/chessinstructor', 1, '2024-08-01 10:00:00'), -- ID 6
('Robotics Competition Team Member', 9, 'Join our team for the national robotics challenge.', '2025-10-30 23:59:59', 'https://example.com/apply/robotics', 1, '2024-09-15 11:00:00'), -- ID 7
('International Student Mentor', 11, 'Help new international students adjust to campus life.', '2025-07-15 23:59:59', 'https://example.com/apply/intlmentor', 2, '2024-06-01 12:00:00'), -- ID 8
('Healthcare Innovation Challenge', 14, 'Develop innovative solutions to current healthcare problems.', '2025-11-01 23:59:59', 'https://example.com/apply/healthinnovation', 1, '2024-09-01 13:00:00'), -- ID 9
('Literary Magazine Editor', 16, 'Help curate and edit our annual literary publication.', '2025-12-01 23:59:59', 'https://example.com/apply/liteditor', 2, '2024-10-01 14:00:00'); -- ID 10

-- Insert student applications
INSERT INTO StudentApplication (NUID, ApplicationID) VALUES
('100000001', 1), -- Lucas Lane applies for Hackathon
('100000006', 1), -- David Miller applies for Hackathon
('100000011', 1), -- Emma Parker applies for Hackathon
('100000001', 2), -- Lucas Lane applies for Workshop Leader
('100000006', 2), -- David Miller applies for Workshop Leader
('100000002', 3), -- Jane Smith applies for Startup Funding
('100000012', 3), -- Mason Thompson applies for Startup Funding
('100000003', 4), -- Tyla Johnson applies for Engineering Project
('100000014', 4), -- Logan Hayes applies for Engineering Project
('100000017', 5), -- Amelia Reed applies for Sustainability Ambassador
('100000010', 5), -- Noah Wilson applies for Sustainability Ambassador
('100000003', 6), -- Tyla Johnson applies for Chess Instructor
('100000018', 6), -- Elijah Cooper applies for Chess Instructor
('100000014', 7), -- Logan Hayes applies for Robotics Competition
('100000011', 7), -- Emma Parker applies for Robotics Competition
('100000026', 7), -- Leo Martin applies for Robotics Competition
('100000013', 8), -- Zoe Bennett applies for International Student Mentor
('100000021', 8), -- Layla Kim applies for International Student Mentor
('100000027', 9), -- Grace Singh applies for Healthcare Innovation Challenge
('100000026', 9), -- Leo Martin applies for Healthcare Innovation Challenge
('100000016', 10); -- Caleb Morgan applies for Literary Magazine Editor

-- Insert feedback
INSERT INTO Feedback (Description, Rating, NUID, ClubID) VALUES
-- Coding Club
('Great resources for learning programming', 5, '100000001', 1), -- Lucas
('Excellent peer learning environment', 5, '100000006', 1), -- David
('Would like more advanced topics', 4, '100000011', 1), -- Emma
('Amazing hackathon experience', 5, '100000034', 1), -- Benjamin

-- Business Society
('Helpful networking opportunities', 5, '100000002', 2), -- Jane
('Great industry connections', 5, '100000012', 2), -- Mason
('Insightful guest speakers', 4, '100000007', 2), -- Sophia
('Case competitions provided real-world experience', 5, '100000035', 2), -- Aubrey

-- Engineering Club
('Hands-on projects are excellent', 5, '100000003', 3), -- Tyla
('Would like more industry partnerships', 4, '100000014', 3), -- Logan
('Great for applying classroom knowledge', 5, '100000010', 3), -- Noah

-- Sustainable Future
('Meaningful impact on campus sustainability', 5, '100000017', 4), -- Amelia
('Well-organized initiatives', 4, '100000010', 4), -- Noah
('Great leadership and community', 5, '100000013', 4), -- Zoe

-- Chess Society
('Welcoming environment for all skill levels', 5, '100000003', 5), -- Tyla
('Well-organized tournaments', 5, '100000018', 5), -- Elijah
('Great teaching methods', 4, '100000001', 5), -- Lucas

-- Robotics Collective
('Excellent equipment and resources', 5, '100000014', 6), -- Logan
('Supportive learning environment', 5, '100000011', 6), -- Emma
('Great preparation for industry', 4, '100000026', 6), -- Leo
('Challenging but rewarding projects', 5, '100000006', 6), -- David

-- International Students Association
('Helped me connect with other international students', 5, '100000013', 7), -- Zoe
('Valuable resources for navigating university life', 5, '100000021', 7), -- Layla
('Welcoming community', 5, '100000012', 7), -- Mason

-- Healthcare Leadership Forum
('Excellent networking opportunities', 5, '100000027', 8), -- Grace
('Insightful discussions on healthcare policy', 4, '100000029', 8), -- Chloe
('Great preparation for healthcare careers', 5, '100000026', 8), -- Leo

-- Creative Writing Workshop
('Constructive feedback environment', 5, '100000016', 9), -- Caleb
('Helped improve my writing significantly', 5, '100000024', 9), -- Miles

-- AI Ethics Coalition
('Thought-provoking discussions', 5, '100000001', 10), -- Lucas
('Great mix of technical and ethical perspectives', 5, '100000006', 10), -- David
('Welcoming to students from different disciplines', 4, '100000024', 10); -- Miles

-- Insert event types
INSERT INTO EventTypes (EventType) VALUES
('Workshop'),       -- ID 1
('Seminar'),        -- ID 2
('Social'),         -- ID 3
('Competition'),    -- ID 4
('Meeting');        -- ID 5

-- Insert events
INSERT INTO Events (Name, Location, Description, StartTime, EndTime, ClubId, PosterImg, Type) VALUES
-- Past Events
('Intro to Python Workshop', 'Room 101', 'Learn Python programming basics', '2024-08-10 14:00:00', '2024-08-10 16:00:00', 1, 26, 1),
('Entrepreneurship Seminar', 'Auditorium', 'Guest speakers discuss startup experiences', '2024-08-15 10:00:00', '2024-08-15 12:00:00', 2, 27, 2),
('Engineering Social', 'Student Center', 'Networking event for engineering students', '2024-08-20 18:00:00', '2024-08-20 20:00:00', 3, NULL, 3),

-- Upcoming Events
('Fall Hackathon', 'Tech Building', '48-hour coding competition', '2024-10-15 09:00:00', '2024-10-17 09:00:00', 1, 28, 4),
('Business Pitch Night', 'Dodge Hall', 'Pitch your business ideas', '2024-10-20 18:00:00', '2024-10-20 21:00:00', 2, 29, 4),
('Sustainable Living Workshop', 'West Village G 108', 'Learn practical tips for reducing your environmental footprint.', '2024-09-30 15:00:00', '2024-09-30 17:00:00', 4, NULL, 1),
('Advanced Chess Tactics', 'Curry Student Center 346', 'Master complex chess strategies with our expert instructors.', '2024-10-05 18:00:00', '2024-10-05 20:00:00', 5, NULL, 1),
('Robotics Programming Workshop', 'Engineering Lab 305', 'Introduction to programming for robotics applications.', '2024-10-22 15:00:00', '2024-10-22 17:30:00', 6, 30, 1),
('International Cultural Festival', 'Curry Student Center Ballroom', 'Celebrating global cultures with food, performances, and exhibits.', '2024-12-05 15:00:00', '2024-12-05 20:00:00', 7, NULL, 3),
('Healthcare Innovation Trends', 'Behrakis Health Sciences Center 410', 'Industry experts discuss emerging healthcare technologies.', '2024-11-05 17:00:00', '2024-11-05 19:00:00', 8, NULL, 2),
('Creative Writing Workshop', 'Ryder Hall 180', 'Essential techniques for fiction writing.', '2024-10-15 16:00:00', '2024-10-15 18:00:00', 9, NULL, 1),
('The Ethics of Generative AI', 'West Village H 366', 'Discussion on ethical implications of AI-generated content.', '2024-11-15 16:00:00', '2024-11-15 18:00:00', 10, NULL, 2);

-- Insert attendance
INSERT INTO Attendance (NUID, EventID) VALUES
-- Past Events
('100000001', 1), -- Lucas attended Python Workshop
('100000006', 1), -- David attended Python Workshop
('100000011', 1), -- Emma attended Python Workshop
('100000034', 1), -- Benjamin attended Python Workshop

('100000002', 2), -- Jane attended Entrepreneurship Seminar
('100000007', 2), -- Sophia attended Entrepreneurship Seminar
('100000012', 2), -- Mason attended Entrepreneurship Seminar
('100000035', 2), -- Aubrey attended Entrepreneurship Seminar

('100000003', 3), -- Tyla attended Engineering Social
('100000010', 3), -- Noah attended Engineering Social
('100000014', 3), -- Logan attended Engineering Social
('100000026', 3), -- Leo attended Engineering Social

-- Registered for upcoming events
('100000001', 4), -- Lucas registered for Hackathon
('100000006', 4), -- David registered for Hackathon
('100000011', 4), -- Emma registered for Hackathon
('100000034', 4), -- Benjamin registered for Hackathon

('100000002', 5), -- Jane registered for Pitch Night
('100000012', 5), -- Mason registered for Pitch Night
('100000035', 5), -- Aubrey registered for Pitch Night

('100000017', 6), -- Amelia registered for Sustainable Living Workshop
('100000010', 6), -- Noah registered for Sustainable Living Workshop

('100000003', 7), -- Tyla registered for Chess Tactics
('100000018', 7), -- Elijah registered for Chess Tactics
('100000001', 7), -- Lucas registered for Chess Tactics

('100000014', 8), -- Logan registered for Robotics Programming
('100000011', 8), -- Emma registered for Robotics Programming
('100000026', 8), -- Leo registered for Robotics Programming
('100000006', 8), -- David registered for Robotics Programming

('100000013', 9), -- Zoe registered for Cultural Festival
('100000021', 9), -- Layla registered for Cultural Festival
('100000012', 9), -- Mason registered for Cultural Festival

('100000027', 10), -- Grace registered for Healthcare Innovation
('100000029', 10), -- Chloe registered for Healthcare Innovation
('100000026', 10), -- Leo registered for Healthcare Innovation

('100000016', 11), -- Caleb registered for Creative Writing
('100000024', 11), -- Miles registered for Creative Writing

('100000001', 12), -- Lucas registered for Ethics of AI
('100000006', 12), -- David registered for Ethics of AI
('100000024', 12), -- Miles registered for Ethics of AI
('100000030', 12); -- Wyatt registered for Ethics of AI

-- Insert interests
INSERT INTO Interests (InterestName) VALUES
('Programming'),            -- ID 1
('Entrepreneurship'),       -- ID 2
('Engineering'),            -- ID 3
('Biology'),                -- ID 4
('Psychology'),             -- ID 5
('Artificial Intelligence'),-- ID 6
('Data Science'),           -- ID 7
('Marketing'),              -- ID 8
('Physics'),                -- ID 9
('Political Science'),      -- ID 10
('Sustainability'),         -- ID 11
('Web Development'),        -- ID 12
('Robotics'),               -- ID 13
('Healthcare'),             -- ID 14
('Creative Writing'),       -- ID 15
('Chess'),                  -- ID 16
('Machine Learning'),       -- ID 17
('International Relations'),-- ID 18
('Game Design'),            -- ID 19
('Film & Media');           -- ID 20

-- Insert student interests
INSERT INTO Interested (NUID, InterestID) VALUES
-- CS/Tech students
('100000001', 1), ('100000001', 6), ('100000001', 7), ('100000001', 12), ('100000001', 17), -- Lucas Lane
('100000006', 1), ('100000006', 6), ('100000006', 7), ('100000006', 17), -- David Miller
('100000011', 1), ('100000011', 3), ('100000011', 13), -- Emma Parker
('100000030', 1), ('100000030', 7), ('100000030', 12), -- Wyatt Lee
('100000034', 1), ('100000034', 12), ('100000034', 17), -- Benjamin Wilson

-- Business/Marketing students
('100000002', 2), ('100000002', 8), -- Jane Smith
('100000007', 2), ('100000007', 8), -- Sophia Davis
('100000012', 2), ('100000012', 18), -- Mason Thompson
('100000035', 2), ('100000035', 8), -- Aubrey Thompson

-- Engineering students
('100000003', 3), ('100000003', 13), ('100000003', 16), -- Tyla Johnson
('100000010', 3), ('100000010', 11), -- Noah Wilson
('100000014', 3), ('100000014', 13), -- Logan Hayes
('100000026', 3), ('100000026', 13), ('100000026', 14), -- Leo Martin

-- Environmental/Sustainability
('100000017', 11), ('100000017', 3), -- Amelia Reed

-- Healthcare/Biology
('100000004', 4), ('100000004', 14), -- Jack Williams
('100000027', 14), -- Grace Singh
('100000029', 5), ('100000029', 14), -- Chloe Martinez

-- Arts/Writing
('100000016', 15), -- Caleb Morgan
('100000024', 6), ('100000024', 15), -- Miles Walsh
('100000028', 15), ('100000028', 20), -- Henry Jones

-- Chess/Competitions
('100000018', 16), -- Elijah Cooper

-- International/Political
('100000009', 10), ('100000009', 18), -- Olivia Rodriguez
('100000013', 18); -- Zoe Bennett

-- Insert club interests mappings
INSERT INTO AppealsTo (InterestID, ClubId) VALUES
-- Coding Club
(1, 1), (6, 1), (7, 1), (12, 1), (17, 1),

-- Business Society
(2, 2), (8, 2),

-- Engineering Club
(3, 3), (13, 3),

-- Sustainable Future Initiative
(11, 4), (3, 4),

-- Chess Society
(16, 5), (9, 5),

-- Robotics Collective
(3, 6), (13, 6),

-- International Students Association
(18, 7),

-- Healthcare Leadership Forum
(14, 8), (4, 8), (5, 8),

-- Creative Writing Workshop
(15, 9),

-- AI Ethics Coalition
(6, 10), (17, 10);

-- Insert executive positions
INSERT INTO Executives (Position, NUID, ClubID) VALUES
-- Coding Club
('President', '100000001', 1), -- Lucas Lane as President
('Vice President', '100000006', 1), -- David Miller as VP
('Treasurer', '100000034', 1), -- Benjamin Wilson as Treasurer

-- Business Society
('President', '100000002', 2), -- Jane Smith as President
('Vice President', '100000007', 2), -- Sophia Davis as VP
('Event Coordinator', '100000035', 2), -- Aubrey Thompson as Event Coordinator

-- Engineering Club
('President', '100000003', 3), -- Tyla Johnson as President
('Vice President', '100000010', 3), -- Noah Wilson as VP
('Project Manager', '100000014', 3), -- Logan Hayes as Project Manager

-- Sustainable Future Initiative
('President', '100000017', 4), -- Amelia Reed as President
('Vice President', '100000010', 4), -- Noah Wilson as VP

-- Chess Society
('President', '100000018', 5), -- Elijah Cooper as President
('Vice President', '100000003', 5), -- Tyla Johnson as VP

-- Robotics Collective
('President', '100000011', 6), -- Emma Parker as President
('Vice President', '100000026', 6), -- Leo Martin as VP
('Technical Lead', '100000014', 6), -- Logan Hayes as Technical Lead

-- International Students Association
('President', '100000013', 7), -- Zoe Bennett as President
('Vice President', '100000021', 7), -- Layla Kim as VP
('Cultural Events Coordinator', '100000012', 7), -- Mason Thompson as Cultural Events

-- Healthcare Leadership Forum
('President', '100000027', 8), -- Grace Singh as President
('Vice President', '100000029', 8), -- Chloe Martinez as VP

-- Creative Writing Workshop
('President', '100000016', 9), -- Caleb Morgan as President
('Editor-in-Chief', '100000024', 9), -- Miles Walsh as Editor

-- AI Ethics Coalition
('President', '100000001', 10), -- Lucas Lane as President
('Vice President', '100000024', 10), -- Miles Walsh as VP
('Research Director', '100000006', 10); -- David Miller as Research Director

-- Insert analysts
INSERT INTO Analysts (AnalystName, Password, Email) VALUES
('Data Analyst 1', 'hashedpassword101', 'analyst1@northeastern.edu'), -- ID 1
('Data Analyst 2', 'hashedpassword102', 'analyst2@northeastern.edu'), -- ID 2
('Data Analyst 3', 'hashedpassword103', 'analyst3@northeastern.edu'); -- ID 3

-- Insert club memberships
INSERT INTO Membership (NUID, ClubID) VALUES
-- Coding Club members
('100000001', 1), -- Lucas Lane in Coding Club
('100000006', 1), -- David Miller in Coding Club
('100000011', 1), -- Emma Parker in Coding Club
('100000034', 1), -- Benjamin Wilson in Coding Club
('100000030', 1), -- Wyatt Lee in Coding Club

-- Business Society members
('100000002', 2), -- Jane Smith in Business Society
('100000007', 2), -- Sophia Davis in Business Society
('100000012', 2), -- Mason Thompson in Business Society
('100000035', 2), -- Aubrey Thompson in Business Society

-- Engineering Club members
('100000003', 3), -- Tyla Johnson in Engineering Club
('100000010', 3), -- Noah Wilson in Engineering Club
('100000014', 3), -- Logan Hayes in Engineering Club
('100000026', 3), -- Leo Martin in Engineering Club

-- Sustainable Future members
('100000017', 4), -- Amelia Reed in Sustainable Future
('100000010', 4), -- Noah Wilson in Sustainable Future
('100000013', 4), -- Zoe Bennett in Sustainable Future

-- Chess Society members
('100000018', 5), -- Elijah Cooper in Chess Society
('100000003', 5), -- Tyla Johnson in Chess Society
('100000001', 5), -- Lucas Lane in Chess Society
('100000031', 5), -- Isabella Taylor in Chess Society

-- Robotics Collective members
('100000011', 6), -- Emma Parker in Robotics Collective
('100000026', 6), -- Leo Martin in Robotics Collective
('100000014', 6), -- Logan Hayes in Robotics Collective
('100000006', 6), -- David Miller in Robotics Collective
('100000030', 6), -- Wyatt Lee in Robotics Collective

-- International Students Association members
('100000013', 7), -- Zoe Bennett in International Students
('100000021', 7), -- Layla Kim in International Students
('100000012', 7), -- Mason Thompson in International Students

-- Healthcare Leadership Forum members
('100000027', 8), -- Grace Singh in Healthcare Leadership
('100000029', 8), -- Chloe Martinez in Healthcare Leadership
('100000026', 8), -- Leo Martin in Healthcare Leadership
('100000004', 8), -- Jack Williams in Healthcare Leadership

-- Creative Writing Workshop members
('100000016', 9), -- Caleb Morgan in Creative Writing
('100000024', 9), -- Miles Walsh in Creative Writing
('100000028', 9), -- Henry Jones in Creative Writing

-- AI Ethics Coalition members
('100000001', 10), -- Lucas Lane in AI Ethics
('100000024', 10), -- Miles Walsh in AI Ethics
('100000006', 10), -- David Miller in AI Ethics
('100000030', 10); -- Wyatt Lee in AI Ethics

-- Insert request types
INSERT INTO RequestTypes (RequestType) VALUES
('Event Creation'),         -- ID 1
('Budget Approval'),        -- ID 2
('Room Booking'),           -- ID 3
('Membership Management'),  -- ID 4
('Program Creation');       -- ID 5

-- Insert requests
INSERT INTO Requests (RequestDescription, Status, Type, ExecutiveID, ExecutiveClub, ExecutivePosition, CreatedTime) VALUES
-- Event Creation Requests
('Request to create a hackathon event', TRUE, 1, '100000001', 1, 'President', '2024-08-01 09:00:00'), -- ID 1
('Request to organize business pitch competition', NULL, 1, '100000002', 2, 'President', '2024-08-05 10:30:00'), -- ID 2
('Request to create a sustainable living workshop', TRUE, 1, '100000017', 4, 'President', '2024-08-10 11:15:00'), -- ID 3
('Request to organize chess tournament', NULL, 1, '100000018', 5, 'President', '2024-08-15 12:00:00'), -- ID 4
('Request to create AI Ethics panel discussion', TRUE, 1, '100000001', 10, 'President', '2024-08-20 13:30:00'), -- ID 5

-- Budget Approval Requests
('Budget request for hackathon prizes', TRUE, 2, '100000001', 1, 'President', '2024-08-02 14:00:00'), -- ID 6
('Budget request for business networking event', FALSE, 2, '100000002', 2, 'President', '2024-08-06 15:15:00'), -- ID 7
('Budget request for sustainability campaign materials', NULL, 2, '100000017', 4, 'President', '2024-08-11 16:30:00'), -- ID 8
('Budget request for robotics competition materials', TRUE, 2, '100000011', 6, 'President', '2024-08-16 17:45:00'), -- ID 9
('Budget request for creative writing guest speakers', FALSE, 2, '100000016', 9, 'President', '2024-08-21 18:00:00'), -- ID 10

-- Room Booking Requests
('Request to book tech lab for coding workshop', TRUE, 3, '100000001', 1, 'President', '2024-08-03 09:30:00'), -- ID 11
('Request to book auditorium for business conference', NULL, 3, '100000002', 2, 'President', '2024-08-07 10:45:00'), -- ID 12
('Request to book engineering lab for project showcase', TRUE, 3, '100000003', 3, 'President', '2024-08-12 11:30:00'), -- ID 13
('Request to book student center for international festival', FALSE, 3, '100000013', 7, 'President', '2024-08-17 12:45:00'), -- ID 14
('Request to book classroom for writing workshop', NULL, 3, '100000016', 9, 'President', '2024-08-22 13:15:00'); -- ID 15

-- Insert request reviews
INSERT INTO RequestReviews (RequestID, AnalystID) VALUES
(1, 1), (2, 2), (3, 3), (4, 1), (5, 2),
(6, 3), (7, 1), (8, 2), (9, 3), (10, 1),
(11, 2), (12, 3), (13, 1), (14, 2), (15, 3);

-- Insert admin types
INSERT INTO AdminTypes (AdminType) VALUES
('Super Admin'),        -- ID 1
('Content Admin'),      -- ID 2
('User Admin'),         -- ID 3
('Event Admin'),        -- ID 4
('Club Admin');         -- ID 5

-- Insert support types
INSERT INTO SupportTypes (SupportType) VALUES
('Technical Issue'),    -- ID 1
('Account Problem'),    -- ID 2
('Feature Request'),    -- ID 3
('Bug Report'),         -- ID 4
('General Inquiry');    -- ID 5

-- Insert support requests
INSERT INTO SupportRequests (SupportRequestType, SupportRequestDescription, StudentID) VALUES
(1, 'Cannot log in to my account', '100000001'), -- ID 1
(2, 'Need to update my email address', '100000002'), -- ID 2
(3, 'Suggestion: add calendar integration with Google Calendar', '100000003'), -- ID 3
(4, 'Event registration button not working on mobile', '100000004'), -- ID 4
(5, 'Question about club membership fees', '100000005'), -- ID 5
(1, 'Website loads very slowly on my device', '100000006'), -- ID 6
(2, 'Cannot reset my password', '100000007'), -- ID 7
(3, 'Feature request: ability to message club members directly', '100000008'), -- ID 8
(4, 'Club search not showing all results', '100000009'), -- ID 9
(5, 'How do I transfer club leadership?', '100000010'); -- ID 10

-- Insert admins
INSERT INTO Admins (UserName, Password, TypeID) VALUES
('superadmin', 'hashedpassword_super', 1),      -- ID 1
('content_admin', 'hashedpassword_content', 2), -- ID 2
('user_admin', 'hashedpassword_user', 3),       -- ID 3
('event_admin', 'hashedpassword_event', 4),     -- ID 4
('club_admin', 'hashedpassword_club', 5);       -- ID 5

-- Insert support admin assignments
INSERT INTO SupportAdmins (AdminID, RequestID) VALUES
(1, 1), (3, 2), (2, 3), (4, 4), (5, 5),
(1, 6), (3, 7), (2, 8), (4, 9), (5, 10);