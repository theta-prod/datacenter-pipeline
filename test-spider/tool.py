from typing import TypedDict, List, Callable, Dict, Any
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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
    args: List[str]

class ActionStorge(TypedDict):
    store: Dict[str, Any]

def initRemoteDriver(c: RemoteDriverConfig) -> webdriver.Remote: 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.set_capability("browserVersion", c["chromeVersion"]) #type: ignore
    chrome_options.set_capability("platformName", c["platformType"]) #type: ignore

    return webdriver.Remote(
        command_executor = c["hostUrl"],
        options= chrome_options
    )


def exchangeLocateFunc(label: ActionFuncDefinitionLabel) -> ActionLocateFunc: 
    return defaultActionLocateFuncMap[label]

def exchangeExecuteFunc(label: ActionFuncDefinitionLabel) -> ActionExecuteFunc: 
    return defaultActionExecuteFuncMap[label]



def runAction(driver: webdriver.Remote, storage: ActionStorge, config: ActionConfig) -> ActionStorge: 
    locate = exchangeLocateFunc(config["target"])
    execute = exchangeExecuteFunc(config["execute"])
    eles: List[WebElement] = locate(driver,*config["args"])
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
    return lambda: driver.find_elements(By.XPATH, target) # type: ignore

def gotopage(driver: webdriver.Remote, target: str) -> List[WebElement]: 
    driver.get(target)
    return []

def wait_sec(driver: webdriver.Remote, target: str) -> List[WebElement]: 
    WebDriverWait(driver, int(target))
    return []
    



defaultActionLocateFuncMap: ActionLocateFuncMap = {
    "findElementsByXpath": findElementsByXpath,
    "findElementsByContentText": lambda d, t: findElementsByXpath(d, t),
    "findElementByContentText": lambda d, t: findElementsByXpath(d, f"//*[contains(.,'{t}')]"),
    "go": gotopage,
    "waitSec": wait_sec
}





### ActionExecute_Definition
def confirmElementIsSingle(elements: List[WebElement]) -> None: 
    if len(elements) > 1:
        raise ValueError("CAN'T CLICK MULTI BUTTON IN THE SAME TIME")
def confirmElementIsExist(elements: List[WebElement]) -> None: ...

def clickElement(elements: List[WebElement]) -> Dict[str, Any]:
    confirmElementIsSingle(elements)
    elements[0].click()
    return {}
    
defaultActionExecuteFuncMap: ActionExecuteFuncMap = {
    "clickElement": clickElement,
    "none": lambda es: {},
}