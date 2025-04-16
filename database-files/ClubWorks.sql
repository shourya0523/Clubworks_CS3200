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


-- Insert test data into Images table
INSERT INTO Images (ImageLink) VALUES
('https://example.com/image1.jpg'),        -- ID 1
('https://example.com/image2.jpg'),        -- ID 2
('https://example.com/image3.jpg'),        -- ID 3
('https://example.com/club_logo1.png'),    -- ID 4
('https://example.com/club_logo2.png'),    -- ID 5
('https://example.com/event_poster1.jpg'), -- ID 6
('https://example.com/event_poster2.jpg'), -- ID 7
('https://example.com/image4.jpg'),        -- ID 8
('https://example.com/image5.jpg'),        -- ID 9
('https://example.com/club_logo3.png'),    -- ID 10
('https://example.com/club_logo4.png'),    -- ID 11
('https://example.com/event_poster3.jpg'), -- ID 12
('https://example.com/event_poster4.jpg'), -- ID 13
('https://example.com/club_logo5.png'),    -- ID 14
('https://example.com/event_poster5.jpg'); -- ID 15


-- Insert test data into Students table
INSERT INTO Students (NUID, FirstName, LastName, GradDate, Email, Major, AboutMe, Password, ProfileIMG, JoinDate) VALUES
('123456789', 'Lucas', 'Lane', '2025-05-15', 'lucas.lane@northeastern.edu', 'Computer Science', 'I am a CS student interested in AI.', 'hashedpassword1', 1, '2023-09-01'),
('987654321', 'Jane', 'Smith', '2024-12-20', 'jane.smith@northeastern.edu', 'Business', 'Business major with interest in entrepreneurship.', 'hashedpassword2', 2, '2023-10-01'),
('456789123', 'Tyla', 'Johnson', '2026-05-10', 'tyla.j@northeastern.edu', 'Engineering', 'Mechanical engineering student.', 'hashedpassword3', 3, '2023-11-01'),
('789123456', 'Jack', 'Williams', '2025-05-15', 'connor.w@northeastern.edu', 'Biology', 'Pre-med student.', 'hashedpassword4', NULL, '2023-11-15'),
('321654987', 'Mary', 'Brown', '2024-12-20', 'michael.b@example.com', 'Psychology', 'Interested in clinical psychology.', 'hashedpassword5', NULL, '2023-09-10'),
('112233445', 'David', 'Miller', '2026-05-15', 'david.miller@northeastern.edu', 'Data Science', 'Data science enthusiast, love visualization.', 'hashedpassword14', 8, '2024-01-10'),
('223344556', 'Sophia', 'Davis', '2025-12-20', 'sophia.davis@northeastern.edu', 'Marketing', 'Exploring digital marketing strategies.', 'hashedpassword15', 9, '2024-02-15'),
('334455667', 'Ethan', 'Garcia', '2025-08-15', 'ethan.garcia@northeastern.edu', 'Physics', 'Fascinated by quantum mechanics.', 'hashedpassword16', NULL, '2024-03-20'),
('445566778', 'Olivia', 'Rodriguez', '2026-12-20', 'olivia.r@northeastern.edu', 'Political Science', 'Interested in international relations.', 'hashedpassword17', NULL, '2024-04-25'),
('556677889', 'Noah', 'Wilson', '2025-05-10', 'noah.wilson@northeastern.edu', 'Chemical Engineering', 'Focusing on sustainable energy solutions.', 'hashedpassword18', NULL, '2024-05-30'),
('667788990', 'Ava', 'Martinez', '2027-05-15', 'ava.martinez@northeastern.edu', 'Graphic Design', 'Passionate about visual communication.', 'hashedpassword19', NULL, '2024-08-11'),
('778899001', 'Liam', 'Anderson', '2025-12-20', 'liam.anderson@northeastern.edu', 'Economics', 'Analyzing market trends.', 'hashedpassword20', NULL, '2024-09-22');


-- Insert test data into Follows table
INSERT INTO Follows (FollowerID, FolloweeID) VALUES
('123456789', '987654321'),
('123456789', '456789123'),
('987654321', '123456789'),
('456789123', '123456789'),
('789123456', '123456789'),
('321654987', '987654321'),
('112233445', '123456789'),
('112233445', '987654321'),
('223344556', '112233445'),
('334455667', '456789123'),
('445566778', '789123456'),
('556677889', '321654987'),
('123456789', '112233445'),
('667788990', '223344556'),
('778899001', '445566778'),
('223344556', '667788990');


-- Insert test data into Clubs table
INSERT INTO Clubs (ClubName, Description, LinkTree, CalendarLink, LogoImg) VALUES
('Coding Club', 'A club for coding enthusiasts', 'https://linktr.ee/codingclub', 'https://calendar.google.com/codingclub', 4), -- ID 1
('Business Society', 'For future entrepreneurs', 'https://linktr.ee/businesssociety', 'https://calendar.google.com/businesssociety', 5), -- ID 2
('Engineering Club', 'For engineering students', 'https://linktr.ee/engineeringclub', NULL, NULL), -- ID 3
('Biology Association', 'For biology enthusiasts', NULL, 'https://calendar.google.com/biologyassociation', NULL), -- ID 4
('Psychology Club', 'For psychology students', 'https://linktr.ee/psychclub', NULL, NULL), -- ID 5
('Data Science Group', 'Exploring data analysis and machine learning', 'https://linktr.ee/datascience', 'https://calendar.google.com/datascience', 10), -- ID 6
('Marketing Mavens', 'Connecting marketing students and professionals', 'https://linktr.ee/marketingmavens', NULL, 11), -- ID 7
('Physics Forum', 'Discussions and events related to physics', NULL, 'https://calendar.google.com/physicsforum', NULL), -- ID 8
('Design Collective', 'Community for designers of all disciplines', 'https://linktr.ee/designcollective', 'https://calendar.google.com/designcollective', 14), -- ID 9
('Economics Hub', 'Discussing economic theories and current events', 'https://linktr.ee/econhub', NULL, NULL); -- ID 10


-- Insert test data into Programs table
INSERT INTO Programs (ClubID, ProgramName, ProgramDescription, InfoLink) VALUES
(1, 'Hackathon', 'Annual coding competition', 'https://example.com/hackathon'), -- ID 1
(1, 'Code Workshop', 'Weekly coding workshops', 'https://example.com/workshop'), -- ID 2
(2, 'Startup Incubator', 'Program for startup ideas', 'https://example.com/incubator'), -- ID 3
(3, 'Engineering Projects', 'Hands-on engineering projects', 'https://example.com/engprojects'), -- ID 4
(4, 'Research Program', 'Biology research opportunities', 'https://example.com/research'), -- ID 5
(6, 'Data Visualization Challenge', 'Compete to create the best data visualizations', 'https://example.com/dataviz'), -- ID 6
(6, 'ML Study Group', 'Collaborative learning for machine learning topics', 'https://example.com/mlstudy'), -- ID 7
(7, 'Digital Marketing Bootcamp', 'Intensive training on digital marketing tools', 'https://example.com/marketingbootcamp'), -- ID 8
(8, 'Physics Seminar Series', 'Guest lectures on cutting-edge physics research', 'https://example.com/physicsseminars'), -- ID 9
(9, 'Portfolio Review Session', 'Get feedback on your design portfolio', 'https://example.com/portfolioreview'), -- ID 10
(10, 'Economic Policy Debate', 'Debate current economic policies', 'https://example.com/econdebate'); -- ID 11


-- Insert test data into Participates table
INSERT INTO Participates (NUID, ProgramID) VALUES
('123456789', 1),
('123456789', 2),
('987654321', 3),
('456789123', 4),
('789123456', 5),
('112233445', 6),
('112233445', 7),
('123456789', 7),
('223344556', 8),
('334455667', 9),
('556677889', 4),
('667788990', 10),
('778899001', 11),
('223344556', 3);


-- Insert test data into ApplicationStatus table
INSERT INTO ApplicationStatus (StatusText) VALUES
('Open'),       -- ID 1
('Closed'),     -- ID 2
('Under Review'); -- ID 3


-- Insert test data into Applications table
-- Adjusted Deadlines and PostedDate to be more current/future
INSERT INTO Applications (NAME, ProgramId, Description, Deadline, ApplyLink, Status, PostedDate) VALUES
('Fall Hackathon Application', 1, 'Apply for our fall hackathon', '2024-10-15 23:59:59', 'https://example.com/apply/hackathon', 1, '2024-09-01 10:00:00'), -- ID 1
('Workshop Leader Application', 2, 'Apply to lead a workshop', '2024-09-20 23:59:59', 'https://example.com/apply/workshop', 3, '2024-08-15 11:00:00'), -- ID 2
('Startup Funding Application', 3, 'Apply for startup funding', '2025-01-10 23:59:59', 'https://example.com/apply/funding', 1, '2024-11-01 09:00:00'), -- ID 3
('Engineering Project Proposal', 4, 'Submit your project proposal', '2024-11-01 23:59:59', 'https://example.com/apply/project', 2, '2024-09-15 14:00:00'), -- ID 4
('Research Assistant Application', 5, 'Apply to be a research assistant', '2024-09-25 23:59:59', 'https://example.com/apply/research', 2, '2024-08-20 16:00:00'), -- ID 5
('DataViz Challenge Entry', 6, 'Submit your visualization for the challenge', '2024-11-30 23:59:59', 'https://example.com/apply/dataviz', 1, '2024-10-01 10:00:00'), -- ID 6
('ML Study Group Sign-up', 7, 'Join the machine learning study group', '2024-09-15 23:59:59', 'https://example.com/apply/mlstudy', 1, '2024-08-25 12:00:00'), -- ID 7
('Marketing Bootcamp Registration', 8, 'Register for the digital marketing bootcamp', '2024-10-01 23:59:59', 'https://example.com/apply/bootcamp', 1, '2024-09-05 13:00:00'), -- ID 8
('Physics Seminar Speaker Proposal', 9, 'Propose a topic to present at our seminar series', '2024-12-31 23:59:59', 'https://example.com/apply/physicspeaker', 3, '2024-10-15 15:00:00'), -- ID 9
('Portfolio Review Sign-up', 10, 'Sign up to have your portfolio reviewed', '2025-01-15 23:59:59', 'https://example.com/apply/portfolioreview', 1, '2024-12-01 11:00:00'), -- ID 10
('Economic Debate Team Application', 11, 'Apply to join the debate team', '2024-09-30 23:59:59', 'https://example.com/apply/econdebate', 1, '2024-09-01 17:00:00'); -- ID 11


-- Insert test data into StudentApplication table
INSERT INTO StudentApplication (NUID, ApplicationID) VALUES
('123456789', 1),
('987654321', 3),
('456789123', 4),
('789123456', 5),
('321654987', 2),
('112233445', 6),
('112233445', 7),
('123456789', 7),
('223344556', 8),
('334455667', 9),
('556677889', 4),
('667788990', 10),
('778899001', 11),
('445566778', 5);


-- Insert test data into Feedback table
INSERT INTO Feedback (Description, Rating, NUID, ClubID) VALUES
('Great club with helpful resources', 5, '123456789', 1),
('Love this club', 4, '123456789', 1),
('Enjoyed the events but could use more workshops', 4, '987654321', 2),
('Excellent mentorship opportunities', 5, '456789123', 3),
('Good community but limited resources', 3, '789123456', 4),
('Its not that great', 2, '789123456', 4),
('Needs more regular meetings', 3, '321654987', 5),
('Data Science Group has amazing projects!', 5, '112233445', 6),
('The ML study group was very informative.', 4, '112233445', 6),
('Marketing Mavens events are top-notch.', 5, '223344556', 7),
('Wish the Physics Forum had more social events.', 3, '334455667', 8),
('Coding Club hackathon was intense but fun.', 4, '123456789', 1),
('Business Society needs better communication.', 2, '987654321', 2),
('Design Collective portfolio review was super helpful!', 5, '667788990', 9),
('Economics Hub debates are always engaging.', 4, '778899001', 10);


-- Insert test data into EventTypes table
INSERT INTO EventTypes (EventType) VALUES
('Workshop'),       -- ID 1
('Seminar'),        -- ID 2
('Social'),         -- ID 3
('Competition'),    -- ID 4
('Meeting'),        -- ID 5
('Guest Speaker'),  -- ID 6
('Study Session'),  -- ID 7
('Portfolio Review'),-- ID 8
('Debate');         -- ID 9


-- Insert test data into Events table
-- Adjusted StartTime and EndTime to be more current/future
INSERT INTO Events (Name, Location, Description, StartTime, EndTime, ClubId, PosterImg, Type) VALUES
('Coding Workshop', 'Room 101', 'Learn the basics of Python programming in this hands-on workshop. Bring your laptop and be ready to code!', '2024-09-10 14:00:00', '2024-09-10 16:00:00', 1, 6, 1), -- ID 1
('Business Seminar', 'Auditorium', 'Join us for a seminar on entrepreneurship featuring guest speakers from successful startups. Networking opportunity after the event.', '2024-09-15 10:00:00', '2024-09-15 12:00:00', 2, 7, 2), -- ID 2
('Engineering Social', 'Student Center', 'Meet fellow engineering students and faculty in a casual setting. Refreshments will be provided.', '2024-09-20 18:00:00', '2024-09-20 20:00:00', 3, NULL, 3), -- ID 3
('Biology Competition', 'Science Building', 'Test your biology knowledge in this day-long competition. Prizes for top performers. Registration required.', '2024-09-25 09:00:00', '2024-09-25 17:00:00', 4, NULL, 4), -- ID 4
('Psychology Club Meeting', 'Room 205', 'Monthly meeting to discuss upcoming events and initiatives. All psychology majors and interested students welcome.', '2024-10-05 16:00:00', '2024-10-05 17:00:00', 5, NULL, 5), -- ID 5
('Data Science Guest Lecture', 'Behrakis Hall', 'Industry expert discusses trends in Big Data.', '2024-10-15 17:00:00', '2024-10-15 18:30:00', 6, 12, 6), -- ID 6
('Marketing Networking Night', 'Cabral Center', 'Connect with marketing professionals from Boston.', '2024-11-05 19:00:00', '2024-11-05 21:00:00', 7, 13, 3), -- ID 7
('Physics Midterm Study Session', 'Library Room 3', 'Collaborative study session for PHYS 1151.', '2024-10-22 18:00:00', '2024-10-22 20:00:00', 8, NULL, 7), -- ID 8
('Advanced Python Workshop', 'WVH 110', 'Deep dive into advanced Python concepts and libraries.', '2025-02-12 15:00:00', '2025-02-12 17:00:00', 1, NULL, 1), -- ID 9
('Entrepreneurship Panel', 'West Village F 020', 'Hear from successful Northeastern alumni entrepreneurs.', '2025-03-20 18:00:00', '2025-03-20 19:30:00', 2, NULL, 6), -- ID 10
('Design Portfolio Reviews', 'Ryder Hall 150', 'Get 1-on-1 feedback from industry professionals.', '2025-04-10 13:00:00', '2025-04-10 16:00:00', 9, 15, 8), -- ID 11
('Economic Outlook Debate', 'Curry Ballroom', 'Debate on the future of the US economy.', '2025-04-25 19:00:00', '2025-04-25 20:30:00', 10, NULL, 9); -- ID 12


-- Insert test data into Attendance table
INSERT INTO Attendance (NUID, EventID) VALUES
('123456789', 1),
('987654321', 2),
('456789123', 3),
('789123456', 4),
('321654987', 5),
('123456789', 2),
('987654321', 1),
('112233445', 6),
('123456789', 6),
('223344556', 7),
('987654321', 7),
('334455667', 8),
('445566778', 8),
('112233445', 9),
('123456789', 9),
('987654321', 10),
('223344556', 10),
('667788990', 11),
('112233445', 11),
('778899001', 12),
('445566778', 12);


-- Insert test data into Interests table
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
('Graphic Design'),         -- ID 13
('Economics'),              -- ID 14
('Finance'),                -- ID 15
('User Experience (UX)');   -- ID 16


-- Insert test data into Interested table
INSERT INTO Interested (NUID, InterestID) VALUES
('123456789', 1), ('123456789', 6), ('123456789', 7), ('123456789', 12),
('987654321', 2), ('987654321', 8), ('987654321', 15),
('456789123', 3), ('456789123', 11),
('789123456', 4),
('321654987', 5),
('112233445', 7), ('112233445', 6), ('112233445', 1),
('223344556', 8), ('223344556', 2), ('223344556', 16),
('334455667', 9),
('445566778', 10), ('445566778', 14),
('556677889', 3), ('556677889', 11),
('667788990', 13), ('667788990', 16),
('778899001', 14), ('778899001', 15), ('778899001', 2);


-- Insert test data into Executives table
INSERT INTO Executives (Position, NUID, ClubID) VALUES
('President', '123456789', 1),
-- ('Vice President', '987654321', 1), -- Removed: '987654321' is President of Club 2
('President', '987654321', 2),
('Treasurer', '456789123', 3),
('Secretary', '789123456', 4),
('President', '321654987', 5),
('President', '112233445', 6), -- David Miller for Data Science Group
('President', '223344556', 7), -- Sophia Davis for Marketing Mavens
('President', '334455667', 8), -- Ethan Garcia for Physics Forum
('President', '667788990', 9), -- Ava Martinez for Design Collective
('President', '778899001', 10);-- Liam Anderson for Economics Hub


-- Insert test data into AppealsTo table
INSERT INTO AppealsTo (InterestID, ClubId) VALUES
(1, 1), (6, 1), (7, 1), (12, 1), -- Coding Club
(2, 2), (8, 2), (15, 2), -- Business Society
(3, 3), (11, 3), -- Engineering Club
(4, 4), -- Biology Association
(5, 5), -- Psychology Club
(7, 6), (6, 6), (1, 6), -- Data Science Group
(8, 7), (2, 7), (16, 7), -- Marketing Mavens
(9, 8), (3, 8), -- Physics Forum
(13, 9), (16, 9), -- Design Collective
(14, 10), (2, 10), (15, 10); -- Economics Hub


-- Insert test data into Analysts table
INSERT INTO Analysts (AnalystName, Password, Email) VALUES
('Data Analyst 1', 'hashedpassword6', 'analyst1@example.com'), -- ID 1
('Data Analyst 2', 'hashedpassword7', 'analyst2@example.com'), -- ID 2
('Data Analyst 3', 'hashedpassword8', 'analyst3@example.com'); -- ID 3


-- Insert test data into Membership table
INSERT INTO Membership (NUID, ClubID) VALUES
('123456789', 1), ('123456789', 2), ('123456789', 6),
('987654321', 2), ('987654321', 7),
('456789123', 3), ('456789123', 8),
('789123456', 4),
('321654987', 5),
('112233445', 6), ('112233445', 1),
('223344556', 7), ('223344556', 2),
('334455667', 8),
('445566778', 10),
('556677889', 3),
('667788990', 9), ('667788990', 7),
('778899001', 10), ('778899001', 2);


-- Insert test data into RequestTypes table
INSERT INTO RequestTypes (RequestType) VALUES
('Event Creation'),         -- ID 1
('Budget Approval'),        -- ID 2
('Room Booking'),           -- ID 3
('Membership Management'),  -- ID 4
('Program Creation');       -- ID 5


-- Insert test data into Requests table
INSERT INTO Requests (RequestDescription, Status, Type, ExecutiveID, ExecutiveClub, ExecutivePosition, CreatedTime) VALUES
('Request to create a coding competition event', TRUE, 1, '123456789', 1, 'President', '2024-08-01 09:00:00'), -- ID 1
('Budget approval for Business Society annual conference', FALSE, 2, '987654321', 2, 'President', '2024-08-05 10:30:00'), -- ID 2
('Request to book Engineering Lab for project showcase', NULL, 3, '456789123', 3, 'Treasurer', '2024-08-10 11:00:00'), -- ID 3
('Request to update membership roster for Biology Association', TRUE, 4, '789123456', 4, 'Secretary', '2024-08-12 14:00:00'), -- ID 4
('Request to create a mentorship program for Psychology Club', FALSE, 5, '321654987', 5, 'President', '2024-08-15 16:20:00'), -- ID 5
('Request to create Data Science guest lecture event', TRUE, 1, '112233445', 6, 'President', '2024-08-20 09:30:00'), -- ID 6
('Budget approval for Marketing Mavens networking night', TRUE, 2, '223344556', 7, 'President', '2024-08-22 11:45:00'), -- ID 7
('Request to book room for Physics study session', TRUE, 3, '334455667', 8, 'President', '2024-08-25 13:00:00'), -- ID 8
('Request to create Design Collective portfolio review program', TRUE, 5, '667788990', 9, 'President', '2024-08-28 15:00:00'), -- ID 9
('Budget approval for Economics Hub debate event', FALSE, 2, '778899001', 10, 'President', '2024-09-01 10:00:00'); -- ID 10


-- Insert test data into RequestReviews table
INSERT INTO RequestReviews (RequestID, AnalystID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 1),
(5, 2),
(6, 1),
(7, 2),
(8, 3),
(9, 1),
(10, 2);


-- Insert test data into AdminTypes table
INSERT INTO AdminTypes (AdminType) VALUES
('Super Admin'),        -- ID 1
('Content Admin'),      -- ID 2
('User Admin'),         -- ID 3
('Event Admin'),        -- ID 4
('Club Admin');         -- ID 5


-- Insert test data into SupportTypes table
INSERT INTO SupportTypes (SupportType) VALUES
('Technical Issue'),    -- ID 1
('Account Problem'),    -- ID 2
('Feature Request'),    -- ID 3
('Bug Report'),         -- ID 4
('General Inquiry');    -- ID 5


-- Insert test data into SupportRequests table
INSERT INTO SupportRequests (SupportRequestType, SupportRequestDescription, StudentID) VALUES
(1, 'Cannot log in to my account', '123456789'), -- ID 1
(2, 'Need to update my email address', '987654321'), -- ID 2
(3, 'Suggestion for new club feature: event reminders', '456789123'), -- ID 3
(4, 'Event registration button not working on mobile', '789123456'), -- ID 4
(5, 'Question about club membership fees', '321654987'), -- ID 5
(1, 'Website is loading very slowly today', '112233445'), -- ID 6
(2, 'Forgot my password, reset link not received', '223344556'), -- ID 7
(4, 'Club page description has a typo', '334455667'), -- ID 8
(5, 'How do I leave a club?', '445566778'), -- ID 9
(3, 'Can we have a dark mode option?', '556677889'); -- ID 10

-- Insert test data into Admins table
INSERT INTO Admins (UserName, Password, TypeID) VALUES
('superadmin', 'hashedpassword_super', 1),      -- ID 1
('content_editor', 'hashedpassword_content', 2), -- ID 2
('user_manager', 'hashedpassword_user', 3),     -- ID 3
('event_coord', 'hashedpassword_event', 4),      -- ID 4
('club_liaison', 'hashedpassword_club', 5),      -- ID 5
('admin_jane', 'hashedpassword_jane', 1),        -- ID 6
('admin_lucas', 'hashedpassword_lucas', 3);      -- ID 7

-- Insert test data into SupportAdmins table
INSERT INTO SupportAdmins (AdminID, RequestID) VALUES
(1, 1), (1, 7), -- Super Admin handles login/password issues
(3, 2), (3, 9), -- User Admin handles account updates/leaving clubs
(2, 8), -- Content Admin handles typo reports
(4, 4), -- Event Admin handles event registration bugs
(5, 5), -- Club Admin handles general club questions
(6, 3), (6, 10), -- Admin Jane handles feature requests
(7, 6); -- Admin Lucas handles technical issues (slow site)


