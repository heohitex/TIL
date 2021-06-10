list = pd.read_excel('./##파일명##.xlsx')
url = "https://manage.searchad.naver.com/customers/##키워드플래너고유NO##/tool/keyword-planner" #본인 쓰는 계정 URL로 변경필요


results = [ ]
for keyword in list['##컬럼명##']:
    browser.get(url)
    time.sleep(1)
    searching_word = browser.find_elements_by_css_selector('textarea.form-control')[0]
    searching_word.send_keys(keyword)
    browser.find_elements_by_css_selector('button.btn-primary')[0].click()
    time.sleep(1)
    browser.find_elements_by_css_selector('elena-keyword')[0].click()
    time.sleep(1)
    m_point_list = browser.find_elements_by_css_selector('g.highcharts-series-1>path.highcharts-point')
    pc_point_list = browser.find_elements_by_css_selector('g.highcharts-series-0>path.highcharts-point')
    try:
        m_point_list[0].click()
        for n in range(0,12):
            m_point_list[n].click()
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            query = soup.select('tr > td:nth-child(2) > strong')[0].text
            date = soup.select('div > span > div > div > strong')[0].text
            data = [keyword,'mobile',query,date]
            results.append(data)
        for n in range(0,12):
            try:
                pc_point_list[n].click()
            except:
                m_point_list[n].click()
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            query = soup.select('tr > td:nth-child(2) > strong')[0].text
            date = soup.select('div > span > div > div > strong')[0].text
            data = [keyword,'desktop',query,date]
            results.append(data)
    except:
        print(keyword , 'Skip')

df = pd.DataFrame(results)
df.columns = ['keyword','device','query','month']
df.to_excel('.\완성\##저장될 파일명##.xlsx') #저장될파일명
    
