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
  `is_superuser` tinyint(1) DEFAULT 1,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `is_staff` tinyint(1) DEFAULT 1,
  `is_active` tinyint(1) DEFAULT 1,
  `date_joined` datetime(6) DEFAULT NULL,
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
  `ip` char(20) NOT NULL COMMENT '节点ip',
  `androidConnect` tinyint(1) NOT NULL DEFAULT '0',
  `port` char(10) NOT NULL DEFAULT '3456' COMMENT '节点端口',
  `status` int(2) DEFAULT '1',
  `ext_info` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;

/*Table structure for table `test_keyword` */

DROP TABLE IF EXISTS `test_keyword`;

CREATE TABLE `test_keyword` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `keyword` char(20) NOT NULL COMMENT '关键字',
  `paraCount` int(10) NOT NULL DEFAULT '1' COMMENT '参数数量',
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

insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('前往','1','driver.get(\"$para1\")',NULL,'前往|http://www.baidu.com','浏览器跳转到指定地址。    注：需要输入http 前缀','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('点击','2','extend.extend().find_element(driver,[\"$para1\",\"$para2\"]).click()','driver.element_by_$para1(\"$para2\")','点击|id@@searchBtn','点击页面元素','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('等待','1','extend.extend().wait($para1)',NULL,'等待|5','手动加入等待时间','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('点击菜单','1','extend.extend().click_menu(driver, \"$para1\")','driver.element_by_partial_link_text(\"$para1\")','点击菜单|系统管理','通过菜单文字点击菜单','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('点击文字','1','extend.extend().click_menu(driver, \"$para1\")','driver.element_by_partial_link_text(\"$para1\")','点击文字|查询','通过文本内容，快速点击元素。   适用于文字链接、按钮等元素。','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('悬浮点击','2','driver.find_element_by_$para1(\"$para2\").click()','driver.element_by_$para1(\"$para2\")','悬浮点击|id@@searchBtn\r\ndriver.find_element_by_id(\"searchBtn\").click()','点击页面元素，可按 id、css、xpath 等方式定位元素。 同 点击','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('选择','4','extend.extend().select(driver,[\"$para1\",\"$para2\",\"$para3\",\"$para4\"])','driver.element_by_$para1(\"$para2\")','选择|id@@selectBox@@index@@1；选择|id@@selectBox@@text@@中国','选择下拉框中指定的选项。 可按 index、value、 text（完全匹配）、text_part（模糊匹配） 等信息选择选项','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('验证','1','extend.extend().assert_text(driver, \"$para1\")',NULL,'验证|成功','验证页面中是否包含预期文字','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('验证文字','3','extend.extend().assert_element_text(driver, [\"$para1\",\"$para2\",\"$para3\"])',NULL,'验证文字|id@@text@@成功','验证指定元素中是否包含预期的文字信息。  如验证提示是否包含“成功”','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('截图','1','extend.extend().screenshot(driver,id,screenFileList)',NULL,'截图','手动截图。 注：用例执行失败时会自动截图。','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('填写日期','3','extend.extend().fill_on_date(driver,[\"$para1\",\"$para2\",\"$para3\"])','driver.element_by_$para1(\"$para2\")','填写日期|id@@start_date@@2018-04-01','在指定元素中输入日期。         ps：此方法会去除元素的 readonly 属性，达到跳过手动选择日期，快速输入的目的','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('返回','1','driver.back()',NULL,'返回','浏览器后退。','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('点击索引','3','extend.extend().click_index(driver,[\"$para1\",\"$para2\",\"$para3\"])','driver.element_by_$para1(\"$para2\")','点击索引|id@@addBtn@@0','当匹配到的页面元素有多个时可按index 索引选择要点击的元素。','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('切换','2','extend.extend().switchIframe(driver,[\"$para1\",\"$para2\"])',NULL,'切换|id@@iframe1','页面中包含iframe 时，需要调用该方法进行切换，否则无法定位其他iframe的元素。','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('滑动到底部','1','driver.execute_script(\"window.scrollTo(0,document.body.scrollHeight)\")',NULL,'滑动到底部','滑动页面到最底','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('反选','1','extend.extend().uncheck_checkbox(driver)',NULL,'反选','特别封装步骤，用于取消已选择的选项。（用于 mt-checkbox 类型的选择框）','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('验证文字非','3','extend.extend().assert_element_text(driver, [\"$para1\",\"$para2\",\"$para3\"], isNot=True)',NULL,'验证文字非|id@@text','验证指定元素中是否不包含预期的文字信息。  如验证提示是否不包含“成功”','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('切换主页','1','driver.switch_to_default_content()',NULL,'切换主页','从iframe中切换回主页面','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('刷新','1','driver.refresh()',NULL,'刷新','浏览器后退。','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('填写1','3','driver.find_element_by_$para1(\"$para2\").send_keys(\"$para3\")','driver.element_by_$para1(\"$para2\")','填写|id@@input_box@@ghw','在指定元素中输入文字。不清除原已输入的值。','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('尝试点击','2','extend.extend().try_click(driver,[\"$para1\",\"$para2\"])','driver.element_by_$para1(\"$para2\")','尝试点击|id@@searchBtn','尝试点击页面元素，如果点击失败，则跳过。','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('填写','3','extend.extend().fill(driver,[\"$para1\",\"$para2\"],\"$para3\")','driver.element_by_$para1(\"$para2\")','填写|id@@input_box@@ghw','在指定元素中输入文字，可按 id、css、xpath、class、name、text 等方式定位元素','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('选择全部','2','extend.extend().select_all(driver,[\"$para1\",\"$para2\"])','driver.element_by_$para1(\"$para2\")','选择全部|id@@select','对下拉框，选择所有选项','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('点击全部','2','extend.extend().check_all(driver,[\"$para1\",\"$para2\"])','driver.element_by_$para1(\"$para2\")','点击全部|id@@CheckBox','对多选框，选择所有选项','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('切换窗口','1','extend.extend().switchWindow(driver)',NULL,'切换窗口','当浏览器弹出新的窗口时，切换到另一个窗口进行操作','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('验证标题','1','extend.extend().assert_title(driver,"$para1")',NULL,'验证标题|百度地图','验证页面的title中是否包含预期文字','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('Chrome','1','Chrome',NULL,'Chrome','初始化Chrome 浏览器','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('公共方法','1','	$para1',NULL,'公共方法|游客登录','调用公共方法','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('填写文件','3','extend.extend().fill_file(driver,[\"$para1\",\"$para2\"],\"$para3\")','driver.element_by_$para1(\"$para2\")','填写文件|id@@input_box@@ghw','在指定元素中输入文件路径，可按 id、css、xpath、class、name、text 等方式定位元素','1');
insert into `test_keyword` ( `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('复制','4','extend.extend().copy_from_another_element(driver,[\"$para1\",\"$para2\"],[\"$para3\",\"$para4\"])','driver.element_by_$para1(\"$para2\")','复制|id@@kw@@id@@su','将后一个元素的内容复制填入到前一个元素中','1');



/*Table structure for table `api_new` */

DROP TABLE IF EXISTS `api_new`;

CREATE TABLE `api_new` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product` char(20) NOT NULL DEFAULT 'SDK' COMMENT 'SDK/CG',
  `module` char(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` char(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `url` char(50) NOT NULL,
  `paras` text NOT NULL,
  `osign_list` char(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `description` char(50) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1' COMMENT '1:正常， 0：已删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `test_minder`;

CREATE TABLE `test_minder` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT 'defaultname',
  `module` varchar(50) DEFAULT 'defaultmodule',
  `description` varchar(50) DEFAULT NULL,
  `content` text,
  `batchId` char(40) DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
