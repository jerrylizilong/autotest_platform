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
        if len(elements)==0:
            return None
        elif len(elements)==1:
            return elements[0]
        elif is_displayed:
            for element in elements:
                if element.is_displayed():
                    return element
            return None
        else:
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
        result = 2
        if isError:
            fileName, fileName1 = util.util().screenshot('error', id)
        else:
            fileName, fileName1 = util.util().screenshot('normal', id)
        try:
            # print(fileName)
            driver.save_screenshot(fileName)
            screenFileList.append(fileName1)
            result = 1
        except requests.exceptions.ConnectionError as e:
            log.log().logger.error(e)
        except selenium.common.exceptions.WebDriverException as e:
            log.log().logger.error(e)
        return result, screenFileList

    def assert_text(self,driver,text):
        try:
            elements = driver.find_elements(by='xpath', value="//*[contains(.,'" + text + "')]")
        except NoSuchElementException as e:
            log.log().logger.info(e)
            elements = []
        if len(elements) > 0:
            result = '1'
        else:
            result = '2'
        log.log().logger.info('verify result is : %s' % result)
        return result

    def assert_title(self, driver, text):
        if text in driver.title:
            result = '1'
        else:
            result = '2'
        log.log().logger.info('verify result is : %s' % result)
        return result


    def assert_element_text(self,driver,para_list,isNot=False):
        result = '2'
        para_list=str(para_list).split(',')
        if len(para_list)==3:
            method, value, text = para_list[0],para_list[1],para_list[2]
            text0 = ''
            try:
                element = self.find_element(driver, [method, value])
                text0 = element.text
            except NoSuchElementException as e:
                log.log().logger.info(e)
            except AttributeError as e:
                log.log().logger.info(e)
            if not len(text0):
                try:
                    text0=element.get_attribute('value')
                except NoSuchElementException as e:
                    log.log().logger.info(e)
                except AttributeError as e:
                    log.log().logger.info(e)
            log.log().logger.info('目标文本：%s， 期待文本：%s' %(text0,text))
            if (text in str(text0)):
                result = '1'
        if isNot:
            if result !=1:
                result =1
        log.log().logger.info('verify result is : %s' % result)
        return result


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
                log.log().logger.info(comd)
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
            try:
                element.click()
            except NoSuchElementException as e:
                log.log().logger.info(e)
        time.sleep(2)

    def try_click(self,driver,para_list):
        # para_list=str(para_list).split(',')
        if len(para_list)==2:
            method, value = para_list[0],para_list[1]
            # print(value)
            element = self.find_element(driver, [method, value])
            if element:
                for i in range(3):
                    try:
                        element.click()
                    except NoSuchElementException as e:
                        log.log().logger.info(e)
        time.sleep(2)

    def click_index(self,driver,para_list):
        method, value, index = para_list[0], para_list[1], para_list[2]
        elements = self.find_elements(driver, [method, value])
        if len(elements):
            for i in range(3):
                try:
                    elements[int(index)].click()
                except NoSuchElementException as e:
                    log.log().logger.info(e)
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