-- Table structure for table `jobs_for_women`
CREATE TABLE IF NOT EXISTS `jobs_for_women` (
  `job_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `job_title` TEXT DEFAULT NULL,
  `job_description` TEXT,
  `is_active` INTEGER DEFAULT NULL,
  `created_on` DATE DEFAULT NULL,
  `job_type` TEXT DEFAULT NULL,
  `qualification` TEXT DEFAULT NULL,
  `experience` TEXT DEFAULT NULL,
  `location` TEXT DEFAULT NULL
);

-- Dumping data for table `jobs_for_women`
INSERT INTO `jobs_for_women` VALUES 
  (1, 'Baby Sitter', 'requirement of a baby sitter who can take care of my child when I am at work', 1, '2023-12-01', 'private', 'no schooling', 'fresher', 'Rajkot'),
  (2, 'Home Decor', 'requirement of a creative home decor for decorating my home', 1, '2023-10-01', 'private', 'graduate', '2 years', 'Jaipur'),
  (3, 'Software Engineer', 'Description for Software Engineer position', 1, '2023-12-05', 'Private', 'Post graduate', '2 year', 'Udaipur'),
  (4, 'HR Manager', 'Description for HR Manager position', 1, '2023-12-06', 'Government', 'Phd', '5 year', 'Jaipur'),
  (5, 'Nurse', 'Description for Nurse position', 1, '2023-12-07', 'Private', 'Graduate', '3 year', 'Kota'),
  (6, 'Marketing Coordinator', 'Description for Marketing Coordinator position', 1, '2023-12-08', 'Private', 'Graduate', '2 years', 'Ahmedabad'),
  (7, 'Financial Analyst', 'Description for Financial Analyst position', 1, '2023-12-09', 'Government', 'Post graduate', '4 years', 'Rajkot'),
  (8, 'Event Planner', 'Description for Event Planner position', 1, '2023-12-10', 'Private', 'Phd', '6 years', 'Kota'),
  (9, 'Office Assistant', 'Description for Office Assistant position', 1, '2023-12-11', 'Private', '8th', '1 year', 'Bathinda'),
  (10, 'Sales Representative', 'Description for Sales Representative position', 1, '2023-12-12', 'Government', 'Diploma after 12th', '3 year', 'Firozpur'),
  (11, 'Graphic Designer', 'Description for Graphic Designer position', 1, '2023-12-13', 'Private', 'Diploma after 10th', '2 year', 'Ujjain'),
  (12, 'Teacher', 'Description for Teacher position', 1, '2023-12-14', 'Private', 'M Phil', '4 year', 'Umaria'),
  (13, 'Research Analyst', 'Description for Research Analyst position', 1, '2023-12-15', 'Government', 'PhD', '7 year', 'Amritsar'),
  (14, 'Cleaner', 'Description for Cleaner position', 1, '2023-12-16', 'Private', 'No Schooling', 'Fresher', 'West Nimar');
