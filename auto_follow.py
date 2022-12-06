from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time as t
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=r"C:\Users\nicky\.wdm\drivers\chromedriver\win32\103.0.5060.53\chromedriver.exe",chrome_options=options)

#CODE USED AS A BASIS
"""
driver.get('http://codepad.org')

# click radio button
python_button = driver.find_elements(By.XPATH,"//input[@name='lang' and @value='Python']")[0]
python_button.click()

# type text
text_area = driver.find_element_by_id('textarea')
text_area.send_keys("print('Hello World')")

# click submit button
submit_button = driver.find_elements_by_xpath('//*[@id="editor"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[3]/input')[0]
submit_button.click()
"""


import itertools
def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)





#Creates list of account names
def get_urls(doc_name):
    with open(doc_name, 'r') as f:
        string = f.read()
        string.strip()
    list = string.split('\n')
    list.remove('')
    urls = ['https://twitter.com']*len(list)
    for i in range(len(list)):
        urls[i] += '/'+ list[i]
    return urls


try:
    values = ['followers', 'favorites', 'retweets']
    urls = []
    for value in values:
        urls += get_urls('top_handles_' +  value +'.txt')
    urls = set(urls)
    print(len(urls))
    #Must login to your twitter account
    driver.get('http://twitter.com/login')
    t.sleep(30)

    for url in urls:
        driver.get(url)
        t.sleep(3)
        res = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(res, "html.parser")
        soup_elements = soup.find_all(attrs={"role": "button"})
        for elt in soup_elements:
            if 'Follow' in elt.text:
                soup_element = elt
                break
        print(soup_element.text)
        xpath = xpath_soup(soup_element)
        print(xpath)
        element = driver.find_element(By.XPATH, xpath)

        action = ActionChains(driver)
        action.click(on_element = element)

        # perform the operation
        action.perform()
        t.sleep(2)
except Exception as e:
    print(e)
    driver.quit()

driver.quit()
