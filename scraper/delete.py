from pyclick import*
from PIL import Image,ImageGrab
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.common.keys import Keys
import re


def open_ip(num=0, grab_ip = False):
    #IP = '58.218.200.229'
    #PORT = '8932'
    # todo: grab ip?
    IP = '43.255.228.150'
    PORT = '3128'
    string_proxy= IP+ ':'+PORT
    print(string_proxy)
    string_part = '--proxy-server=http://'
    change_IP = string_part + string_proxy
    print(change_IP)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(change_IP)
    driver = webdriver.Chrome(executable_path='/Users/xinyue/PycharmProjects/web_scraping/driver/chromedriver',options=chrome_options)
    driver.delete_all_cookies()
    driver = open_driver(driver, num)
    start_scrape(driver, num)


def open_driver(driver, num):
    link = 'https://www.tianyancha.com/property/2'

    try:
         # wait 30 second
        driver.get(link)
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver = login(driver, num)
        return driver
    except:
        open_ip(num)
    #
    #WebDriverWait(driver, 10)




def login(driver, num):
    trying = driver.find_elements_by_class_name('nav-item ')
    time.sleep(2)
    for each in trying:
        if each.text == '登录/注册':
            each.click()
            #time.sleep(5)
            password_login = driver.find_elements_by_xpath('//div[contains(@class, "title")]')
            for each_link in password_login:
                if each_link.get_attribute('onclick') ==  'loginObj.changeCurrent(1);':
                    each_link.click()
                    print('login')
                    time.sleep(1)
                    driver = login_with_password(driver, num)
    print('loged_in')
    return driver


def login_with_password(driver,num):
    inputElement = driver.find_elements_by_tag_name('input')
    input_username = driver.find_element_by_css_selector('#mobile')
    input_username.send_keys('17045621797')
    input_passwoard = driver.find_element_by_css_selector('#password')
    input_passwoard.send_keys('Exo983106(*')
    try:
        i = 0
        while i<100:
            i = i+1
            driver.find_element_by_css_selector('div > div.body.-scorll-fix.modal-scroll > div > div > div.module.module1.module2.loginmodule.collapse.in > div.sign-in > div.modulein.modulein1.mobile_box.f-base.collapse.in > div.btn.-xl.btn-primary.-block').click()
    except:
        time.sleep(10)
    return driver


def login_with_password_1(driver,num):
    inputElement = driver.find_elements_by_tag_name('input')
    input_username = driver.find_element_by_css_selector('#mobile')
    input_username.send_keys('17045621797')
    input_passwoard = driver.find_element_by_css_selector('#password')
    input_passwoard.send_keys('Exo983106(*')
    time.sleep(20000)
    try:
        i = 0
        while i<100:
            i = i+1
            driver.find_element_by_css_selector('div > div.body.-scorll-fix.modal-scroll > div > div > div.module.module1.module2.loginmodule.collapse.in > div.sign-in > div.modulein.modulein1.mobile_box.f-base.collapse.in > div.btn.-xl.btn-primary.-block').click()
    except:
        time.sleep(3)
        autologin(driver, num)
        #check_second_robort(driver, num)
        print('sucessed')
        return driver


def autologin(driver,num):
    # 点击登录之后开始截取验证码图片
    time.sleep(2)
    img = driver.find_element_by_css_selector('body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_widget > div.gt_box_holder > div.gt_box > a.gt_fullbg.gt_show')
    time.sleep(0.5)
    # 获取图片位子和宽高
    location = img.location

    size = img.size

    # 返回左上角和右下角的坐标来截取图片
    top, bottom, left, right = location['y']-300+30, location['y']-300+30 + size['height']*2, location['x']+600, location['x']+550 + size[
        'width']+300-20
    # 截取第一张图片(无缺口的)
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    captcha1 = screenshot.crop((left, top, right, bottom))
    print('--->', captcha1.size)
    captcha1.save('captcha1.png')
    # 截取第二张图片(有缺口的)
    driver.find_element_by_css_selector('body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_slider > div.gt_slider_knob.gt_show').click()
    time.sleep(4)
    img1 = driver.find_element_by_css_selector('body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_widget > div.gt_box_holder > div.gt_box > a.gt_fullbg.gt_hide > div.gt_cut_fullbg.gt_show')
    time.sleep(0.5)
    location1 = img1.location
    size1 = img1.size
    top1, bottom1, left1, right1 = location1['y']-300+30, location1['y']-300+30 + size1['height']*2, location1['x']+600, location1['x']+550 + size1[
        'width']+300-20
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    captcha2 = screenshot.crop((left1, top1, right1, bottom1))
    captcha2.save('captcha2.png')
    # 获取偏移量
    left = 55

    for i in range(left, captcha1.size[0]):
        for j in range(captcha1.size[1]):
            # 判断两个像素点是否相同
            pixel1 = captcha1.load()[i, j]
            pixel2 = captcha2.load()[i, j]
            f = open("pixel1.txt", "a+")
            f.write("pixel1 %s\r\n" % str(pixel1))
            f.close()
            f1 = open("pixel2.txt", "a+")
            f1.write("pixel2 %s\r\n" % str(pixel2))
            f1.close()
            threshold =65
            #if abs(pixel1[0] - pixel2[0]) > threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            if (abs(pixel1[0] - pixel2[0]) < threshold) & (abs(pixel1[1] - pixel2[1]) < threshold) & (abs(pixel1[2] - pixel2[2]) < threshold):
                pass
            else:
                left = i

    print('缺口位置', left)
    driver = start_move(driver, left, num)
    return driver


def start_move(driver, distance, num):
    element = driver.find_element_by_css_selector(
        'body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_slider > div.gt_slider_knob.gt_show')
    distance -= element.size.get('width')
    distance = 6*23*distance/(49*7)
    ActionChains(driver).click_and_hold(element).perform()
    time.sleep(0.5)
    while distance > 0:
        if distance > 10:
                # 如果距离大于10，就让他移动快一点
            span = random.randint(5, 8)
        else:
                # 快到缺口了，就移动慢一点
            span = random.randint(2, 3)
        print(span)
        ActionChains(driver).move_by_offset(span, 0).perform()
        distance = distance-span

    ActionChains(driver).pause(0.5).release().perform()
    try:
        time.sleep(3)
        if driver.find_element_by_css_selector('body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_slider > div.gt_slider_knob.gt_show'):
            print('能找到滑块，重新试')
            driver.delete_all_cookies()
            driver.refresh()
            driver.quit()
            open_ip(num)
        else:
            print('login success')
            return driver
    except:
        print('login success')
        return driver


def start_scrape(driver, num):
    input_comp = pd.read_csv('CCR_firm_names_2000_2006.txt')[num:]
    for i,r in input_comp.iterrows():
        try:
            if type(r['company_name'])!= float:
                first_result, second_result, third_result, forth_result, fifth_result, sixth_result= search_comp(driver, r['company_name'], num)
                #first_result, second_result, third_result = search_comp(driver, r['company_name'], num)
                num = num+1
                first_result.to_csv('/Users/xinyue/PycharmProjects/web_scraping/1/'+r['company_name']+'.csv')
                second_result.to_csv('/Users/xinyue/PycharmProjects/web_scraping/2/'+r['company_name']+'.csv')
                third_result.to_csv('/Users/xinyue/PycharmProjects/web_scraping/3/'+r['company_name']+'.csv')
                forth_result.to_csv('/Users/xinyue/PycharmProjects/web_scraping/4/'+r['company_name']+'.csv')
                fifth_result.to_csv('/Users/xinyue/PycharmProjects/web_scraping/5/' + r['company_name'] + '.csv')
                sixth_result.to_csv('/Users/xinyue/PycharmProjects/web_scraping/6/' + r['company_name'] + '.csv')
        except:
            num = num + 1
            f = open("error.txt", "a+")
            f.write("Mssing %s\r\n" % r['company_name'])
            f.close()
            pass


def search_comp(driver, comp_name, num):
    check_second_robort(driver, num)
    driver.find_element_by_id('header-company-search').clear()
    inputElement = driver.find_element_by_id("header-company-search")
    inputElement.send_keys(comp_name)
    inputElement.send_keys(Keys.ENTER)

    check_robort(driver, num)

    company_link = driver.find_elements_by_class_name('name')
    window_before = driver.window_handles[0]
    driver.execute_script("arguments[0].click();", company_link[0])

    driver.implicitly_wait(3)
    check_robort(driver, num)
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    current_name = driver.find_element_by_css_selector('div.header > h1').text
    first_result, second_result, third_result, forth_result, fifth_result, sixth_result = scrape_info(driver, current_name, comp_name, num)
    #first_result, second_result, third_result= scrape_info(driver,current_name, comp_name, num)

    driver = check_handels(driver, num)
    driver.switch_to.window(window_before)
    #return first_result, second_result, third_result
    return first_result, second_result, third_result, forth_result, fifth_result, sixth_result


def scrape_info(driver, current_name, comp_name, num):
    try:
        first_result = find_stuff_first_table(driver, current_name, comp_name)
    except:
        first_result = pd.DataFrame()
    try:
        second_result = find_stuff_second_table(driver, current_name, comp_name)
    except:
        second_result = pd.DataFrame()
    try:
        forth_result = find_stuff_forth_table(driver, current_name, comp_name)
    except:
        forth_result = pd.DataFrame()
    try:
        fifth_result = find_stuff_fifth_table(driver, current_name, comp_name)
    except:
        fifth_result = pd.DataFrame()
    try:
        sixth_result = find_stuff_sixth_table(driver, current_name, comp_name)
    except:
        sixth_result = pd.DataFrame()
    try:
        third_result = find_stuff_third_table(driver, current_name, comp_name)
    except:
        third_result = pd.DataFrame()
    #return first_result, second_result, third_result
    return first_result, second_result,third_result,forth_result,fifth_result,sixth_result


def find_stuff_first_table(driver, current_name, comp_name):
    first_table = pd.DataFrame(columns=['name','base_money', 'real_money', 'social_code', 'regist_code', 'company_type',
           'industry', 'time','reg_orgnization', 'run_time','tax', 'employee','insurance', 'old_name','eng_name', 'adress','business'])
    name = driver.find_element_by_css_selector('#_container_baseInfo > table:nth-child(1) > tbody > tr:nth-child(1) > td.left-col.shadow > div > div:nth-child(1) > div.humancompany > div.name > a').text
    base_money = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(1) > td:nth-child(2) > div').text
    real_money = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(1) > td:nth-child(4)').text
    social_code = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(3) > td:nth-child(2)').text
    regist_code = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(3) > td:nth-child(4)').text
    company_type = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(5) > td:nth-child(2)').text
    industry = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(5) > td:nth-child(4)').text
    time = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(6) > td:nth-child(2)').text
    reg_orgnization = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(6) > td:nth-child(4)').text
    run_time = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(7) > td:nth-child(2) > span').text
    tax = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(7) > td:nth-child(4)').text
    employee = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(8) > td:nth-child(2)').text
    insurance = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(8) > td:nth-child(4)').text
    old_name = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(9) > td:nth-child(2)').text
    eng_name = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(9) > td:nth-child(4)').text
    adress = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(10) > td:nth-child(2)').text
    business = driver.find_element_by_css_selector('#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(11) > td:nth-child(2) > span').text
    data = {'name': name,'base_money': base_money, 'real_money':real_money, 'social_code':social_code, 'regist_code':regist_code, 'company_type':company_type,
           'industry': industry, 'time':time,'reg_orgnization':reg_orgnization, 'run_time':run_time,'tax':tax, 'employee':employee,'insurance': insurance, 'old_name':old_name,'eng_name':eng_name, 'adress':adress,'business':business}
    first_table = first_table.append(data, ignore_index=True)
    return first_table


def find_stuff_second_table(driver, company, list_name):
    second_result = pd.DataFrame(columns=['company','order', 'invested_company', 'representative', 'date', 'invests_amount', 'invests_portion',
           'status', 'product','organization'])
    find_element = driver.find_elements_by_xpath('//*[@id="_container_invest"]/div/table/tbody/tr')
    for each_tr in find_element:
        td = each_tr.find_elements_by_xpath(".//td")
        order = td[0].text
        invested_company = td[1].find_element_by_xpath('.//a').text
        representative = td[4].find_element_by_xpath('.//a').text
        date = td[7].find_element_by_xpath('.//span').text
        invests_amount = td[8].find_element_by_xpath('.//span').text
        invests_portion = td[9].find_element_by_xpath('.//span').text
        status = td[10].find_element_by_xpath('.//span').text
        product = td[11].find_element_by_xpath('.//span').text
        organization = td[12].find_element_by_xpath('.//span').text
        data = {'company': company,'order': order, 'invested_company': invested_company,
                'representative': representative, 'date': date,
                'invests_amount':invests_amount, 'invests_portion':invests_portion,
                'status':status, 'product':product, 'organization':organization, 'list_name': list_name}
        second_result = second_result.append(data, ignore_index=True)
    col = ['company', 'order', 'invested_company', 'representative', 'date', 'invests_amount', 'invests_portion',
           'status', 'product','organization', 'list_name']
    if len(second_result.index>0):
        second_result = second_result[col]
    return second_result


def find_stuff_third_table(driver, company, list_name):
    third_result = pd.DataFrame()
    window_before = driver.window_handles[1]
    driver.find_element_by_xpath('//div[contains(@tyc-event-ch,"CompanyDetail.qiyetupu.Detail")]').click()
    WebDriverWait(driver, 3)
    window_after = driver.window_handles[2]
    driver.switch_to.window(window_after)


    iframe = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(iframe)
    time.sleep(1)
    find_tag = driver.find_elements_by_tag_name('g')
    stock_owner_list = []
    employ_list = []
    hstock_owner = []
    invest_list=[]
    branch_list=[]
    hoper_list = []
    driver.find_element_by_css_selector('#graph-web-toolbar > ul > li:nth-child(3)').click()
    driver.find_element_by_css_selector('#graph-web-toolbar > ul > li:nth-child(3)').click()
    driver.find_element_by_css_selector('#graph-web-toolbar > ul > li:nth-child(3)').click()
    for each_tag in find_tag:
        if each_tag.get_attribute('class') == 'holder-node pointer':
            text_list =each_tag.find_elements_by_tag_name('text')
            text = ''
            for i in text_list:
                text = text+i.text+','
            stock_owner_list.append(text)
        if each_tag.get_attribute('class') == 'executives-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            employ_list.append(text)
        if each_tag.get_attribute('class') =='history-holder-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            hstock_owner.append(text)
        if each_tag.get_attribute('class') =='invest-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            invest_list.append(text)
        if each_tag.get_attribute('class') =='branch-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            branch_list.append(text)
        if each_tag.get_attribute('class') =='hoper-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            hoper_list.append(text)
    #third_result_update = append_content(stock_owner_list, third_result, 'stock_owner', 'portion')
    #third_result_update = append_content(employ_list, third_result_update, 'employ', 'job')
    third_result_update = append_content_column(stock_owner_list, third_result, 'stock_owner')
    third_result_update = append_content_column(employ_list, third_result_update, 'employee')
    third_result_update = append_content_column(hstock_owner, third_result_update,'hstock_owner')
    third_result_update = append_content_column(invest_list,third_result_update,'invest')
    third_result_update = append_content_column(branch_list, third_result_update, 'branch')
    third_result_update = append_content_column(hoper_list,third_result_update,'hoper')
    third_result_update['company'] = company
    third_result_update['list_name'] = list_name
    col = ['company','stock_owner', 'employee', 'hstock_owner', 'invest', 'branch', 'hoper', 'list_name']
    third_result_update = third_result_update[col]
    driver.close()
    driver.switch_to.window(window_before)
    driver.close()
    return third_result_update


def find_stuff_forth_table(driver, company, list_name):
    forth_result = pd.DataFrame(columns=['company','name', 'position', 'list_name'])
    tr = driver.find_elements_by_css_selector('#_container_staff > div > table > tbody > tr')
    for each_tr in tr:
        name = each_tr.find_elements_by_xpath('.//td[2]')
        name = name[-1].text
        position_1 = each_tr.find_elements_by_xpath('.//td[3]')
        position = position_1[-1].text
        data = {'company': company,'name': name, 'position': position, 'list_name':list_name}
        forth_result = forth_result.append(data,ignore_index=True)
    return forth_result


def find_stuff_fifth_table(driver, company, list_name):
    fifth_result = pd.DataFrame(columns = ['company','name', 'proportion', 'money', 'list_name'])
    tr = driver.find_elements_by_css_selector('#_container_holder > table > tbody > tr')
    for each_tr in tr:
        name = each_tr.find_element_by_xpath('.//td[2]/table/tbody/tr/td[2]/a').text
        proportion = each_tr.find_element_by_xpath('.//td[3]/div/div/span').text
        money = each_tr.find_element_by_xpath('.//td[4]/div/span').text

        data = {'company': company, 'name': name, 'proportion': proportion,'money':money, 'list_name': list_name}
        fifth_result= fifth_result.append(data, ignore_index=True)
    return fifth_result


def find_stuff_sixth_table(driver, company, list_name):
    sixth_result = pd.DataFrame(columns=['company', 'brunch', 'represent', 'date', 'statue','list_name'])
    tr = driver.find_elements_by_css_selector('#_container_branch > table > tbody > tr')
    for each_tr in tr:

        brunch = each_tr.find_element_by_xpath('.//td[2]/table/tbody/tr/td[2]/a').text

        print(brunch)
        represent = each_tr.find_elements_by_xpath('.//td[3]')[0].text
        print(represent)
        date = each_tr.find_element_by_xpath('.//td[4]/span').text
        print(date)
        statue =  each_tr.find_element_by_xpath('.//td[5]/span').text
        print(statue)
        data = {'company': company, 'brunch': brunch, 'represent': represent, 'date': date, 'statue': statue, 'list_name': list_name}
        sixth_result = sixth_result.append(data, ignore_index=True)
    print(sixth_result)
    return sixth_result


def append_content_column(waiting_list,df,var1):
    i=0
    while i<len(waiting_list):
        df.at[i, var1] = waiting_list[i]
        i=i+1
    if len(waiting_list)<1:
        df.at[0, var1] = None
    return df


def check_robort(driver, num):
    src = driver.page_source
    text_found = re.search(r'看不清，点击', src)
    if text_found !=None:
        print('*robot error*')
        print('-current is:' + str(num) + '-')
        time.sleep(60)
        driver.delete_all_cookies()
        driver.quit()
        open_ip(num)


def check_handels(driver, num):
    if len(driver.window_handles)> 1:
        print('*handle error*')
        print('-current is:' + str(num) + '-')
        handles = driver.window_handles
        for i in handles[1:]:
            driver.switch_to_window(i)
            driver.close()
        driver.switch_to_window(handles[0])
    return driver


def check_second_robort(driver, num):
    try:
        if driver.find_element_by_css_selector('#web-content > div > div.container > div > div > div.module.module1.module2.loginmodule.collapse.in > div.scan-box > div.scan-wrapper > div.scan-img > img'):
            print('*log_in error*')
            print('-current is:' + str(num)+'-')
            driver.delete_all_cookies()
            driver.quit()
            #open_ip(num)
    except:
        pass



open_ip(num=1172)
