from typing import TypedDict, List, Callable, Dict, Any
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from commonTool import to1D
import time

ActionFuncDefinitionLabel = str
ActionLocateFunc = Callable[[webdriver.Remote, str], List[WebElement]]
ActionExecuteFunc = Callable[[List[WebElement]], Dict[str, Any]]
ActionLocateFuncMap = Dict[ActionFuncDefinitionLabel, ActionLocateFunc]
ActionExecuteFuncMap = Dict[ActionFuncDefinitionLabel, ActionExecuteFunc]

class RemoteDriverConfig(TypedDict):
    hostUrl: str
    chromeVersion: str
    platformType: str

class ActionConfig(TypedDict):
    target: ActionFuncDefinitionLabel
    execute: ActionFuncDefinitionLabel
    args: str

class ActionStorge(TypedDict):
    store: Dict[str, Any]

def initRemoteDriver(c: RemoteDriverConfig) -> webdriver.Remote: 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.set_capability("browserVersion", c["chromeVersion"]) #type: ignore
    chrome_options.set_capability("platformName", c["platformType"]) #type: ignore

    driver = webdriver.Remote(
        command_executor = c["hostUrl"],
        options= chrome_options
    )
    driver.implicitly_wait(25) # seconds
    return driver


def exchangeLocateFunc(label: ActionFuncDefinitionLabel) -> ActionLocateFunc: 
    return defaultActionLocateFuncMap[label]

def exchangeExecuteFunc(label: ActionFuncDefinitionLabel) -> ActionExecuteFunc: 
    return defaultActionExecuteFuncMap[label]



def runAction(driver: webdriver.Remote, storage: ActionStorge, config: ActionConfig) -> ActionStorge: 
    locate = exchangeLocateFunc(config["target"])
    execute = exchangeExecuteFunc(config["execute"])

    ##
    eles: List[WebElement] = locate(driver,config["args"])
    result = execute(eles)
    storage['store'].update(result)
    return storage
def quitRemoteDriver(driver: webdriver.Remote):
    driver.quit()


###
###
###
### ActionLocate_Definition
def findElementsByXpath(driver: webdriver.Remote, target: str) -> List[WebElement]: 
    print(f"findElements:XPATH:{target}")
    return driver.find_elements(By.XPATH, target) 

def gotopage(driver: webdriver.Remote, target: str) -> List[WebElement]: 
    driver.get(target)
    return []

def wait_sec(driver: webdriver.Remote, target: str) -> List[WebElement]: 
    time.sleep(int(target))
    return []




defaultActionLocateFuncMap: ActionLocateFuncMap = {
    "findElementByXpath": findElementsByXpath,
    "findLinkByContainText": lambda d, target: to1D([findElementsByXpath(d, f"//a[contains(.,'{t}')]") for t in target.split("|")]),
    "findElementByContainText": lambda d, target: to1D([findElementsByXpath(d, f"//*[contains(.,'{t}')]") for t in target.split("|")]),
    "go": gotopage,
    "waitSec": wait_sec
}





### ActionExecute_Definition
def confirmElementIsSingle(elements: List[WebElement]) -> None: 
    if len(elements) > 1:
        raise ValueError("CAN'T CLICK MULTI BUTTON IN THE SAME TIME")
def confirmElementIsExist(elements: List[WebElement]) -> None: ...

def clickElement(elements: List[WebElement]) -> Dict[str, Any]:
    # confirmElementIsSingle(elements)
    elements[0].click()
    return {}
    
defaultActionExecuteFuncMap: ActionExecuteFuncMap = {
    "clickElement": clickElement,
    "saveContent": lambda es: {
         "article_titles":[e.text for e in es if e.text != '']
    },
    "none": lambda es: {},
}