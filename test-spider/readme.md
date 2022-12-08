# [REF] Build a clawer using selenium

- **Metadata** : `type: REF` `scope: Selenium` 
- **Techs Need** : `python`
- **Status** : `done`

## ✨ You should already know

> Selenium 是一個瀏覽器控制套件，通常可以作為網頁整合測試的工具。
👩‍💻 👨‍💻

## ✨ About the wiki

- `Situation:`  我們需要透過瀏覽器來蒐集網頁內容資料
- `Target:`  一個包含蒐集資料和儲存資料的框架
- `Index:`

| Sub title | decription | memo |
| ------ | ------ | ------ |
| main.py | descript how to run a job | -- |
| driverTool.py  | -- | -- |
| actionDefination.py  | -- | -- |



## ✨  Sections

<br/>

---
### **主要執行(main.py)**
> 進入點
####  📝 1. 透過`瀏覽器驅動模組`來初始化瀏覽器
```
cm: RemoteDriverConfig = {
  "hostUrl": "http://selenium:4444",
  "chromeVersion": "107.0",
  "platformType": "Linux"
}
driver: webdriver.Remote = initRemoteDriver(cm)
```

####  📝 2. 根據`任務架構模組`來宣告任務
> 根據需求，宣告任務的每一步驟。
```
tests: List[ActionConfig] = [
  {
    "target": "go",
    "execute": "none",
    "targetArgs": "https://news.google.com/topstories?hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "executeArgs": "",
  },
  {
    "target": "findElementByContainText",
    "execute": "click",
    "targetArgs": "頭條新聞|發燒新聞",
    "executeArgs": "",
  },
]
```

####  📝 3. 使用`任務執行模組`來驅動任務
> 這邊指要求依序執行，根據需求可以使用`storage`回傳的資料做決策點，從此達到分岔路線的功能
```
def runSteps(d: webdriver.Remote, ts: List[ActionConfig]) -> webdriver.Remote:
	storage: ActionStorge = {"store": {}}
	for c in ts:
		print(c["target"], c["targetArgs"])
		# print(f"Windows: {d.window_handles}")
		storage = runAction(d, storage, c)
	return d
```


<br/>

---
### **driverTool.py**
> 透過`selenium`來驅動chrome

####  📝 1. 定義`瀏覽器驅動模塊`
> 定義初始化`瀏覽器驅動模塊`所需輸入與初始化步驟
```
class RemoteDriverConfig(TypedDict):
  hostUrl: str
  chromeVersion: str
  platformType: str
  
def initRemoteDriver(c: RemoteDriverConfig) -> webdriver.Remote:
  chrome_options = webdriver.ChromeOptions()
  chrome_options.set_capability("browserVersion", c["chromeVersion"])  #type: ignore
  chrome_options.set_capability("platformName", c["platformType"])  #type: ignore
  chrome_options.add_argument("ignore-certificate-errors")  #type: ignore
  chrome_options.add_argument('--disable-notifications')  #type: ignore
  chrome_options.add_argument('--disable-gpu')  #type: ignore
  chrome_options.add_argument('--headless')  #type: ignore


  # chrome_options.add_experimental_option("prefs",{"profile.default_content_setting_values.notifications" : 2})  #type: ignore
  driver = webdriver.Remote(command_executor=c["hostUrl"], options=chrome_options)
  driver.implicitly_wait(5)  # seconds
  driver.set_page_load_timeout(25) # seconds
  return driver

```
####  📝 2. 定義`任務架構模組`
> 定義`任務架構模組`所有結構
```
class ActionConfig(TypedDict):
  target: ActionFuncDefinitionLabel
  execute: ActionFuncDefinitionLabel
  targetArgs: str
  executeArgs: str


class ActionStorge(TypedDict):
  store: Dict[str, Any]
  


```
####  📝 3. 定義`任務執行模組`
> 定義`任務執行模組`如何執行任務內容步驟
> `任務執行模組`會根據任務內容來`任務範本模組`進行組合，透過`文字標籤`取得實際執行程式的方式。
> `任務執行模組` 需取得兩種任務模組，分別是`任務範本定位模組`和`任務範本執行模組`
```

def exchangeLocateFunc(label: ActionFuncDefinitionLabel) -> ActionLocateFunc:
  return defaultActionLocateFuncMap[label]


def exchangeExecuteFunc(label: ActionFuncDefinitionLabel) -> ActionExecuteFunc:
  return defaultActionExecuteFuncMap[label]


def runAction(driver: webdriver.Remote, storage: ActionStorge,
              config: ActionConfig) -> ActionStorge:
  locate = exchangeLocateFunc(config["target"])
  execute = exchangeExecuteFunc(config["execute"])

  ##
  eles = locate(driver, config["targetArgs"])
  result = execute(eles, config["executeArgs"])
  storage['store'].update(result)
  return storage


```








<br/>

---
### **actionDefination.py**
> `任務範本模組`負責定義任務的實際執行內容


####  📝 1.`任務範本模組`結構定義
```
ActionFuncDefinitionLabel = str

ActionLocateFunc = Callable[[webdriver.Remote, str], List[WebElement]]
ActionLocateFuncMap = Dict[ActionFuncDefinitionLabel, ActionLocateFunc]

ActionExecuteFuncMap = Dict[ActionFuncDefinitionLabel, ActionExecuteFunc]
ActionExecuteFunc = Callable[[List[WebElement], str], Dict[str, Any]]

```

####  📝 2.`任務範本定位模組`的定義與宣告
> `任務範本定位模組`主要是在頁面上找尋特定元素的任務
> 也負責部分簡單行為，例如網頁導向、等待時間等

- 定義任務執行內容
```

def findElementsByXpath(driver: webdriver.Remote,target: str) -> List[WebElement]:
  return driver.find_elements(By.XPATH, target)  # type: ignore


def findLastElementsByXpath(driver: webdriver.Remote, target: str) -> List[WebElement]:
  return driver.find_elements(By.XPATH, f"({target})[last()]")  # type: ignore


def goToPage(driver: webdriver.Remote, target: str) -> List[WebElement]:
  driver.get(target)
  return []


def waitSec(driver: webdriver.Remote, target: str) -> List[WebElement]:
  time.sleep(int(target))
  return []


def switchLatestWindow(driver: webdriver.Remote,target: str) -> List[WebElement]:
  maxTime = 0
  while len(driver.window_handles) == 1 and maxTime < 20:
    time.sleep(0.3)
    maxTime += 1
  driver.switch_to.window(driver.window_handles[-1])  #type: ignore
  return []


def switchDefaultWindow(driver: webdriver.Remote, target: str) -> List[WebElement]:
  driver.switch_to.window(driver.window_handles[0])  #type: ignore
  return []


def switchAlertWindow(driver: webdriver.Remote, target: str) -> List[WebElement]:
  driver.switch_to.alert  #type: ignore
  return []

```

- 定義任務執行與任務標籤之定義物件
```
defaultActionLocateFuncMap: ActionLocateFuncMap = {
  "findElementByXpath": findElementsByXpath,
  "findLastElementsByXpath": findLastElementsByXpath,
  "findButtonByContainText": lambda d, target: to1D([findElementsByXpath(d, f"//button[contains(.,'{t}')]")for t in target.split("|")]),
  "findLinkByContainText": lambda d, target: to1D([findElementsByXpath(d, f"//a[contains(.,'{t}')]")for t in target.split("|")]),
  "findElementByContainText": lambda d, target: to1D([findElementsByXpath(d, f"//*[contains(.,'{t}')]")for t in target.split("|")]),
  "findInputById": lambda d, target: to1D([findElementsByXpath(d, f"//input[@id='{t}']") for t in target.split("|")]),
  "findElementById": lambda d, target: to1D([findElementsByXpath(d, f"//*[@id='{t}']") for t in target.split("|")]),
  "go": goToPage,
  "waitSec": waitSec,
  "switchLatestWindow": switchLatestWindow,
  "switchAlertWindow": switchAlertWindow,
  "switchDefaultWindow": switchDefaultWindow,
}
```

####  📝 3.`任務範本執行模組`的定義與宣告
> `任務範本執行模組`主要針對頁面上特定元素的執行行為的任務
> 也是主要更新任務回傳資料的部分。

- 定義任務執行內容
```
def confirmElementIsSingle(elements: List[WebElement], agrs: str) -> None:
  if len(elements) > 1:
    raise ValueError("CAN'T CLICK MULTI BUTTON IN THE SAME TIME")


def clickElement(elements: List[WebElement], agrs: str) -> Dict[str, Any]:
  # print(f"elements:{elements}")
  elements[0].click()
  return {}


def clickAllElement(elements: List[WebElement], agrs: str) -> Dict[str, Any]:
  # print(f"elements:{elements}")
  for e in elements:
    e.click()
  return {}


def typingElement(elements: List[WebElement], agrs: str) -> Dict[str, Any]:
  elements[0].send_keys(agrs)  # type: ignore
  return {}

def saveAttribute(elements: List[WebElement], agrs: str) -> Dict[str, Any]:
  returnArr: List[str] = []
  for e in elements:
    returnArr.append(e.get_attribute(agrs))# type: ignore
  return {
    agrs: returnArr
  }

def saveContent(elements: List[WebElement], agrs: str) -> Dict[str, Any]:
  return {
    agrs: [e.text for e in elements]

```

- 定義任務執行與任務標籤之定義物件
```
defaultActionExecuteFuncMap: ActionExecuteFuncMap = {
  "click": clickElement,
  "clickAll": clickAllElement,
  "saveContent": saveContent,
  "saveLink": lambda es, a: saveAttribute(es,'href'),
  "saveByAttr": saveAttribute,
  "typing": typingElement,
  "none": lambda es, a: {},
}
```







