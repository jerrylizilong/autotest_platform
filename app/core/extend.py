import time,requests
from app.core import log,util
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import selenium

class extend():
    """
    You can add new function here for you own.
    """


    def find_elements(self,driver,para_list,is_displayed=True,text=''):
        """
        Find elements using the given condition..

        :param driver:
        :param para_list: [method, value] eg : ['id','add_btn']
        :param is_displayed: True : Only the elements shown on the page will be returned.    False: Elements will also be returned no matter is shown or hidden.
        :param text: Only the elements contain the specified text will be returned.
        :return: Found element list.
        """
        method, value = para_list[0], para_list[1]
        if 'css' in method:
            method = By.CSS_SELECTOR
        elif 'class' in method:
            method = By.CLASS_NAME
        elif 'text' in method:
            method = By.PARTIAL_LINK_TEXT
        elif 'tag' in method:
            method = By.TAG_NAME
        elements = driver.find_elements(by=method,value=value)
        new_elements = []
        for element in elements:
            if text != '':
                if self.is_text_in_element(element,text):
                    if is_displayed:
                        if element.is_displayed():
                            new_elements.append(element)
                    else:
                        new_elements.append(element)
            else:
                if is_displayed:
                     if element.is_displayed():
                        new_elements.append(element)
                else:
                    new_elements.append(element)
        return new_elements


    def find_element(self,driver,para_list,is_displayed=True,index=0,text=''):
        """
        Find element using the given condition..

        :param driver:
        :param para_list: [method, value] eg : ['id','add_btn']
        :param is_displayed: True : Only the element shown on the page will be returned.    False: Element will also be returned no matter is shown or hidden.
        :param index: If more than one element is found, driver will return the specified element by index.  e.g: element 0,1,2 is found and the index is set to by 2, the element 2 will be returned.
        :param text: Only the element contains the specified text will be returned.
        :return: Found element.
        """
        elements = self.find_elements(driver,para_list,is_displayed=is_displayed,text=text)
        if len(elements)>0 and index < len(elements):
            return elements[index]
        else:
            return elements[0]

    def is_text_in_element(self,element,text):
        """
        Return whether element's text related attribute('textContent','text','value','placeholder') contains the specified text.

        :param element: Specified web element.
        :param text: Target text.
        :return: True or false.
        """
        attribute_list = ['textContent','text','value','placeholder']
        for attribute in attribute_list:
            result = self.get_element_attribute(element,attribute,text)
            if result:
                return True
        return False


    def get_element_attribute(self,element,attribute,text):
        """
        Return whether element's given attribute contains the specified text.

        :param element: Specified web element.
        :param attribute: Target attribute.
        :param text: Target text.
        :return: True or false.
        """
        if element.get_attribute(attribute) is not None:
            return text in element.get_attribute(attribute)
        else:
            return None

    def switchIframe(self,driver,para_list):
        """
        Swith to specified iframe.

        :param driver:
        :param para_list:  [method, value] eg : ['id','iframe-main']
        """
        method, value = para_list[0], para_list[1]
        if method=='css':
            method = By.CSS_SELECTOR
        driver.switch_to_frame(driver.find_element(by = method,value=value))
        time.sleep(2)

    def switchWindow(self,driver):
        """
        Swith to another tab on the browser.

        :param driver:
        """
        for name in driver.window_handles:
            if name != driver.current_window_handle:
                driver.switch_to.window(name)
        time.sleep(2)

    def screenshot(self,driver,id,screenFileList,isError=False):
        """
        Save current page as a screenshot.

        :param driver:
        :param id:  case id.
        :param screenFileList:  screenshot file list for this case.
        :param isError:  screenshot type, error or normal.
        :return:
        """
        result = '2'
        if isError:
            fileName, fileName1 = util.util().screenshot('error', id)
        else:
            fileName, fileName1 = util.util().screenshot('normal', id)
        log.log().logger.info(fileName)
        driver.save_screenshot(fileName)
        screenFileList.append(fileName1)
        if not isError:
            result = '1'
        return result, screenFileList

    def assert_text(self,driver,text):
        """
        Assert whether current web page contains the given text.

        :param driver:
        :param text:
        :return:
        """
        elements = driver.find_elements(by='xpath', value="//*[contains(.,'" + text + "')]")
        assert len(elements)

    def assert_title(self,driver,text):
        """
        Assert whether current web page's title contains the given text.

        :param driver:
        :param text:
        :return:
        """
        log.log().logger.info('目标文本：%s， 期待包含文本：%s' % (driver.title, text))
        assert text in driver.title

    def assert_element_text(self,driver,para_list,isNot=False,isUpper = False):
        """
        Assert whether the specified web element contains the given text.

        :param driver:
        :param para_list:   [method, value] eg : ['id','add_btn']
        :param isNot:  If you want to assert that target element doesn't contain the given text, isNot should be set to True.
        :param isUpper: if isUpper is false, will convert the target text to upper mode.
        :return:
        """
        text0 = ''
        if len(para_list)==3:
            method, value, text = para_list[0],para_list[1],para_list[2]
            element = self.find_element(driver, [method, value])
            text0 = element.text
            if isUpper:
                text = text.upper()
                text0 = text0.upper()
            if not len(text0):
                text0=element.get_attribute('value')
        if isNot:
            log.log().logger.info('目标文本：%s， 期待不包含文本：%s' % (text0, text))
            assert (text in str(text0))==False
        else:
            log.log().logger.info('目标文本：%s， 期待包含文本：%s' % (text0, text))
            assert (text in str(text0))


    def select(self,driver,para_list):
        """
        Select a option for sepecified select type web element.

        :param driver:
        :param para_list: [method, value, option_method, option_value] eg : ['id','country_list','text','China']
                        index: select the option by it's index.
                        value: select the option by it's value.
                        text: select the option by it's text(full text).
                        text_part: select the option by it's text(part of the option).  e.g:  option text is 'autotest15865524', you can found the option by 'autotest'
        :return:
        """
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
        """
        select the option by it's text(part of the option).  e.g:  option text is 'autotest15865524', you can found the option by 'autotest'

        :param parant_el:  The specified select type web element.
        :param text:
        :return:
        """
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
        """
        Click all options for the web element.

        :param driver:
        :param para_list:  [method, value] eg : ['id','add_btn']
        :param tag_name: option by default . you can set to other tag type.
        :return:
        """
        method, value = para_list[0], para_list[1]
        elements = self.find_elements(driver,[method,value])
        for element in elements:
            for opt in element.find_elements_by_tag_name(tag_name):
                opt.click()
        time.sleep(2)

    def check_all(self,driver,para_list):
        """
        Click all options for the web element.

        :param driver:
        :param para_list:  [method, value] eg : ['id','add_btn']
        :param tag_name: option by default . you can set to other tag type.
        :return:
        """
        method, value = para_list[0], para_list[1]
        elements = self.find_elements(driver,[method,value])
        for element in elements:
            element.click()
        time.sleep(2)

    def click_menu(self,driver,text):
        """
        Click on a element by it's text.

        :param driver:
        :param text:
        :return:
        """
        try :
            driver.find_element_by_link_text(text).click()
        except:
            try:
                driver.find_element_by_partial_link_text(text).click()
            except:
                try:
                    elements = driver.find_elements_by_tag_name('span')
                    if len(elements):
                        for element in elements:
                            if self.is_text_in_element( element, text):
                                element.click()
                                break
                except:
                    try:
                        elements = driver.find_elements_by_tag_name('li')
                        if len(elements):
                            for element in elements:
                                if self.is_text_in_element(element, text):
                                    element.click()
                                    break
                    except:
                        elements = driver.find_elements(by='xpath', value="//*[contains(.,'" + text + "')]")
                        for element in elements:
                            element.click()
        time.sleep(2)

    def click_menu_new(self,driver,menulist,needAssert=True):
        """
        Click on menu.  Only used for GHW's admin page.
        use / to split menu's text for two levels.

        :param driver:
        :param menulist:  e.g :   parent_menu_name/sub_menu_name
        :param needAssert: whether want to assert the header title contains the given menulist.
        :return:
        """
        menulist = menulist.split('/')
        log.log().logger.info('click on menu1: %s' %menulist[0])
        self.click_menu(driver, menulist[0])
        time.sleep(1)
        if len(menulist)>1:
            for i in range(3):
                try :
                    log.log().logger.info('click on menu2: %s' % menulist[1])
                    self.click_menu(driver,menulist[1])
                    break
                except NoSuchElementException as e:
                    log.log().logger.info('click on menu1: %s' % menulist[0])
                    self.click_menu(driver, menulist[0])
            time.sleep(1)
            if needAssert:
                self.assert_element_text(driver, ['id','headerTitle',menulist[1]])
                self.assert_element_text(driver,['id','headerTitle',menulist[0]])




    def click_text(self,driver,text,type):
        """
        click a web element by it's text and type.

        :param driver:
        :param text:
        :param type: by default is empty.  you can specified the type to it's tag name.  e.g : span, li, a .
        :return:
        """
        if len(type) ==0:
            try :
                driver.find_element_by_link_text(text).click()
            except:
                try:
                    driver.find_element_by_partial_link_text(text).click()
                except:
                    elements = driver.find_elements(by='xpath', value="//*[contains(.,'" + text + "')]")
                    for element in elements:
                        element.click()
        else:
            elements = self.find_elements(driver, ['tag', type], is_displayed=True, text=text)
            if len(elements):
                elements[0].click()
        time.sleep(2)


    def click_button_by_text(self,driver,text,type):
        """
        click a button type web element by it's text and type.

        :param driver:
        :param text:
        :param type: by default is btn.  you can specified the type to it's class name.  e.g : btn, button .
        :return:
        """
        if len(type) ==0:
            type = 'btn'
        elements = self.find_elements(driver,['class',type],is_displayed=True,text=text)
        if len(elements):
            elements[0].click()
            time.sleep(2)

    def try_click(self,driver,para_list):
        """
        Try to click on a specified web element.  Sometimes a message will be popped up on a web page. We need this function to close the pop up window.

        :param driver:
        :param para_list:
        :return:
        """
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
        """
        When more than one web element are found by the given value, you can use the index the specified which element you want to click.

        :param driver:
        :param para_list: [method, value, index]
        :return:
        """
        method, value, index = para_list[0], para_list[1], para_list[2]
        elements = self.find_elements(driver, [method, value])
        elements[int(index)].click()
        time.sleep(2)


    def fill(self,driver,para_list,text, is_displayed = True,index=0):
        """
        Fill specified text to the target web elelemnt.

        :param driver:
        :param para_list: [method, value]
        :param text:    You can use {r} to insert random value for the text.   e.g:   productId{r}  = productId15642  (generated by random)
        :param is_displayed:
        :param index:
        :return:
        """
        text = self.replaceRandomValue(text)
        elements = self.find_elements(driver, para_list,is_displayed,text='')
        elements[index].clear()
        elements[index].send_keys(text)

    def fill_file(self,driver,para_list,text):
        """
        Fill specified file path to target web element.
        Params are the same with fill function.
        e.g: text = c:/example.jpg

        :param driver:
        :param para_list:[method,value]
        :param text:
        :return:
        """
        self.fill(driver,para_list,text, is_displayed = False)

    def fill_index(self,driver,para_list,text,index):
        """
        Fill specified text to target web element. For more than one element is found, use index to specified target element.
        Params are the same with fill function.

        :param driver:
        :param para_list:[method,value]
        :param text:
        :param index:
        :return:
        """
        self.fill( driver, para_list, text, is_displayed=False, index=index)

    def fill_on_date(self,driver,para_list):
        """
        Fill specified date to target web element. Remove the readonly attribute otherwise you cannot sendkeys to the element.
        Params are the same with fill function.
        e.g: text = 2019-01-01

        :param driver:
        :param para_list:[method,value]
        :return:
        """
        method, value,text = para_list[0], para_list[1], para_list[2]
        driver.execute_script("document.getElementBy%s('%s').removeAttribute('readOnly');" %(str(method).capitalize(),value))
        self.find_element(driver,[method,value]).clear()
        self.find_element(driver, [method,value]).send_keys(text)
        time.sleep(2)

    def copy_from_another_element(self,driver,para_list1,para_list2, is_displayed = True):
        """
        Get the text value of element2 , and fill it into element1.

        :param driver:
        :param para_list1:[method,value]
        :param para_list2:[method,value]
        :param is_displayed:
        :return:
        """
        element1 = self.find_element(driver, para_list1,is_displayed)
        text =self.get_element_text(driver, para_list2)
        element1.clear()
        element1.send_keys(text)

    def get_element_text(self,driver,para_list):
        """
        Get text value from text related attribute('textContent','text','value','placeholder') for a specified element.

        :param driver:
        :param para_list: [method,value]
        :return:
        """
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


    def replaceRandomValue(self,oriValue):
        """
        General random value for the given text.
        e.g:  oriValue is productId{r}testing,  new value is : productId45213testing

        :param oriValue:
        :return:
        """
        import random
        newValue = str(oriValue).replace('{r}',str(random.randint(10000,99999)))
        print(oriValue,newValue)
        return newValue



    def wait(self,t):
        """
        Sleep for speicified seconds.    2 seconds by default.

        :param t: int.
        :return:
        """
        import time
        if len(str(t))==0:
            t=2
        else:
            time.sleep(int(t))


    def move_to(self,driver,para_list):
        """
        Move mouse to target element.

        :param driver:
        :param para_list:[method, value ]
        :return:
        """
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

