from app import useDB
from app.db import test_batch_manage
class test_task_manage():
    def test_suite_list(self,runtype='2'):
        sql = 'select id,run_type from test_suite where status in (0,2) and isDeleted = 0 and run_type = "%s";' %runtype
        idList = useDB.useDB().search(sql)
        return idList

    def test_case_list(self,isATX=False):
        if isATX:
            sql = 'select t1.id, t1.steps,t1.browser_type from test_batch t1, test_case t2 where t1.status in (0) and t1.test_case_id=t2.id and t2.module="android";'
        else:
            sql = 'select t1.id, t1.steps,t1.browser_type from test_batch t1, test_case t2 where t1.status in (0) and t1.test_case_id=t2.id and t2.module !="android";'
        idList = useDB.useDB().search(sql)
        return idList

    def update_test_suite(self, relateId,status):
        import string
        sql = string.Template('update test_suite set status = $status, runCount = runCount+1  where id = "$relateId";')
        sql = sql.substitute(relateId = relateId,status=status)
        useDB.useDB().insert(sql)

    def update_test_suite_check(self):
        check_list,test_suite_list = test_batch_manage.test_batch_manage().search_done_test_suite()
        # print(check_list,test_suite_list)
        if len(check_list):
            sql = 'update test_suite set status = 1  where id in (%s);' %check_list
            useDB.useDB().insert(sql)
            from app import config
            if config.is_email_enable:
                from app.util import sendEmail
                sendEmail.sendEmail().send_test_results(test_suite_list)