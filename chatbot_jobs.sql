-- Table structure for table `jobs`
CREATE TABLE IF NOT EXISTS `jobs` (
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

-- Dumping data for table `jobs`
INSERT INTO `jobs` VALUES 
  (1, 'Full Stack Web Developer', 'Want a MERN stack developer, who has expertise in ReactJS', 1, '2023-03-12', 'private', 'Graduate', '2 years', 'Udaipur'),
  (2, 'Java developer', 'Requirement of experienced java developer', 1, '2023-10-22', 'government', 'post graduate', '5 years', 'Ahmedabad'),
  (3, 'Office assistant', 'Responsible for basic clerical tasks, including data entry, filing, and handling correspondence', 1, '2023-09-23', 'private', '10th', '1 year', 'Ahmedabad'),
  (4, 'Delivery Executive', 'Delivering packages promptly to customers while providing excellent customer service', 1, '2023-11-21', 'government', '10th', 'Fresher', 'Jaipur'),
  (5, 'Data Entry Operator', 'Inputting customer and account data from source documents within time limits', 0, '2023-08-03', 'private', '10th', '2 years', 'Udaipur'),
  (6, 'Marketing Executive', 'Assisting in the development and implementation of marketing strategies', 1, '2023-07-17', 'private', 'Graduate', '2 years', 'Ahmedabad'),
  (7, 'Software Developer', 'Designing, coding, and testing software applications', 1, '2023-10-20', 'government', 'Graduate', 'Fresher', 'Jaipur'),
  (8, 'HR Manager', 'Overseeing the HR departments operations and strategies', 1, '2023-12-03', 'private', 'Graduate', '5 years', 'Kota'),
  (9, 'Research Analyst', 'Analyzing market trends and providing actionable insights', 0, '2023-06-10', 'government', 'Post graduate', '2 years', 'Rajkot'),
  (10, 'Project Manager', 'Leading and managing projects from initiation to completion', 1, '2023-09-15', 'private', 'Post graduate', '10 years', 'Udaipur'),
  (11, 'Technical Support Associate', 'Providing technical assistance and support to customers via phone or email', 1, '2023-08-05', 'government', 'Diploma after 10th', '2 years', 'Ahmedabad'),
  (12, 'Mechanical Technician', 'Leading and managing projects from initiation to completion', 1, '2023-02-19', 'private', 'Diploma after 10th', 'Fresher', 'Ahmedabad'),
  (13, 'Electrical Engineer Trainee', 'Assisting senior engineers in designing, testing, and maintaining electrical systems', 1, '2022-12-25', 'private', 'Diploma after 10th', '9 years', 'Ahmedabad'),
  (14, 'Civil Engineering Technician', 'Assisting civil engineers in project planning, design, and site supervision', 1, '2023-07-07', 'private', 'Diploma after 12th', '1 year', 'Jaipur'),
  (15, 'Computer Hardware Technician', 'Installing, maintaining, and repairing computer hardware', 1, '2023-11-01', 'government', 'Diploma after 12th', '2 years', 'Jaipur'),
  (16, 'Medical Lab Technician', 'Maintaining laboratory equipment, records, and quality control procedures', 1, '2023-12-03', 'private', 'Diploma after 12th', 'Fresher', 'Jaipur'),
  (17, 'Automobile Technician', 'Diagnosing, repairing, and maintaining vehicle systems and components', 1, '2023-04-30', 'private', '12th', '1 year', 'Rajkot'),
  (18, 'Fashion Design Assistant', 'Assisting in the design and creation of fashion products', 1, '2023-06-29', 'government', '12th', 'Fresher', 'Rajkot'),
  (19, 'Pharmacy Assistant', 'Assisting pharmacists in dispensing medications and maintaining inventory', 1, '2023-09-12', 'government', 'Post graduate', '10 years', 'Rajkot');
