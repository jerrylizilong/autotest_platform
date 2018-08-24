from app import useDB,log
import string

class test_user_manage:

    def checklogin(self,username,password):
        sql = 'select id,username from  auth_user where 1=1 and  username=%s and password=%s'
        args = (username,password)
        list = useDB.useDB().searchsql(sql,args)
        results=[]
        for i in range(len(list)):
            result = {}
            result['id'] = list[i][0]
            result['username'] = list[i][1]
            results.append(result)
        return results

    def show_users(self,username):
        results = []
        if username=='':
            sql = 'select id, username from auth_user order by id desc ;'
        else:
            sql = 'select id, username from auth_user where username like "%' + username + '%" order by id desc;'
        users = useDB.useDB().search(sql)
        for i in range(len(users)):
            result = {}
            result['id'] = users[i][0]
            result['username'] = users[i][1]
            results.append(result)
        # print(results)
        return results

    def new_user(self, username,password):
        users = self.show_users(username)
        if len(users):
            return 0
        else:
            sql = 'insert into auth_user (username,password) values ("%s","%s");' %(username,password)
            # print(sql)
            useDB.useDB().insert(sql)
            return 1

    def update_user_password(self, id, fieldlist, valueList):
        update_value = '%s = "%s"' % (fieldlist[0], valueList[0])
        for i in range(1, len(fieldlist)):
            update_value += ', %s = "%s"' % (fieldlist[i], valueList[i])
        sql = string.Template('update auth_user set $field where id = "$id";')
        sql = sql.substitute(field=update_value, id=id)
        useDB.useDB().insert(sql)

