from app.core import log
import string
from app import useDB

class keywords(object):
    def __init__(self):
        self.keywords = [
    {'index': '前往', 'paraCount': 1, 'template': 'driver.get("http://$para1")'},
    {'index': '点击', 'paraCount': 2, 'template':'driver.element_by_$para1("$para2").click()'},
    {'index': '填写', 'paraCount': 3, 'template': 'driver.element_by_$para1("$para2").send_keys("$para3")'},
    {'index': '等待', 'paraCount': 1, 'template': 'time.sleep($para1)'},
    {'index': '点击菜单', 'paraCount': 1, 'template': 'driver.element_by_partial_link_text("$para1").click()'},
    {'index': '点击文字', 'paraCount': 1, 'template': 'driver.element_by_partial_link_text("$para1").click()'},
    {'index': '悬浮点击', 'paraCount': 2, 'template':'driver.element_by_$para1("$para2").click()'},
    {'index': '选择', 'paraCount': 4, 'template': 'Select(driver.element_by_$para1("$para2")).select_by_$para3("$para4")'},
    {'index': '验证', 'paraCount': 1, 'template': 'time.sleep(1)'},
    {'index': '验证文字', 'paraCount': 3, 'template': 'result1=(driver.element_by_$para1("$para2").text)'},
    {'index': '截图', 'paraCount': 1, 'template': 'driver.save_screenshot("%s"  %$para1)'}
    ]

    def getPara1(self, keyword):
        # print(self.keywords)
        keywords = self.keywords
        result = 0
        log.log().logger.info(keyword)
        for list in keywords:
            if list['index']==keyword:
                result =1
                return list['paraCount'], list['template']
                break
        if result ==0:
            return '',''

    def getPara(self, keyword):
        result = 0
        # log.log().logger.info(keyword)
        sql = string.Template(
            "select paraCount, template, elementTemplate from `test_keyword` where `keyword`= '$index' limit 1;")
        sql = sql.substitute(index=keyword)
        result = useDB.useDB().search(sql)
        if len(result):
            return result[0][0], result[0][1],result[0][2]
        else:
            return '','',''
