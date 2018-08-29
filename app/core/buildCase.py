import string
import os
from app.core import keywords,log
from app import useDB

screen_shot_path = os.getcwd()

class buildCase(object):
    def __init__(self):
        self.name = ''

    def getRandom(self,oriValue):
        import random
        newValue = oriValue +str(random.randint(10000,99999))
        return newValue

    def convertToComend(self,template, paraCount, paraValue,elementTemplate):
        # log.log().logger.info(template, paraCount, paraValue,elementTemplate)
        for i in range(len(paraValue)):
            paraValue[i] = paraValue[i].replace('"', '\'')
            paraValue[i] = paraValue[i].replace('comma', ',')
        # log.log().logger.info(paraValue)
        template = string.Template(template)
        if elementTemplate != '' and elementTemplate !=None:
            elementTemplate = string.Template(elementTemplate)
        else:
            elementTemplate = ''
            element = ''
        if len(paraValue) in (paraCount, paraCount+1) and paraCount > 0 and paraCount < 5:
            if paraValue[0] == 'css':
                paraValue[0] = 'css_selector'
            if paraValue[0] == 'class':
                paraValue[0] = 'class_name'
            if paraValue[0] == 'url':
                paraValue.append( 'p')
            if len(paraValue) == paraCount+1:
                if paraValue[-1]=='p':
                    # p stands for parameter
                    paraValue[-2]=self.getPara(paraValue[-2])
                if paraValue[-1]=='r':
                    # r stands for random
                    paraValue[-2]=self.getRandom( paraValue[-2])
            if paraCount == 1:
                comed = template.substitute(para1=paraValue[0])
                if elementTemplate != '':
                    element = elementTemplate.substitute(para1=paraValue[0])
            elif paraCount == 2:
                comed = template.substitute(para1=paraValue[0], para2=str(paraValue[1]))
                if elementTemplate != '':
                    element = elementTemplate.substitute(para1=paraValue[0], para2=str(paraValue[1]))
            elif paraCount == 3:
                comed = template.substitute(para1=paraValue[0], para2=str(paraValue[1]), para3=paraValue[2])
                if elementTemplate != '':
                    element = elementTemplate.substitute(para1=paraValue[0], para2=str(paraValue[1]), para3=paraValue[2])
            elif paraCount == 4:
                comed = template.substitute(para1=paraValue[0], para2=str(paraValue[1]), para3=paraValue[2],
                                            para4=paraValue[3])
                if elementTemplate != '':
                    element = elementTemplate.substitute(para1=paraValue[0], para2=str(paraValue[1]), para3=paraValue[2],
                                            para4=paraValue[3])
            elif paraCount == 5:
                comed = template.substitute(para1=paraValue[0], para2=str(paraValue[1]), para3=paraValue[2],
                                            para4=paraValue[3], para5=paraValue[4])
                if elementTemplate != '':
                    element = elementTemplate.substitute(para1=paraValue[0], para2=str(paraValue[1]), para3=paraValue[2],
                                            para4=paraValue[3], para5=paraValue[4])
            # log.log().logger.info(comed, element)
            return comed, element
        else:
            log.log().logger.error("para count is wrong for %s , should be %s , but %s : %s" % (
                template, paraCount, len(paraValue), str(paraValue)))
            return '',''

    def build_case(self,keyword,steps):
        paraCount,template, elementTemplate = keywords.keywords().getPara(keyword)
        conmod, element = self.convertToComend(template,paraCount,steps,elementTemplate)
        return conmod,element


    def readPublic(self,caseList0) :
        # print(caseList0)
        resultList = []
        isRead=True
        while(isRead):
            case2 = caseList0[0].split('|')
            if case2[0] == "公共方法":
                caseList0.remove(caseList0[0])
                # log.log().logger.info(case2)
                case0 = self.read_public_case(case2[1])
                if len(case0):
                    resultList0 = []
                    case0=case0[0]
                    for casei in caseList0:
                        case0.append(casei)
                    try:
                        case0.remove('')
                    except ValueError as e:
                        # log.log().logger.info('error: %s' %e)
                        pass
                    caseList0=case0
                else:
                    log.log().logger.error('public function is not found!')
                    resultList=[]
                    isRead = False
            else:
                resultList=caseList0
                isRead = False
        # print(resultList)
        return resultList


    #根据编号查找公共用例
    def read_public_case(self,caseNo) :
        sql = 'select steps from test_case where isPublicFunction = "1" and status = 1 and name = "'+caseNo+'";'
        case = useDB.useDB().search(sql)
        if len(case):
            caseList = []
            for case0 in case :
                case3 = str(case0[0]).split(',')
                caseList.append(case3)
            # log.log().logger.info(caseList)
            return caseList
        else:
            return ''

    def getPara(self,para):
        url = useDB.useDB().search("SELECT VALUE FROM test_config WHERE NAME = '%s' AND isUseAble = '1';" % para)
        return url[0][0]

    def getCase(self,case):
        case = case.split(',')
        if '' in case:
            case.remove('')
        # connect with public steps to normal steps.
        # case = self.readPublic(case)
        if len(case):
            if '公共方法' in case[0]:
                case = self.readPublic(case)
        newstep = []
        if len(case):
          for step in case:
            step0 = []
            # log.log().logger.info(step)
            step = step.split('|')
            if step == '':
                pass
            else:
                step0.append(step[0])
                if len(step) > 1:
                    step1 = step[1].split('@@')
                    step0.append(step1)
                else:
                    step0.append(['1'])

                newstep.append(step0)
        else:
            newstep=''
        return newstep
