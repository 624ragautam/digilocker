SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";



CREATE TABLE `external_user` (
  `euid` int(11) NOT NULL,
  `euname` varchar(20) NOT NULL,
  `eukey` varchar(20) NOT NULL,
  `fid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `attendence`
--

-- INSERT INTO `attendence` (`aid`, `rollno`, `attendance`) VALUES
-- (6, '1ve17cs012', 98);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

-- CREATE TABLE `department` (
--   `cid` int(11) NOT NULL,
--   `branch` varchar(50) NOT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --
-- -- Dumping data for table `department`
-- --

-- INSERT INTO `department` (`cid`, `branch`) VALUES
-- (2, 'Information Science'),
-- (3, 'Electronic and Communication'),
-- (4, 'Electrical & Electronic'),
-- (5, 'Civil '),
-- (7, 'computer science'),
-- (8, 'IOT');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `file` (
  `file_id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `fsize` varchar(50) NOT NULL,
  `ftype` varchar(50) NOT NULL,
  `data` varchar(50) NOT NULL,
  `lock` varchar(2000) NOT NULL,
  `email` varchar(50) NOT NULL,
  `description` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `student`
--
DELIMITER $$
CREATE TRIGGER `DELETE` BEFORE DELETE ON `file` FOR EACH ROW INSERT INTO history VALUES(null,OLD.file_id,OLD.fname,OLD.email,'FILE DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Insert` AFTER INSERT ON `file` FOR EACH ROW INSERT INTO history VALUES(null,NEW.file_id,NEW.fname,NEW.email,'FILE INSERTED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `UPDATE` AFTER UPDATE ON `file` FOR EACH ROW INSERT INTO history VALUES(null,NEW.file_id,NEW.fname,NEW.email,'FILE UPDATED',NOW())
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `username` varchar(52) NOT NULL,
  `email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`id`, `username`, `email`) VALUES
(1, 'aaa', 'aaa@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `trig`
--

CREATE TABLE `history` (
  `tid` int(11) NOT NULL,
  `fid` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `uname` varchar(50) NOT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trig`
--

-- INSERT INTO `trig` (`tid`, `rollno`, `action`, `timestamp`) VALUES
-- (7, '1ve17cs012', 'STUDENT INSERTED', '2021-01-10 19:19:56'),
-- (8, '1ve17cs012', 'STUDENT UPDATED', '2021-01-10 19:20:31'),
-- (9, '1ve17cs012', 'STUDENT DELETED', '2021-01-10 19:21:23');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--


--
-- Dumping data for table `user`
--

-- INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
-- (4, 'anees', 'anees@gmail.com', 'pbkdf2:sha256:150000$1CSLss89$ef995dfc48121768b2070bfbe7a568871cd56fac85ac7c95a1e645c8806146e9');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendence`
--


--
-- Indexes for table `department`
--


--
-- Indexes for table `student`
--
ALTER TABLE `file`
  ADD PRIMARY KEY (`file_id`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trig`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`tid`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `external_user`
  ADD PRIMARY KEY (`euid`);

--
-- AUTO_INCREMENT for dumped tables
--

--

--

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `file`
  MODIFY `file_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;



--
-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `trig`
--
ALTER TABLE `history`
  MODIFY `tid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;


ALTER TABLE `external_user`
  MODIFY `euid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

-- /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
-- /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
-- /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
