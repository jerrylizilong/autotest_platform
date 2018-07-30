/*
SQLyog Community v11.2 Beta1 (32 bit)
MySQL - 5.6.23 : Database - test_auto
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
--CREATE DATABASE /*!32312 IF NOT EXISTS*/`test_auto_new` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `test_auto_new`;

/*Table structure for table `auth_user` */

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Table structure for table `test_batch` */

insert into auth_user (`password`,email,username,is_superuser,first_name,last_name,is_staff,is_active,date_joined) values('cfcd208495d565ef66e7dff9f98764da','admin','admin',1,'admin','admin',1,1,'2018-07-01');


DROP TABLE IF EXISTS `test_batch`;

CREATE TABLE `test_batch` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `test_suite_id` bigint(10) NOT NULL,
  `test_case_id` bigint(10) NOT NULL,
  `name` tinytext,
  `status` int(2) DEFAULT '0' COMMENT '0:待执行；1：执行成功；2：执行失败 3：执行中',
  `steps` text,
  `runtime` datetime DEFAULT NULL,
  `message` text,
  `screenshot` longtext,
  `module` char(20) DEFAULT NULL,
  `ip` varchar(50) DEFAULT NULL,
  `browser_type` varchar(50) DEFAULT 'Chrome',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21852 DEFAULT CHARSET=utf8;

/*Table structure for table `test_case` */

DROP TABLE IF EXISTS `test_case`;

CREATE TABLE `test_case` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `isPublicFunction` tinyint(1) NOT NULL DEFAULT '0',
  `module` varchar(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `steps` text,
  `description` varchar(50) DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=648 DEFAULT CHARSET=utf8;

/*Table structure for table `test_config` */

DROP TABLE IF EXISTS `test_config`;

CREATE TABLE `test_config` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `value` varchar(100) DEFAULT NULL,
  `isUseAble` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Table structure for table `test_hubs` */

DROP TABLE IF EXISTS `test_hubs`;

CREATE TABLE `test_hubs` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `ip` char(20) NOT NULL COMMENT '关键字',
  `androidConnect` tinyint(1) NOT NULL DEFAULT '0',
  `port` char(10) NOT NULL DEFAULT '3456' COMMENT '参数长度',
  `status` int(2) DEFAULT '1',
  `ext_info` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;

/*Table structure for table `test_keyword` */

DROP TABLE IF EXISTS `test_keyword`;

CREATE TABLE `test_keyword` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `keyword` char(20) NOT NULL COMMENT '关键字',
  `paraCount` int(10) NOT NULL DEFAULT '1' COMMENT '参数长度',
  `status` int(1) DEFAULT '1',
  `template` longtext NOT NULL COMMENT '模板，如：driver.element_by_partial_link_text("$para1").click()',
  `elementTemplate` longtext,
  `example` longtext,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

/*Table structure for table `test_run_list` */

DROP TABLE IF EXISTS `test_run_list`;

CREATE TABLE `test_run_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` char(20) DEFAULT 'test_suite',
  `relateId` int(11) DEFAULT NULL,
  `status` int(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Table structure for table `test_suite` */

DROP TABLE IF EXISTS `test_suite`;

CREATE TABLE `test_suite` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `name` char(50) DEFAULT 'null',
  `status` int(2) NOT NULL DEFAULT '-1' COMMENT '0:待执行；1：执行成功；2：执行失败 3：执行中',
  `run_type` char(20) DEFAULT 'Chrome' COMMENT '0：Chrome 1：IE 2：Firefox 3：remote 4：all',
  `description` char(100) DEFAULT NULL,
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0',
  `runCount` int(10) DEFAULT '0',
  `relateCaseId` bigint(20) DEFAULT NULL,
  `batchId` char(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=381 DEFAULT CHARSET=utf8;

/*Table structure for table `unittest_record` */

DROP TABLE IF EXISTS `unittest_record`;

CREATE TABLE `unittest_record` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL DEFAULT 'unittest',
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `file_name` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
