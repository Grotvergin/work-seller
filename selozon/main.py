from selozon.source import *


@Inspector(NAME)
def Main() -> None:
    service = BuildService()
    config, sections = ParseConfig(NAME)
    driver = CreateDriver()
    sheet_id = config['DEFAULT']['SheetID']
    cities = GetColumn('A', service, 'Cities', sheet_id)
    driver.get('https://seller.ozon.ru/app/analytics/search-results/explainer')
    for heading in sections:
        Stamp(f'Processing {heading}', 'b')
        row = 2
        column = config[heading]['Column']
        CleanSheet(len(COLUMNS), heading, sheet_id, service)
        words = GetColumn(column, service, 'Words', sheet_id)
        cab_num = ord(column) - ord('A') + 2
        for dataset in GetData(driver, cab_num, cities, words):
            UploadData(dataset, heading, sheet_id, service, row)
            row += SmartLen(dataset)
    KillDriver(driver)


def GetData(driver: undetected_chromedriver.Chrome, cab_num: int, cities: list, words: list) -> Generator:
    Sleep(SLEEP_CLICK, 0.5)
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div/div[1]/div/span').click()
    Sleep(SLEEP_CLICK, 0.5)
    driver.find_element(By.XPATH, f'//div[4]/div/div/div/div/div/div/div/div[{cab_num}]').click()
    Sleep(SLEEP_CLICK, 0.5)
    for word in words:
        for city in cities:
            Stamp(f'Processing word <<{word}>> city <<{city}>>', 'i')
            Sleep(SLEEP_CLICK, 0.5)
            pole_for_word = driver.find_element(By.XPATH, "//input[@placeholder='Например, iphone 12 pro']")
            pole_for_word.clear()
            pole_for_word.send_keys(word)
            Sleep(SLEEP_CLICK, 0.5)
            driver.find_element(By.XPATH, "//input[@placeholder='Введите любой город / область']").send_keys(city)
            Sleep(SLEEP_CLICK, 0.5)
            driver.find_element(By.XPATH,"//div[@class='tippy-content']/div/div/div/div/div/div/div/div").click()
            Sleep(SLEEP_CLICK, 0.5)
            driver.find_element(By.XPATH, "//span[contains(., 'Показать результат')]").click()
            wait = WebDriverWait(driver, MAX_TIME_TABLE)
            wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@value='']")))
            Stamp('Table appeared', 's')
            Sleep(SLEEP_CLICK, 0.5)
            driver.find_element(By.XPATH, "//input[@value='']").click()
            Sleep(SLEEP_CLICK, 0.5)
            result = driver.find_element(By.XPATH, "//div[@id='result-list']/div[2]/div/div[1]/table/tbody")
            Sleep(SLEEP_CLICK, 0.5)
            table = parseHtmlTable(result.get_attribute('innerHTML'))
            Sleep(SLEEP_CLICK, 0.5)
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
    chromedriver_autoinstaller.install()
    SuppressException(undetected_chromedriver)
    options = undetected_chromedriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=C:\Users\Рома\AppData\Local\Google\Chrome\User Data')
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36')
    driver = undetected_chromedriver.Chrome(options=options)
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


def parseHtmlTable(html):
    parser = MyHTMLParser()
    parser.feed(html)
    return parser.fullList


if __name__ == '__main__':
    Main()
