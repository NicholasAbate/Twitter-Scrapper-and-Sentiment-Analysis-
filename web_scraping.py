from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

"""
Used to create the urls from text of handles
"""
with open('mid_handles.txt', 'r') as f:
    string = f.read()
    string.strip()
list = string.split('\n')
list.remove('')
urls = ['https://twitter.com']*len(list)
for i in range(len(list)):
    urls[i] += '/'+ list[i] + '/followers'


options = webdriver.ChromeOptions()


#######################################################################################
"""
Could be potentially used to automate login as well
"""
#options.add_argument(r"C:\Users\nicky\AppData\Local\Google\Chrome Beta\User Data\Profile 1")
#Path to your chrome profile
#options.add_argument("user-data-dir=C:\\Users\\Hana\\AppData\\Local\\Google\\Chrome\\User Data\\")
#options.add_argument('--profile-directory= Profile 1')
##########################################################################################

driver= webdriver.Chrome(executable_path=r"C:\Users\nicky\.wdm\drivers\chromedriver\win32\103.0.5060.53\chromedriver.exe", chrome_options=options)


# solution
filename = r'C:\Users\nicky\Documents\DavinciWearables\Fertility_and_Menstrual_followers.csv'
def twitter_followings_while():
    users_dup = []
    num_users = 0
    for url in urls:
        driver.get(url)
        sleep(2)
        res = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(res, "html.parser")

        current_height = 0
        last_height = 0
        while True:
            current_height = driver.execute_script('return document.body.scrollHeight')

            if current_height == last_height:
                break
            else:
                print(str(current_height - last_height))
            users = []
            res = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(res, "html.parser")
            data = soup.find(attrs={"data-testid": "primaryColumn"}).find_all(attrs={"data-testid": "UserCell"})
            for counter in range(len(data)):
                user = data[counter].find_all("span")
                #print('user', user)
                full_name = user[1].text
                handle = user[2].text

                # not all users have a bio
                try:
                    bio = user[5].text
                except:
                    bio = None

                # avoid duplicates
                user_data = {"full_name": full_name,
                              "handle": handle,
                              "bio": bio
                             }

                if user_data['handle'] not in users_dup:
                    users.append(user_data)
                    users_dup.append(user_data['handle'])
            num_users += len(users)
            print('number of users: ' + str(num_users))
            data_df = pd.DataFrame(users)
            data_df.to_csv(filename, mode='a')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            last_height = current_height
            sleep(5)







driver.get("https://twitter.com/login")     #Can't currently login on its own. Must first login to Twitter
sleep(50)
twitter_followings_while()
print('Done!')
driver.quit()
