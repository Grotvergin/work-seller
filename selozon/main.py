from selozon.source import *


@Inspector(NAME)
def Main() -> None:
    service = BuildService()
    config, sections = ParseConfig(NAME)
    driver = CreateDriver()
    sheet_id = config['DEFAULT']['SheetID']
    cities = GetColumn('A', service, 'Cities', sheet_id)
    driver.get('https://seller.ozon.ru/app/analytics/search-results/explainer')
    row_all = len(GetColumn('A', service, NAME_ALL, sheet_id)) + 2
    for heading in sections:
        Stamp(f'Processing {heading}', 'b')
        row_heading = len(GetColumn('A', service, heading, sheet_id)) + 2
        column = config[heading]['Column']
        words = GetColumn(column, service, 'Words', sheet_id)
        cab_num = ord(column) - ord('A') + 2
        for dataset in GetData(driver, cab_num, cities, words):
            UploadData(dataset, heading, sheet_id, service, row_heading)
            UploadData(dataset, NAME_ALL, sheet_id, service, row_all)
            row_heading += SmartLen(dataset)
            row_all += SmartLen(dataset)
    KillDriver(driver)


@ControlRecursion
def ClickNotification(driver: undetected_chromedriver.Chrome) -> None:
    Stamp(f'Trying to click notification', 'i')
    try:
        notification = driver.find_elements(By.XPATH, '//*[@id="tippy-16"]/div/div[1]/div/div/div[2]/button/div/span')
        if SmartLen(notification) > 0:
            Stamp('Clicking the notification', 'w')
            notification[0].click()
            Sleep(SLEEP_CLICK)
        else:
            Stamp('Notification is absent', 'i')
    except WebDriverException as e:
        Stamp(f'Webdriver error during notification click: {e}', 'e')
        Sleep(MEDIUM_SLEEP)
        ClickNotification(driver)


@ControlRecursion
def ChooseCabinet(driver: undetected_chromedriver.Chrome, cab_num: int) -> None:
    Stamp(f'Trying to choose cabinet <<{cab_num}>>', 'i')
    try:
        driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[1]/div/div/div[1]/div/span').click()
        AccurateSleep(SLEEP_CLICK, 0.4)
        driver.find_element(By.XPATH, f'//div[4]/div/div/div/div/div/div/div/div[{cab_num}]').click()
        AccurateSleep(SLEEP_CLICK, 0.5)
        WebDriverWait(driver, MAX_TIME_TABLE).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@placeholder='Например, iphone 12 pro']")))
        Stamp('Input name appeared after choosing new cabinet', 's')
        AccurateSleep(SLEEP_CLICK, 0.6)
    except WebDriverException as e:
        Stamp(f'Webdriver error during choosing cabinet: {e}', 'e')
        Sleep(MEDIUM_SLEEP)
        ChooseCabinet(driver, cab_num)


@ControlRecursion
def InsertValues(driver: undetected_chromedriver.Chrome, value: str, XPath: str) -> None:
    Stamp(f'Trying to insert value <<{value}>>', 'i')
    try:
        element = driver.find_element(By.XPATH, XPath)
        element.clear()
        element.send_keys(value)
        AccurateSleep(SLEEP_CLICK, 0.6)
    except WebDriverException as e:
        Stamp(f'Webdriver error during inserting values: {e}', 'e')
        Sleep(MEDIUM_SLEEP)
        InsertValues(driver, value, XPath)


def ChooseFirstCity(driver: undetected_chromedriver.Chrome) -> None:
    Stamp('Trying to choose first city', 'i')
    try:
        WebDriverWait(driver, MAX_TIME_TABLE).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='tippy-content']/div/div/div/div/div/div/div/div")))
        driver.find_element(By.XPATH, "//div[@class='tippy-content']/div/div/div/div/div/div/div/div").click()
        AccurateSleep(SLEEP_CLICK, 0.5)
    except WebDriverException as e:
        Stamp(f'Webdriver error during choosing the first city: {e}', 'e')
        Sleep(MEDIUM_SLEEP)
        ChooseFirstCity(driver)


def RequestTable(driver: undetected_chromedriver.Chrome) -> list:
    Stamp('Trying to request table', 'i')
    try:
        driver.find_element(By.XPATH, "//span[contains(., 'Показать результат')]").click()
        WebDriverWait(driver, MAX_TIME_TABLE).until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@value='']")))
        Stamp('Table appeared', 's')
        AccurateSleep(SLEEP_CLICK, 0.5)
        ClickNotification(driver)
        driver.find_element(By.XPATH, "//input[@value='']").click()
        AccurateSleep(SLEEP_CLICK, 0.5)
        result = driver.find_element(By.XPATH, '//*[@id="result-list"]/div[2]/div/div[1]/div/table/tbody')
        AccurateSleep(SLEEP_CLICK, 0.5)
        table = ParseHtmlTable(result.get_attribute('innerHTML'))
        AccurateSleep(SLEEP_CLICK, 0.5)
    except WebDriverException as e:
        Stamp(f'Webdriver error during requesting the table: {e}', 'e')
        Sleep(MEDIUM_SLEEP)
        table = RequestTable(driver)
    return table


def GetData(driver: undetected_chromedriver.Chrome, cab_num: int, cities: list, words: list) -> Generator:
    ChooseCabinet(driver, cab_num)
    for word in words:
        InsertValues(driver, word, "//input[@placeholder='Например, iphone 12 pro']")
        for city in cities:
            InsertValues(driver, city, "//input[@placeholder='Введите любой город / область']")
            ChooseFirstCity(driver)
            table = RequestTable(driver)
            yield ProcessData(table, word, city)


def ProcessData(table: list, word: str, city: str) -> list[list[str]]:
    list_of_rows = []
    for row in table:
        one_row = []
        for key, value in COLUMNS.items():
            if key == 'Word':
                one_row.append(word)
            elif key == 'City':
                one_row.append(city)
            elif key == 'Date':
                one_row.append(datetime.now().strftime('%Y-%m-%d %H:%M'))
            elif key == 'ID':
                match = re.search(r'id:\s*(\d+)', row[value])
                cur_id = match.group(1) if match else 'DataError'
                one_row.append(str(cur_id))
            else:
                one_row.append(str(row[value]))
        list_of_rows.append(one_row)
    return list_of_rows


def KillDriver(driver: undetected_chromedriver.Chrome) -> None:
    driver.close()
    driver.quit()


def CreateDriver() -> undetected_chromedriver.Chrome:
    Stamp('Trying to build driver', 'i')
    chromedriver_autoinstaller.install()
    SuppressException(undetected_chromedriver)
    options = undetected_chromedriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-gpu')
    # options.add_argument(r'--user-data-dir=/root/.config/google-chrome')
    options.add_argument(r'--user-data-dir=C:\Users\Рома\AppData\Local\Google\Chrome\User Data')
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36')
    driver = undetected_chromedriver.Chrome(options=options, version_main=121)
    Stamp('Built driver successfully', 's')
    return driver


def SuppressException(uc: undetected_chromedriver) -> None:
    old_del = uc.Chrome.__del__

    def NewDel(self) -> None:
        try:
            old_del(self)
        except OSError:
            pass
    setattr(uc.Chrome, '__del__', NewDel)


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.tabSpace = ""
        self.tdCount = 0
        self.tdList = [1, 2, 3, 4, 7, 8, 9]
        self.stringData = ""
        self.stingList = []
        self.fullList = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.tdCount = 0
        if tag == "td":
            self.tdCount = self.tdCount + 1
            if self.tdCount not in self.tdList:
                self.inLink = True
                return
        if self.inLink:
            return
        self.tabSpace = self.tabSpace + "    "

    def handle_endtag(self, tag):
        if tag == "td" and self.inLink:
            self.inLink = False
            return
        if self.inLink:
            return
        if tag == "td":
            self.stingList.append(self.stringData)
            self.stringData = ""
        if tag == "tr":
            self.fullList.append(self.stingList)
            self.stingList = []
        self.tabSpace = self.tabSpace[:-4]

    def handle_data(self, data):
        if self.inLink:
            return
        if data not in ["Изменить", "Продвигается", "Поднять"]:
            self.stringData = self.stringData + data


def ParseHtmlTable(html: str) -> List[List[str]]:
    parser = MyHTMLParser()
    parser.feed(html)
    return parser.fullList


if __name__ == '__main__':
    Main()
