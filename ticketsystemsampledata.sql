-- Sample data for userrole table
INSERT INTO userrole (RoleID,RoleName) VALUES 
('1','agent'),
('2','customer');

-- Sample data for user table
INSERT INTO user (Username, Password, RoleID) VALUES 
('agent1', 'password1', 1),  
('agent2', 'password2', 1),  
('customer1', 'password1', 2),  
('customer2', 'password2', 2);  

-- Sample data for ticket table
INSERT INTO ticket (TicketNumber, UserID, TicketContent, State, Created, Modified) VALUES
(100001, 3, 'Issue with network connection', 'open', NOW(), NOW()),
(100002, 3, 'Software not functioning properly', 'open', NOW(), NOW()),
(100003, 4, 'Cannot access email', 'open', NOW(), NOW()),
(100004, 4, 'Request for product demo', 'open', NOW(), NOW()),
(100005, 3, 'Issue with printer', 'open', NOW(), NOW()),
(100006, 3, 'Payment processing error', 'open', NOW(), NOW()),
(100007, 4, 'Website down', 'open', NOW(), NOW()),
(100008, 4, 'Account access problem', 'open', NOW(), NOW()),
(100009, 3, 'Slow performance on website', 'open', NOW(), NOW()),
(100010, 3, 'Billing discrepancy', 'open', NOW(), NOW());

-- Sample data for ticketcomment table
INSERT INTO ticketcomment (TicketNumber, UserID, CommentContent, CommentDate) VALUES
(100001, 3, 'Yes, I have tried resetting the password but still facing the issue', NOW()),
(100002, 1, 'I will assign a technician to investigate the network issue', NOW()),
(100003, 2, 'Could you provide more details about the software issue?', NOW()),
(100004, 4, 'I can assist you with accessing your email. Let me know if you need help.', NOW()),
(100005, 1, 'Thank you for scheduling the product demo. Looking forward to it.', NOW()),
(100006, 3, 'The printer has been serviced and should be working fine now.', NOW()),
(100007, 1, 'We have identified the payment processing error and are working on a fix.', NOW()),
(100008, 2, 'The website should be back up and running now. Apologies for the inconvenience.', NOW()),
(100009, 4, 'Please check your email for instructions on account verification.', NOW()),
(100010, 3, 'Optimization measures have been implemented. Performance should improve.', NOW());

-- Sample data for useractivity table
INSERT INTO useractivity (UserID, ActivityType, ActivityDate) VALUES
(1, 'login', NOW()),
(2, 'login', NOW()),
(3, 'login', NOW()),
(4, 'login', NOW());
