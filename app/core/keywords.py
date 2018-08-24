from app.core import log
import string
from app import useDB

class keywords(object):

    def getPara(self, keyword):
        result = 0
        log.log().logger.info(keyword)
        sql = string.Template(
            "select paraCount, template, elementTemplate from `test_keyword` where `keyword`= '$index' limit 1;")
        sql = sql.substitute(index=keyword)
        result = useDB.useDB().search(sql)
        if len(result):
            return result[0][0], result[0][1],result[0][2]
        else:
            return '','',''
