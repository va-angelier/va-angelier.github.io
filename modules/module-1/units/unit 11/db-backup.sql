/*M!999999\- enable the sandbox mode */
-- MariaDB dump 10.19-11.6.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: company1
-- ------------------------------------------------------
-- Server version	11.6.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `dept`
--

DROP TABLE IF EXISTS `dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dept` (
                        `DEPTNO` int(11) NOT NULL AUTO_INCREMENT,
                        `DNAME` varchar(155) DEFAULT NULL,
                        `LOC` varchar(155) DEFAULT NULL,
                        PRIMARY KEY (`DEPTNO`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dept`
--

LOCK TABLES `dept` WRITE;
/*!40000 ALTER TABLE `dept` DISABLE KEYS */;
INSERT INTO `dept` VALUES
                       (10,'ACCOUNTING','NEW YORK'),
                       (20,'RESEARCH','DALLAS'),
                       (30,'SALES','CHICAGO');
/*!40000 ALTER TABLE `dept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emp`
--

DROP TABLE IF EXISTS `emp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emp` (
                       `EMPNO` int(11) NOT NULL AUTO_INCREMENT,
                       `ENAME` varchar(155) DEFAULT NULL,
                       `JOB` varchar(155) DEFAULT NULL,
                       `MGR` int(11) DEFAULT NULL,
                       `HIREDATE` date DEFAULT NULL,
                       `SAL` decimal(10,2) DEFAULT 0.00,
                       `COM` decimal(10,2) DEFAULT 0.00,
                       `DEPTNO` int(11) DEFAULT NULL,
                       PRIMARY KEY (`EMPNO`),
                       KEY `idxMGR` (`MGR`,`EMPNO`),
                       KEY `idxDEP` (`DEPTNO`,`EMPNO`),
                       CONSTRAINT `depNumber` FOREIGN KEY (`DEPTNO`) REFERENCES `dept` (`DEPTNO`) ON DELETE SET NULL ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7935 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emp`
--

LOCK TABLES `emp` WRITE;
/*!40000 ALTER TABLE `emp` DISABLE KEYS */;
INSERT INTO `emp` VALUES
                      (7369,'SMITH','CLERK',7902,'1980-12-17',800.00,NULL,20),
                      (7499,'ALLEN','SALESMAN',7698,'1981-02-20',1600.00,300.00,30),
                      (7521,'WARD','SALESMAN',7698,'1981-02-22',1250.00,500.00,30),
                      (7566,'JONES','MANAGER',7839,'1981-04-02',2975.00,NULL,20),
                      (7654,'MARTIN','SALESMAN',7698,'1981-09-28',1250.00,1400.00,30),
                      (7698,'BLAKE','MANAGER',7839,'1981-05-01',2850.00,NULL,30),
                      (7782,'CLARK','MANAGER',7839,'1981-06-09',2450.00,NULL,10),
                      (7788,'SCOTT','ANALYST',7566,'1987-04-19',3000.00,NULL,20),
                      (7839,'KING','PRESIDENT',NULL,'1981-11-17',5000.00,NULL,10),
                      (7844,'TURNER','SALESMAN',7698,'1981-09-08',1500.00,0.00,30),
                      (7876,'ADAMS','CLERK',7788,'1987-05-23',1100.00,NULL,20),
                      (7900,'JAMES','CLERK',7698,'1981-12-03',950.00,NULL,30),
                      (7902,'FORD','ANALYST',7566,'1981-12-03',3000.00,NULL,20),
                      (7934,'MILLER','CLERK',7782,'1982-01-23',1300.00,NULL,10);
/*!40000 ALTER TABLE `emp` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-04-02 13:11:32
