appKey = 'abc'

class api_manage():

    def build_api_url(self,api_info,osign_list,type='default',host_id=''):
        """
        Build test url for given api info.

        :param api_info:  json data with api info.
        :param osign_list: The list for paras to be reogin.
        :param type:  by default , first value will be selected for para.  If type is set to be random , a random value will be selected from paras.py file.
        :param host_id: the host you want to test with.
            0: 53
            1:product
            2:product cn
            3:sdk-test1
            4:sdk-test1 cn
        :return:  the final url.
        """
        para_info = self.get_para_info(api_info,osign_list,type=type)
        if host_id =='':
            host = api_info['url']['host']
        else:
            from app.api_new import paras
            host = getattr(paras.paraValues(), 'sdkHosts')[host_id]
        url = host+api_info['url']['url']+'?'+self.dict_2_str(para_info)
        return url

    def split_api_info(self,example_url):
        """
        This function will split all infomation from a given url, including host, url path,paras.

        :param
        """
        api_url,para_url = example_url.split('?')
        paras = para_url.split('&')
        para_list = {}
        for para in paras:
            para_name,value = para.split('=')
            para_list[para_name]=value
        api_info = {}
        api_info['url']=self.split_url_info(api_url)
        api_info['paras']=para_list
        return api_info

    def split_url_info(self,url):
        """
        This function will split all infomation from a given url, including host, url path,type.

        :param url:  如： http://localhost/api/login/test.do?username=user1&password=123456
        :return:
            host：http://localhost
            url ： /api/login/test.do
            type： /api
        """
        api_type_list = ['/api/']   # 可根据接口格式，自定义对应的分隔关键字
        url_info={}
        host, api_url ,type ='','',''
        for api_type in api_type_list:
            if api_type in url:
                host,api_url = url.split(api_type)
                api_url = api_type+api_url
                type = api_type.replace('/','')
                break
        url_info['host']=host
        url_info['url']=api_url
        url_info['type']=type
        return url_info

    def get_para_info(self,api_info,osign_list,type='default', needOsign=True):
        """
        Get target value for all paras and do the osign process.

        :param api_info:
        :param osign_list:
        :param type:
        :param needOsign:
        :return:
        """
        para_info = api_info['paras']
        para_info = self.get_api_paras(para_info,type=type)
        if needOsign:
            para_info = self.api_osign(para_info,osign_list,appkey=appKey)
        return para_info


    def get_api_paras(self,para_info,type='default'):
        """
        Convert all changeable values in the para list.

        :param para_info:
        :param type:
        :return:
        """
        for para in para_info:
            if '{' in para_info[para] and '}' in para_info[para]:
                para_info[para]=self.get_para_values(para_info[para],type=type)
        return para_info

    def get_para_values(self,para_name,type='default'):
        """
        Convert para's value to target value.  If you want to set a para to be changeable, set the value to be {paraname} in api info.
        the value is saved on paras.py , such as :
        :param para_info:
        :param type:  there are three types:
            default :  return the first value on the value list.
            random :  return a random value on the value list.
            all :  return the the whole value list.
        :return:
        """
        para_name = para_name.replace('{','')
        para_name = para_name.replace('}','')
        from app.api_new import paras
        try:
            values = getattr(paras.paraValues(), para_name)
        except AttributeError as e:
            print(e)
            values = []
        if len(values)>1:
            if type=='all':
                return values
            elif type == 'random':
                import random
                randomIndex = random.randrange(1,100)%len(values)
                return values[randomIndex]
            else:
                return values[0]
        else:
            return values

    def api_osign(self,para_info, osign_list,appkey=appKey):
        """
        Calculate the osign value using the osign list.
        :param para_info:
        :param osign_list:
        :param appkey:
        :return:
        """
        para_info['osign'] = self.getOsign(para_info, osign_list, appkey=appkey)
        return para_info

    def getOsign(self,para_info, osignList, appkey):
        """
        The real osign method.

        :param para_info:
        :param osignList:
        :param appkey:
        :return:
        """
        paraPand = ''
        print('osign list is :',osignList)
        for para in osignList:
            if para == 'appKey':
                paraPand += appkey
            else:
                paraPand += str(para_info[para])
                print(para_info[para])
        print(paraPand)
        return self.md5(paraPand)

    def md5(self,preosign):
        """
        MD5 osign.
        :param preosign:
        :return:
        """
        import hashlib
        m = hashlib.md5()
        preosign = preosign.encode('utf-8')
        print(preosign)
        m.update(preosign)
        return m.hexdigest()

    def dict_2_str(self,para_info):
        '''
        将字典变成，key='value',key='value' 的形式
        '''
        tmplist = []
        import urllib.parse
        for k, v in para_info.items():
            if str(k) != 'appKey':
                tmp = "%s=%s" % (str(k), urllib.parse.quote(str(v)))
                tmplist.append(tmp)
        return '&'.join(tmplist)



    def sendRequest(self,url, usingHeader=True):
        import httplib2
        print(url)
        http = httplib2.Http(timeout=30)
        headers = {'Content-type': 'application/json;charset=utf8'}
        tryTime = 3
        while tryTime:
            try:
                if usingHeader:
                    response, content = http.request(url, 'POST',body='', headers=headers)
                else:
                    response, content = http.request(url, 'POST', headers=headers)
                content = content.decode('utf-8')
                break
            except Exception as e:
                response = "Error"
                content = e
                tryTime += -1
        return response, content

