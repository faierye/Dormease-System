-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 15, 2026 at 03:01 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dormease_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_log`
--

CREATE TABLE `activity_log` (
  `id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity_log`
--

INSERT INTO `activity_log` (`id`, `action`, `created_at`) VALUES
(1, 'New resident added: Jodi Faye Mayo', '2026-05-12 20:58:31'),
(2, 'Bed assigned: Jodi Faye Mayo → Room 2 Bed 1', '2026-05-12 21:02:41'),
(3, 'Resident stay ended: Jane Doe (End date: 2026-05-13)', '2026-05-12 21:48:52'),
(4, 'Resident archived: Jane Doe', '2026-05-12 21:53:19'),
(5, 'Resident stay ended: Jodi Mayo (End date: 2026-05-13)', '2026-05-12 22:42:45'),
(6, 'Resident archived: Jodi Mayo', '2026-05-12 22:42:48'),
(7, 'Payment marked as Paid: Jodi Faye Mayo', '2026-05-13 00:35:35'),
(8, 'New resident added: REYNALD  CABUJOC ', '2026-05-13 06:11:26'),
(9, 'Bed assigned: REYNALD  CABUJOC  → Room 1 Bed 3', '2026-05-13 06:12:05'),
(10, 'Resident stay ended: REYNALD  CABUJOC  (End date: 2026-05-14)', '2026-05-14 04:36:40'),
(11, 'Resident archived: REYNALD  CABUJOC ', '2026-05-14 04:36:47');

-- --------------------------------------------------------

--
-- Table structure for table `admin_tb`
--

CREATE TABLE `admin_tb` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) CHARACTER SET utf32 COLLATE utf32_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_tb`
--

INSERT INTO `admin_tb` (`admin_id`, `username`, `password`) VALUES
(1, 'admin', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `applications_tb`
--

CREATE TABLE `applications_tb` (
  `application_id` int(11) NOT NULL,
  `period_id` int(11) NOT NULL,
  `applicant_number` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `extension_name` varchar(50) NOT NULL,
  `age` int(11) NOT NULL,
  `sex` varchar(10) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `permanent_address` varchar(255) NOT NULL,
  `current_address` varchar(255) NOT NULL,
  `applicant_type` enum('Student','Employee') NOT NULL,
  `status` enum('Pending','For_Interview','For_Approval','Approved','Rejected') NOT NULL DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications_tb`
--

INSERT INTO `applications_tb` (`application_id`, `period_id`, `applicant_number`, `first_name`, `middle_name`, `last_name`, `extension_name`, `age`, `sex`, `contact_number`, `email`, `permanent_address`, `current_address`, `applicant_type`, `status`, `created_at`) VALUES
(2, 1, 'APP-2026-0002', 'Jodi', 'Bongo', 'Mayo', '', 20, 'Female', '09123456789', 'jodi@gmail.com', 'Brgy. Pago Tanauan, Leyte', 'Brgy. Pago Tanauan, Leyte', 'Student', 'Approved', '2026-05-03 07:37:33'),
(3, 1, 'APP-2026-0003', 'Jane', 'A ', 'Doe', '', 19, 'Female', '09526382589', 'janedoe@gmail.com', 'Tacloban, City', 'Tacloban, City', 'Student', 'Approved', '2026-05-03 04:10:16'),
(4, 1, 'APP-2026-0004', 'Jilliane Mae', 'A', 'Javellana', '', 19, 'Female', '0912234567', 'javellana@gmail.com', 'Brgy. Pilit Santa Fe, Leyte', 'Brgy. Pilit Santa Fe, Leyte', 'Student', 'Approved', '2026-05-04 01:46:29'),
(5, 1, 'APP-2026-0005', 'John', 'A', 'Doe', '', 21, 'Male', '09564317974', 'johndoe@gmail.com', 'Brgy. San Roque Tanauan, Leyte', 'Brgy. San Roque Tanauan, Leyte', 'Employee', 'Approved', '2026-05-07 06:55:44'),
(6, 1, 'APP-2026-0006', 'Yoongi', 'Suga', 'Min', '', 32, 'Male', '09526382562', 'minyoongi13@gmail.com', 'Brgy. Zone 2, Santa Fe, Leyte', 'Brgy. Zone 2, Santa Fe, Leyte', 'Employee', 'Rejected', '2026-05-12 07:50:18'),
(7, 1, 'APP-2026-0007', 'Jodi Faye', 'B.', 'Mayo', '', -21, 'Female', '09212189745', 'jodimayo98@gmail.com', 'Brgy. Pilit Santa Fe, Leyte', 'Brgy. Pilit Santa Fe, Leyte', 'Student', 'Approved', '2026-05-12 09:29:15'),
(8, 6, 'APP-2026-0008', 'Reynald', 'Ampilong', 'Cabujoc', 'Jr.', 20, 'Male', '09203483127', 'sashafierce69@gmail.com', 'Brgy. Zone 1, San Miguel, Leyte', 'Brgy. Zone 1, San Miguel, Leyte', 'Student', 'Approved', '2026-05-13 05:31:55'),
(9, 6, 'APP-2026-0009', 'Jonalie ', 'Cerena', 'Montera', '', 19, 'Female', '09636385507', 'javellanajilliane032797@gmail.com', 'Brgy. Olot, Tolosa, Leyte', 'Brgy. Olot, Tolosa, Leyte', 'Student', 'For_Interview', '2026-05-13 05:44:21'),
(10, 6, 'APP-2026-0010', 'AIzee', 'Noveda', 'Javellana', '', 21, 'Female', '09639116956', 'jilliane061313@gmail.com', 'Brgy. Zone 2, Santa Fe, Leyte', 'Brgy. Zone 2, Santa Fe, Leyte', 'Employee', 'Pending', '2026-05-14 04:29:05'),
(11, 6, 'APP-2026-0011', 'Elizabeth', 'Rusiana', 'Sanico', '', 19, 'Female', '09123456788', 'maryelizabethsanico@gmail.com', 'Brgy. San Roque Tanauan, Leyte', 'Brgy. San Roque Tanauan, Leyte', 'Student', 'Pending', '2026-05-15 06:54:15');

-- --------------------------------------------------------

--
-- Table structure for table `application_period`
--

CREATE TABLE `application_period` (
  `period_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` enum('Open','Closed','Upcoming') NOT NULL DEFAULT 'Upcoming'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application_period`
--

INSERT INTO `application_period` (`period_id`, `name`, `start_date`, `end_date`, `status`) VALUES
(1, '1st Semester 2025-2026', '2026-01-01', '2026-03-31', 'Closed'),
(2, '2nd Semester 2025-2026', '2026-01-05', '2026-01-09', 'Closed'),
(3, '2nd Semester 2025-2026', '2026-01-05', '2026-01-09', 'Closed'),
(4, '2nd Semester 2025-2026', '2026-01-05', '2026-01-09', 'Closed'),
(5, '2nd Semester 2025-2026', '2026-01-05', '2026-01-09', 'Closed'),
(6, '1st Semester 2026-2027', '2026-08-03', '2026-08-07', 'Open');

-- --------------------------------------------------------

--
-- Table structure for table `beds_tb`
--

CREATE TABLE `beds_tb` (
  `bed_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `bed_number` varchar(11) NOT NULL,
  `status` enum('Available','Occupied') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `beds_tb`
--

INSERT INTO `beds_tb` (`bed_id`, `room_id`, `bed_number`, `status`) VALUES
(1, 1, '1', 'Available'),
(2, 1, '2', 'Occupied'),
(3, 1, '3', 'Available'),
(4, 1, '4', 'Available'),
(5, 2, '1', 'Occupied'),
(6, 2, '2', 'Available'),
(7, 2, '3', 'Available'),
(8, 2, '4', 'Available'),
(9, 2, '5', 'Available'),
(10, 2, '6', 'Available'),
(11, 3, '1', 'Occupied'),
(12, 3, '2', 'Available'),
(13, 3, '3', 'Available'),
(14, 3, '4', 'Available'),
(15, 3, '5', 'Available'),
(16, 3, '6', 'Available'),
(17, 1, '5', 'Available'),
(18, 1, '6', 'Available');

-- --------------------------------------------------------

--
-- Table structure for table `building_tb`
--

CREATE TABLE `building_tb` (
  `building_id` int(11) NOT NULL,
  `building_name` varchar(255) NOT NULL,
  `applicant_type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `building_tb`
--

INSERT INTO `building_tb` (`building_id`, `building_name`, `applicant_type`) VALUES
(1, 'Building A', 'Student'),
(2, 'Building B', 'Employee');

-- --------------------------------------------------------

--
-- Table structure for table `employee_info`
--

CREATE TABLE `employee_info` (
  `employee_id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `employee_number` varchar(50) NOT NULL,
  `department` varchar(100) NOT NULL,
  `position` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee_info`
--

INSERT INTO `employee_info` (`employee_id`, `application_id`, `employee_number`, `department`, `position`) VALUES
(1, 5, '101010', 'CAS', 'Teacher 1'),
(2, 6, '061313', 'Engineering ', 'Prompt Engineer'),
(3, 10, '26540', 'CAS', 'Nurse');

-- --------------------------------------------------------

--
-- Table structure for table `interview_sched`
--

CREATE TABLE `interview_sched` (
  `interview_id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `interview_date` date NOT NULL,
  `interview_time` time NOT NULL,
  `status` enum('Scheduled','Completed','No_Show') NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interview_sched`
--

INSERT INTO `interview_sched` (`interview_id`, `application_id`, `interview_date`, `interview_time`, `status`, `updated_at`) VALUES
(2, 2, '2026-05-08', '16:21:00', 'Completed', '2026-05-11 00:27:18'),
(4, 3, '2026-05-12', '10:00:00', 'Completed', '2026-05-07 22:22:43'),
(5, 5, '2026-05-11', '09:00:00', 'Completed', '2026-05-12 09:09:59'),
(6, 4, '2026-05-12', '17:16:00', 'Completed', '2026-05-12 06:24:38'),
(7, 6, '2026-05-12', '18:50:00', 'No_Show', '2026-05-12 08:26:01'),
(8, 7, '2026-05-13', '08:00:00', 'Completed', '2026-05-12 20:55:29'),
(18, 8, '2026-05-13', '15:00:00', 'Completed', '2026-05-13 05:57:30'),
(23, 9, '2026-05-14', '10:00:00', 'Scheduled', '2026-05-13 05:55:43');

-- --------------------------------------------------------

--
-- Table structure for table `payment_tb`
--

CREATE TABLE `payment_tb` (
  `payment_id` int(11) NOT NULL,
  `resident_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_date` datetime NOT NULL DEFAULT current_timestamp(),
  `status` enum('Pending','Paid') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment_tb`
--

INSERT INTO `payment_tb` (`payment_id`, `resident_id`, `amount`, `payment_date`, `status`) VALUES
(1, 9, 0.00, '2026-05-12 00:00:00', 'Paid'),
(2, 7, 0.00, '2026-05-12 00:00:00', 'Paid'),
(3, 8, 0.00, '2026-05-13 00:00:00', 'Paid'),
(4, 11, 0.00, '2026-05-13 00:00:00', 'Paid'),
(5, 12, 0.00, '2026-05-13 14:11:26', 'Pending');

-- --------------------------------------------------------

--
-- Table structure for table `requirements_tb`
--

CREATE TABLE `requirements_tb` (
  `requirement_id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_type` enum('ID','Enrollment','Employment') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `requirements_tb`
--

INSERT INTO `requirements_tb` (`requirement_id`, `application_id`, `file_name`, `file_type`) VALUES
(1, 2, '7fcf7eb8-d6e2-4e08-a317-42f7ce78cd67_chae.jpg', ''),
(2, 3, 'ad21f777-e5d3-4acd-bfd0-c038f79d88ea_ref.jpg', 'Enrollment'),
(3, 4, '433492da-7d36-43c8-b315-b141b129f49b_japanese koi.jpg', 'Enrollment'),
(4, 5, 'f9f7401f-78f2-4cc7-8c99-debeff0527d2_discord emoji emote side eye sideeye korean chinese meme doodle drawing_.jpg', 'Employment'),
(5, 6, '396ec9c9-08ec-4cca-9d4e-7d3aa92c1800_Loving Reflections_ Impasto Art Design.jpg', 'Employment'),
(6, 7, 'ee81e941-8a84-4a67-91a3-807d90687f66_Woman.jpg', 'Enrollment'),
(7, 8, 'd9fc1abc-324a-40aa-bf6e-9849fb9d48b7_Vanessa Foley _ Swans.jpg', 'Enrollment'),
(8, 9, 'c14f4e91-5d26-43c4-892b-d6bd7d5a6111_WIN_20241203_15_10_27_Pro.jpg', 'Enrollment'),
(9, 10, 'b42bcf38-ff8a-4764-9e12-70ab4dc0f3e3_WIN_20241203_12_32_35_Pro.jpg', 'Employment'),
(10, 11, 'a4c7ca1d-55cc-4b4c-8b71-ceda69e24bd8_download (7).jpg', 'Enrollment');

-- --------------------------------------------------------

--
-- Table structure for table `residents_tb`
--

CREATE TABLE `residents_tb` (
  `resident_id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `room_id` int(11) DEFAULT NULL,
  `bed_id` int(11) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'Active',
  `is_archived` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `residents_tb`
--

INSERT INTO `residents_tb` (`resident_id`, `application_id`, `room_id`, `bed_id`, `start_date`, `end_date`, `status`, `is_archived`) VALUES
(7, 2, NULL, NULL, '2026-05-12', '2026-05-13', 'Inactive', 1),
(8, 3, NULL, NULL, '2026-05-12', '2026-05-13', 'Inactive', 1),
(9, 4, NULL, 2, '2026-05-12', NULL, 'Active', 0),
(10, 5, NULL, 11, '2026-05-12', NULL, 'Active', 0),
(11, 7, NULL, 5, '2026-05-13', NULL, 'Active', 0),
(12, 8, NULL, NULL, '2026-05-13', '2026-05-14', 'Inactive', 1);

-- --------------------------------------------------------

--
-- Table structure for table `rooms_tb`
--

CREATE TABLE `rooms_tb` (
  `room_id` int(11) NOT NULL,
  `building_id` int(11) NOT NULL,
  `room_number` int(11) NOT NULL,
  `capacity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms_tb`
--

INSERT INTO `rooms_tb` (`room_id`, `building_id`, `room_number`, `capacity`) VALUES
(1, 1, 1, 6),
(2, 1, 2, 6),
(3, 2, 1, 6);

-- --------------------------------------------------------

--
-- Table structure for table `student_info`
--

CREATE TABLE `student_info` (
  `student_id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `student_number` varchar(50) NOT NULL,
  `program` varchar(100) NOT NULL,
  `year_level` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_info`
--

INSERT INTO `student_info` (`student_id`, `application_id`, `student_number`, `program`, `year_level`) VALUES
(1, 2, '2402451', 'BSIT', 2),
(2, 3, '2401234', 'BSIT', 2),
(3, 4, '2402015', 'BSIT', 2),
(4, 7, '2401234', 'BSIT', 2),
(5, 8, '2402015', 'BSIT', 2),
(6, 9, '2402547', 'BSIT', 2),
(7, 11, '2403375', 'Bsit', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_log`
--
ALTER TABLE `activity_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin_tb`
--
ALTER TABLE `admin_tb`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `applications_tb`
--
ALTER TABLE `applications_tb`
  ADD PRIMARY KEY (`application_id`),
  ADD UNIQUE KEY `unique_applicant_period` (`applicant_number`,`period_id`),
  ADD KEY `period_id` (`period_id`);

--
-- Indexes for table `application_period`
--
ALTER TABLE `application_period`
  ADD PRIMARY KEY (`period_id`);

--
-- Indexes for table `beds_tb`
--
ALTER TABLE `beds_tb`
  ADD PRIMARY KEY (`bed_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `building_tb`
--
ALTER TABLE `building_tb`
  ADD PRIMARY KEY (`building_id`);

--
-- Indexes for table `employee_info`
--
ALTER TABLE `employee_info`
  ADD PRIMARY KEY (`employee_id`),
  ADD KEY `application_id` (`application_id`);

--
-- Indexes for table `interview_sched`
--
ALTER TABLE `interview_sched`
  ADD PRIMARY KEY (`interview_id`),
  ADD UNIQUE KEY `unique_application` (`application_id`),
  ADD KEY `application_id` (`application_id`);

--
-- Indexes for table `payment_tb`
--
ALTER TABLE `payment_tb`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `resident_id` (`resident_id`);

--
-- Indexes for table `requirements_tb`
--
ALTER TABLE `requirements_tb`
  ADD PRIMARY KEY (`requirement_id`),
  ADD KEY `application_id` (`application_id`);

--
-- Indexes for table `residents_tb`
--
ALTER TABLE `residents_tb`
  ADD PRIMARY KEY (`resident_id`),
  ADD KEY `application_id` (`application_id`),
  ADD KEY `room_id` (`room_id`),
  ADD KEY `bed_id` (`bed_id`);

--
-- Indexes for table `rooms_tb`
--
ALTER TABLE `rooms_tb`
  ADD PRIMARY KEY (`room_id`),
  ADD KEY `building_id` (`building_id`);

--
-- Indexes for table `student_info`
--
ALTER TABLE `student_info`
  ADD PRIMARY KEY (`student_id`),
  ADD KEY `application_id` (`application_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_log`
--
ALTER TABLE `activity_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `admin_tb`
--
ALTER TABLE `admin_tb`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `applications_tb`
--
ALTER TABLE `applications_tb`
  MODIFY `application_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `application_period`
--
ALTER TABLE `application_period`
  MODIFY `period_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `beds_tb`
--
ALTER TABLE `beds_tb`
  MODIFY `bed_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `building_tb`
--
ALTER TABLE `building_tb`
  MODIFY `building_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `employee_info`
--
ALTER TABLE `employee_info`
  MODIFY `employee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `interview_sched`
--
ALTER TABLE `interview_sched`
  MODIFY `interview_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `payment_tb`
--
ALTER TABLE `payment_tb`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `requirements_tb`
--
ALTER TABLE `requirements_tb`
  MODIFY `requirement_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `residents_tb`
--
ALTER TABLE `residents_tb`
  MODIFY `resident_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `rooms_tb`
--
ALTER TABLE `rooms_tb`
  MODIFY `room_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `student_info`
--
ALTER TABLE `student_info`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `applications_tb`
--
ALTER TABLE `applications_tb`
  ADD CONSTRAINT `applications_tb_ibfk_1` FOREIGN KEY (`period_id`) REFERENCES `application_period` (`period_id`) ON UPDATE CASCADE;

--
-- Constraints for table `beds_tb`
--
ALTER TABLE `beds_tb`
  ADD CONSTRAINT `beds_tb_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms_tb` (`room_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `employee_info`
--
ALTER TABLE `employee_info`
  ADD CONSTRAINT `employee_info_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications_tb` (`application_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `interview_sched`
--
ALTER TABLE `interview_sched`
  ADD CONSTRAINT `interview_sched_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications_tb` (`application_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `payment_tb`
--
ALTER TABLE `payment_tb`
  ADD CONSTRAINT `payment_tb_ibfk_1` FOREIGN KEY (`resident_id`) REFERENCES `residents_tb` (`resident_id`) ON UPDATE CASCADE;

--
-- Constraints for table `requirements_tb`
--
ALTER TABLE `requirements_tb`
  ADD CONSTRAINT `requirements_tb_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications_tb` (`application_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `residents_tb`
--
ALTER TABLE `residents_tb`
  ADD CONSTRAINT `residents_tb_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications_tb` (`application_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `residents_tb_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms_tb` (`room_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `residents_tb_ibfk_3` FOREIGN KEY (`bed_id`) REFERENCES `beds_tb` (`bed_id`) ON UPDATE CASCADE;

--
-- Constraints for table `rooms_tb`
--
ALTER TABLE `rooms_tb`
  ADD CONSTRAINT `rooms_tb_ibfk_1` FOREIGN KEY (`building_id`) REFERENCES `building_tb` (`building_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `student_info`
--
ALTER TABLE `student_info`
  ADD CONSTRAINT `student_info_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applications_tb` (`application_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
