import time,requests
from app.core import log,util
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import selenium

class extend():
    def find_element(self,driver,para_list,is_displayed=True):
        method, value= para_list[0], para_list[1]
        if 'css' in method:
            method = By.CSS_SELECTOR
        elif 'class' in method:
            method = By.CLASS_NAME
        elif 'text' in method:
            method = By.PARTIAL_LINK_TEXT
        elements = driver.find_elements(by=method,value=value)
        if len(elements)>0 and is_displayed:
            for element in elements:
                if element.is_displayed():
                    return element
                else:
                    elements.remove(element)
        return elements[0]

    def find_elements(self,driver,para_list):
        method, value = para_list[0], para_list[1]
        if 'css' in method:
            method = By.CSS_SELECTOR
        elif 'class' in method:
            method = By.CLASS_NAME
        elif 'text' in method:
            method = By.PARTIAL_LINK_TEXT
        elements = driver.find_elements(by=method,value=value)
        return elements

    def switchIframe(self,driver,para_list):
        method, value = para_list[0], para_list[1]
        # 切换 iframe
        if method=='css':
            method = By.CSS_SELECTOR
        driver.switch_to_frame(driver.find_element(by = method,value=value))
        time.sleep(2)

    def switchWindow(self,driver):
        for name in driver.window_handles:
            if name != driver.current_window_handle:
                driver.switch_to.window(name)
        time.sleep(2)

    def screenshot(self,driver,id,screenFileList,isError=False):
        result = '2'
        if isError:
            fileName, fileName1 = util.util().screenshot('error', id)
        else:
            fileName, fileName1 = util.util().screenshot('normal', id)
        log.log().logger.debug(fileName)
        driver.save_screenshot(fileName)
        screenFileList.append(fileName1)
        if not isError:
            result = '1'
        return result, screenFileList

    def assert_text(self,driver,text):
        elements = driver.find_elements(by='xpath', value="//*[contains(.,'" + text + "')]")
        assert len(elements)

    def assert_title(self,driver,text):
        log.log().logger.info('目标文本：%s， 期待包含文本：%s' % (driver.title, text))
        assert text in driver.title

    def assert_element_text(self,driver,para_list,isNot=False):
        # para_list=str(para_list).split(',')
        text0 = ''
        if len(para_list)==3:
            method, value, text = para_list[0],para_list[1],para_list[2]
            element = self.find_element(driver, [method, value])
            text0 = element.text
            if not len(text0):
                text0=element.get_attribute('value')
            # log.log().logger.info('目标文本：%s， 期待文本：%s' % (text0,text))
        if isNot:
            log.log().logger.info('目标文本：%s， 期待不包含文本：%s' % (text0, text))
            assert (text in str(text0))==False
        else:
            log.log().logger.info('目标文本：%s， 期待包含文本：%s' % (text0, text))
            assert (text in str(text0))



    def select(self,driver,para_list):
        method, value, option_method, option_value = para_list[0],para_list[1],para_list[2],para_list[3]
        from selenium.webdriver.support.select import Select
        if option_method =='index':
            comd = 'Select(driver.find_element_by_%s("%s")).select_by_%s(%s)' %(method,value,option_method,option_value)
        else:
            if option_method == 'text_part':
                self.select_by_visible_text(driver.find_element(by=method,value=value),option_value)
            else:
                if  option_method == 'text':
                    option_method = 'visible_text'
                comd = 'Select(driver.find_element_by_%s("%s")).select_by_%s("%s")' % (
                method, value, option_method, option_value)
                log.log().logger.debug(comd)
                exec(comd)
        time.sleep(2)

    def select_by_visible_text(self,parant_el, text):
        opts = parant_el.find_elements(By.TAG_NAME,'option')
        matched = False
        if len(opts):
            for candidate in opts:
                if text in candidate.text:
                    candidate.click()
                    matched = True
                    break
        if not matched:
            raise NoSuchElementException("Could not locate element with visible text: %s" % text)
        time.sleep(2)


    def select_all(self,driver,para_list,tag_name='option'):
        method, value = para_list[0], para_list[1]
        elements = self.find_elements(driver,[method,value])
        for element in elements:
            for opt in element.find_elements_by_tag_name(tag_name):
                opt.click()
        time.sleep(2)

    def check_all(self,driver,para_list):
        method, value = para_list[0], para_list[1]
        elements = self.find_elements(driver,[method,value])
        for element in elements:
            element.click()
        time.sleep(2)

    def click_menu(self,driver,text):
        try :
            driver.find_element_by_link_text(text).click()
        except:
            driver.find_element_by_partial_link_text(text).click()
        time.sleep(2)

    def click_text(self,driver,text):
        elements = driver.find_elements(by='xpath', value="//*[contains(.,'" + text + "')]")
        for element in elements:
            element.click()
        time.sleep(2)

    def try_click(self,driver,para_list):
        if len(para_list)==2:
            method, value = para_list[0],para_list[1]
            for i in range(3):
                try:
                    self.find_element(driver, [method, value]).click()
                    break
                except:
                    pass
        time.sleep(2)

    def click_index(self,driver,para_list):
        method, value, index = para_list[0], para_list[1], para_list[2]
        elements = self.find_elements(driver, [method, value])
        elements[int(index)].click()
        time.sleep(2)

    def fill_on_date(self,driver,para_list):
        method, value,text = para_list[0], para_list[1], para_list[2]
        driver.execute_script("document.getElementBy%s('%s').removeAttribute('readOnly');" %(str(method).capitalize(),value))
        self.find_element(driver,[method,value]).clear()
        self.find_element(driver, [method,value]).send_keys(text)
        time.sleep(2)

    def wait(self,t):
        import time
        if len(str(t))==0:
            t=2
        else:
            time.sleep(int(t))


    def move_to(self,driver,para_list):
        if len(para_list)==2:
            method, value = para_list[0],para_list[1]
            for i in range(3):
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(driver).move_to_element(to_element=self.find_element(driver, [method, value])).perform()
                    break
                except:
                    pass
        time.sleep(2)

    def fill(self,driver,para_list,text, is_displayed = True):
        element = self.find_element(driver, para_list,is_displayed)
        # element = driver.find_element(by=para_list[0],value=para_list[1])
        element.clear()
        element.send_keys(text)

    def fill_file(self,driver,para_list,text, is_displayed = False):
        self.fill(driver,para_list,text, is_displayed = False)

    def copy_from_another_element(self,driver,para_list1,para_list2, is_displayed = True):
        # 将 元素 2 的值复制填写到 元素1中
        element1 = self.find_element(driver, para_list1,is_displayed)
        text =self.get_element_text(driver, para_list2)
        element1.clear()
        element1.send_keys(text)

    def get_element_text(self,driver,para_list):
        element = self.find_element(driver, para_list,is_displayed=True)
        if len(element.text):
            return element.text
        elif len(element.get_attribute('value')):
            return element.get_attribute('value')
        elif len(element.get_attribute('textContent')):
            return element.get_attribute('textContent')
        elif len(element.get_attribute('innerText')):
            return element.get_attribute('innerText')
        else:
            return ''