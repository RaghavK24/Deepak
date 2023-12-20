-- Table structure for table `jobs_for_disables`
CREATE TABLE IF NOT EXISTS `jobs_for_disables` (
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

-- Dumping data for table `jobs_for_disables`
INSERT INTO `jobs_for_disables` VALUES 
  (1, 'Data Entry Operator', 'Entering data accurately with suitable speed.', 1, '2023-12-18', 'Private', '10th', 'Fresher', 'Amritsar'),
  (2, 'Customer Service Representative', 'Assisting customers with their queries and issues.', 1, '2023-12-19', 'Government', '12th', '1 year', 'Udaipur'),
  (3, 'Office Assistant', 'Supporting office operations with administrative tasks.', 1, '2023-12-20', 'Private', 'Diploma after 10th', '1 year', 'Kota'),
  (4, 'Warehouse Worker', 'Handling inventory and ensuring smooth warehouse operations.', 1, '2023-12-21', 'Private', '8th Grade', 'Fresher', 'Firozpur'),
  (5, 'Receptionist', 'Welcoming visitors and managing front desk activities.', 1, '2023-12-22', 'Government', 'Diploma after 10th', '2 year', 'Faridkot'),
  (6, 'Security Guard', 'Maintaining security and ensuring safety within the premises.', 1, '2023-12-23', 'Private', '12th', '3 year', 'Bathinda');
