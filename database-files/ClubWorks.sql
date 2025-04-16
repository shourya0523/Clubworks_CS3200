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
('https://example.com/image1.jpg'),
('https://example.com/image2.jpg'),
('https://example.com/image3.jpg'),
('https://example.com/club_logo1.png'),
('https://example.com/club_logo2.png'),
('https://example.com/event_poster1.jpg'),
('https://example.com/event_poster2.jpg');


-- Insert test data into Students table
INSERT INTO Students (NUID, FirstName, LastName, GradDate, Email, Major, AboutMe, Password, ProfileIMG, JoinDate) VALUES
('123456789', 'Lucas', 'Lane', '2024-05-15', 'lucas.lane@northeastern.edu', 'Computer Science', 'I am a CS student interested in AI.', 'hashedpassword1', 1, '2024-07-01'),
('987654321', 'Jane', 'Smith', '2023-12-20', 'jane.smith@northeastern.edu', 'Business', 'Business major with interest in entrepreneurship.', 'hashedpassword2', 2, '2024-08-01'),
('456789123', 'Tyla', 'Johnson', '2025-05-10', 'tyla.j@northeastern.edu', 'Engineering', 'Mechanical engineering student.', 'hashedpassword3', 3, '2024-09-01'),
('789123456', 'Jack', 'Williams', '2024-05-15', 'connor.w@northeastern.edu', 'Biology', 'Pre-med student.', 'hashedpassword4', NULL, '2024-09-01'),
('321654987', 'Mary', 'Brown', '2023-12-20', 'michael.b@example.com', 'Psychology', 'Interested in clinical psychology.', 'hashedpassword5', NULL, '2024-07-01');


-- Insert test data into Follows table
INSERT INTO Follows (FollowerID, FolloweeID) VALUES
('123456789', '987654321'),
('123456789', '456789123'),
('987654321', '123456789'),
('456789123', '123456789'),
('789123456', '123456789'),
('321654987', '987654321');


-- Insert test data into Clubs table
INSERT INTO Clubs (ClubName, Description, LinkTree, CalendarLink, LogoImg) VALUES
('Coding Club', 'A club for coding enthusiasts', 'https://linktr.ee/codingclub', 'https://calendar.google.com/codingclub', 4),
('Business Society', 'For future entrepreneurs', 'https://linktr.ee/businesssociety', 'https://calendar.google.com/businesssociety', 5),
('Engineering Club', 'For engineering students', 'https://linktr.ee/engineeringclub', NULL, NULL),
('Biology Association', 'For biology enthusiasts', NULL, 'https://calendar.google.com/biologyassociation', NULL),
('Psychology Club', 'For psychology students', 'https://linktr.ee/psychclub', NULL, NULL);


-- Insert test data into Programs table
INSERT INTO Programs (ClubID, ProgramName, ProgramDescription, InfoLink) VALUES
(1, 'Hackathon', 'Annual coding competition', 'https://example.com/hackathon'),
(1, 'Code Workshop', 'Weekly coding workshops', 'https://example.com/workshop'),
(2, 'Startup Incubator', 'Program for startup ideas', 'https://example.com/incubator'),
(3, 'Engineering Projects', 'Hands-on engineering projects', 'https://example.com/engprojects'),
(4, 'Research Program', 'Biology research opportunities', 'https://example.com/research');


-- Insert test data into Participates table
INSERT INTO Participates (NUID, ProgramID) VALUES
('123456789', 1),
('123456789', 2),
('987654321', 3),
('456789123', 4),
('789123456', 5);


-- Insert test data into ApplicationStatus table
INSERT INTO ApplicationStatus (StatusText) VALUES
('Open'),
('Closed'),
('Under Review'),
('Accepted'),
('Rejected');


-- Insert test data into Applications table
INSERT INTO Applications (NAME, ProgramId, Description, Deadline, ApplyLink, Status) VALUES
('Summer Hackathon Application', 1, 'Apply for our summer hackathon', '2025-06-15 23:59:59', 'https://example.com/apply/hackathon', 1),
('Workshop Leader Application', 2, 'Apply to lead a workshop', '2025-05-20 23:59:59', 'https://example.com/apply/workshop', 3),
('Startup Funding Application', 3, 'Apply for startup funding', '2025-07-10 23:59:59', 'https://example.com/apply/funding', 1),
('Engineering Project Proposal', 4, 'Submit your project proposal', '2025-06-01 23:59:59', 'https://example.com/apply/project', 2),
('Research Assistant Application', 5, 'Apply to be a research assistant', '2025-05-25 23:59:59', 'https://example.com/apply/research', 4);


-- Insert test data into StudentApplication table
INSERT INTO StudentApplication (NUID, ApplicationID) VALUES
('123456789', 1),
('987654321', 3),
('456789123', 4),
('789123456', 5),
('321654987', 2);


-- Insert test data into Feedback table
INSERT INTO Feedback (Description, Rating, NUID, ClubID) VALUES
('Great club with helpful resources', 5, '123456789', 1),
('Love this club', 4, '123456789', 1),
('Enjoyed the events but could use more workshops', 4, '987654321', 2),
('Excellent mentorship opportunities', 5, '456789123', 3),
('Good community but limited resources', 3, '789123456', 4),
('Its not that great', 2, '789123456', 4),
('Needs more regular meetings', 3, '321654987', 5);


-- Insert test data into EventTypes table
INSERT INTO EventTypes (EventType) VALUES
('Workshop'),
('Seminar'),
('Social'),
('Competition'),
('Meeting');


-- Insert test data into Events table
INSERT INTO Events (Name, Location, StartTime, EndTime, ClubId, PosterImg, Type) VALUES
('Coding Workshop', 'Room 101', '2023-06-10 14:00:00', '2023-06-10 16:00:00', 1, 6, 1),
('Business Seminar', 'Auditorium', '2023-06-15 10:00:00', '2023-06-15 12:00:00', 2, 7, 2),
('Engineering Social', 'Student Center', '2023-06-20 18:00:00', '2023-06-20 20:00:00', 3, NULL, 3),
('Biology Competition', 'Science Building', '2023-06-25 09:00:00', '2023-06-25 17:00:00', 4, NULL, 4),
('Psychology Club Meeting', 'Room 205', '2023-06-05 16:00:00', '2023-06-05 17:00:00', 5, NULL, 5);


-- Insert test data into Attendance table
INSERT INTO Attendance (NUID, EventID) VALUES
('123456789', 1),
('987654321', 2),
('456789123', 3),
('789123456', 4),
('321654987', 5),
('123456789', 2),
('987654321', 1);


-- Insert test data into Interests table
INSERT INTO Interests (InterestName) VALUES
('Programming'),
('Entrepreneurship'),
('Engineering'),
('Biology'),
('Psychology'),
('Artificial Intelligence'),
('Data Science');


-- Insert test data into Interested table
INSERT INTO Interested (NUID, InterestID) VALUES
('123456789', 1),
('123456789', 6),
('987654321', 2),
('456789123', 3),
('789123456', 4),
('321654987', 5);


-- Insert test data into Executives table
INSERT INTO Executives (Position, NUID, ClubID) VALUES
('President', '123456789', 1),
('Vice President', '987654321', 1),
('President', '987654321', 2),
('Treasurer', '456789123', 3),
('Secretary', '789123456', 4),
('President', '321654987', 5);


-- Insert test data into AppealsTo table
INSERT INTO AppealsTo (InterestID, ClubId) VALUES
(1, 1),
(6, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(7, 1);


-- Insert test data into Analysts table
INSERT INTO Analysts (AnalystName, Password, Email) VALUES
('Data Analyst 1', 'hashedpassword6', 'analyst1@example.com'),
('Data Analyst 2', 'hashedpassword7', 'analyst2@example.com'),
('Data Analyst 3', 'hashedpassword8', 'analyst3@example.com');


-- Insert test data into Membership table
INSERT INTO Membership (NUID, ClubID) VALUES
('123456789', 1),
('123456789', 2),
('987654321', 2),
('456789123', 3),
('789123456', 4),
('321654987', 5);


-- Insert test data into RequestTypes table
INSERT INTO RequestTypes (RequestType) VALUES
('Event Creation'),
('Budget Approval'),
('Room Booking'),
('Membership Management'),
('Program Creation');


-- Insert test data into Requests table
INSERT INTO Requests (RequestDescription, Status, Type, ExecutiveID, ExecutiveClub, ExecutivePosition) VALUES
('Request to create a coding competition event', TRUE, 1, '123456789', 1, 'President'),
('Budget approval for Business Society annual conference', FALSE, 2, '987654321', 2, 'President'),
('Request to book Engineering Lab for project showcase', NULL, 3, '456789123', 3, 'Treasurer'),
('Request to update membership roster for Biology Association', TRUE, 4, '789123456', 4, 'Secretary'),
('Request to create a mentorship program for Psychology Club', FALSE, 5, '321654987', 5, 'President');


-- Insert test data into RequestReviews table
INSERT INTO RequestReviews (RequestID, AnalystID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 1),
(5, 2);


-- Insert test data into AdminTypes table
INSERT INTO AdminTypes (AdminType) VALUES
('Super Admin'),
('Content Admin'),
('User Admin'),
('Event Admin'),
('Club Admin');


-- Insert test data into SupportTypes table
INSERT INTO SupportTypes (SupportType) VALUES
('Technical Issue'),
('Account Problem'),
('Feature Request'),
('Bug Report'),
('General Inquiry');


-- Insert test data into SupportRequests table
INSERT INTO SupportRequests (SupportRequestType, SupportRequestDescription, StudentID) VALUES
(1, 'Cannot log in to my account', '123456789'),
(2, 'Need to update my email address', '987654321'),
(3, 'Suggestion for new club feature', '456789123'),
(4, 'Event registration not working', '789123456'),
(5, 'Question about club membership', '321654987');

-- Insert test data into Admins table
INSERT INTO Admins (UserName, Password, TypeID) VALUES
('connor123', 'hashedpassword9', 1),
('lucyjane80', 'hashedpassword10', 2),
('kristie.smith', 'hashedpassword11', 3),
('kathryn.johnson', 'hashedpassword12', 4),
('timothy5109northeastern', 'hashedpassword13', 5);

-- Insert test data into SupportAdmins table
INSERT INTO SupportAdmins (AdminID, RequestID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);


