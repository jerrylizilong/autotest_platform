/*
SQLyog Community v11.2 Beta1 (32 bit)
MySQL - 5.6.23 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `test_keyword` (
	`id` int (10),
	`keyword` char (60),
	`paraCount` int (10),
	`template` text ,
	`elementTemplate` text ,
	`example` text ,
	`description` text ,
	`status` int (11)
); 
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('1','前往','1','driver.get(\"$para1\")',NULL,'前往|http://www.baidu.com','浏览器跳转到指定地址。    注：需要输入http 前缀','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('2','点击','2','extend.extend().find_element(driver,[\"$para1\",\"$para2\"]).click()','driver.element_by_$para1(\"$para2\")','点击|id@@searchBtn','点击页面元素','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('4','等待','1','extend.extend().wait($para1)',NULL,'等待|5','手动加入等待时间','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('5','点击菜单','1','extend.extend().click_menu(driver, \"$para1\")','driver.element_by_partial_link_text(\"$para1\")','点击菜单|系统管理','通过菜单文字点击菜单','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('6','点击文字','1','extend.extend().click_menu(driver, \"$para1\")','driver.element_by_partial_link_text(\"$para1\")','点击文字|查询','通过文本内容，快速点击元素。   适用于文字链接、按钮等元素。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('7','悬浮点击','2','driver.find_element_by_$para1(\"$para2\").click()','driver.element_by_$para1(\"$para2\")','悬浮点击|id@@searchBtn\r\ndriver.find_element_by_id(\"searchBtn\").click()','点击页面元素，可按 id、css、xpath 等方式定位元素。 同 点击','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('8','选择','4','extend.extend().select(driver,[\"$para1\",\"$para2\",\"$para3\",\"$para4\"])','driver.element_by_$para1(\"$para2\")','选择|id@@selectBox@@index@@1；选择|id@@selectBox@@text@@中国','选择下拉框中指定的选项。 可按 index、value、 text（完全匹配）、text_part（模糊匹配） 等信息选择选项','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('9','验证','1','$para1',NULL,'验证|成功','验证页面中是否包含预期文字','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('10','验证文字','3','$para1,$para2,$para3',NULL,'验证文字|id@@text@@成功','验证指定元素中是否包含预期的文字信息。  如验证提示是否包含“成功”','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('11','截图','1','extend.extend().screenshot(driver,id,screenFileList)',NULL,'截图','手动截图。 注：用例执行失败时会自动截图。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('12','填写日期','3','extend.extend().fill_on_date(driver,[\"$para1\",\"$para2\",\"$para3\"])','driver.element_by_$para1(\"$para2\")','填写日期|id@@start_date@@2018-04-01','在指定元素中输入日期。         ps：此方法会去除元素的 readonly 属性，达到跳过手动选择日期，快速输入的目的','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('13','返回','1','driver.back()',NULL,'返回','浏览器后退。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('14','发送','1','extend.extend().sendData(driver, \"$para1\")',NULL,'发送','特别封装步骤，用于Android 的批量数据收集方法。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('15','点击索引','3','extend.extend().click_index(driver,[\"$para1\",\"$para2\",\"$para3\"])','driver.element_by_$para1(\"$para2\")','点击索引|id@@addBtn@@0','当匹配到的页面元素有多个时可按index 索引选择要点击的元素。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('16','切换','2','extend.extend().switchIframe(driver,[\"$para1\",\"$para2\"])',NULL,'切换|id@@iframe1','页面中包含iframe 时，需要调用该方法进行切换，否则无法定位其他iframe的元素。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('17','发送H5','1','extend.extend().sendH5Data(driver)',NULL,'发送H5','特别封装步骤，用于 H5 demo 的批量数据收集方法。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('18','滑动到底部','1','driver.execute_script(\"window.scrollTo(0,document.body.scrollHeight)\")',NULL,'滑动到底部','滑动页面到最底','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('19','反选','1','extend.extend().uncheck_checkbox(driver)',NULL,'反选','特别封装步骤，用于取消已选择的选项。（用于 mt-checkbox 类型的选择框）','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('20','验证文字非','3','$para1,$para2,$para3',NULL,'验证文字非|id@@text','验证指定元素中是否不包含预期的文字信息。  如验证提示是否不包含“成功”','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('21','切换主页','1','driver.switch_to_default_content()',NULL,'切换主页','从iframe中切换回主页面','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('22','刷新','1','driver.refresh()',NULL,'刷新','浏览器后退。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('23','填写1','3','driver.find_element_by_$para1(\"$para2\").send_keys(\"$para3\")','driver.element_by_$para1(\"$para2\")','填写|id@@input_box@@ghw','在指定元素中输入文字。不清除原已输入的值。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('24','尝试点击','2','extend.extend().try_click(driver,[\"$para1\",\"$para2\"])','driver.element_by_$para1(\"$para2\")','尝试点击|id@@searchBtn','尝试点击页面元素，如果点击失败，则跳过。','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('25','填写','3','extend.extend().find_element(driver,[\"$para1\",\"$para2\"]).clear()\r\nextend.extend().find_element(driver,[\"$para1\",\"$para2\"]).send_keys(\"$para3\")','driver.element_by_$para1(\"$para2\")','填写|id@@input_box@@ghw','在指定元素中输入文字，可按 id、css、xpath、class、name、text 等方式定位元素','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('26','选择全部','2','extend.extend().select_all(driver,[\"$para1\",\"$para2\"])','driver.element_by_$para1(\"$para2\")','选择全部|id@@select','对下拉框，选择所有选项','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('27','点击全部','2','extend.extend().check_all(driver,[\"$para1\",\"$para2\"])','driver.element_by_$para1(\"$para2\")','点击全部|id@@CheckBox','对多选框，选择所有选项','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('28','切换窗口','1','extend.extend().switchWindow(driver)',NULL,'切换窗口','当浏览器弹出新的窗口时，切换到另一个窗口进行操作','1');
insert into `test_keyword` (`id`, `keyword`, `paraCount`, `template`, `elementTemplate`, `example`, `description`, `status`) values('29','切换应用','1','extend.extend().switchApp(driver,\"$para1\")',NULL,'切换应用|testLogin','页面中包含iframe 时，需要调用该方法进行切换，否则无法定位其他iframe的元素。','1');
