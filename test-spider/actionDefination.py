from typing import  List, Dict, Any, Callable
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

### ActionLocate_Definition
def findElementsByXpath(driver: webdriver.Remote, target: str) -> List[WebElement]: 
    print(f"findElements:XPATH:{target}")
    return driver.find_elements(By.XPATH, target) 

def goToPage(driver: webdriver.Remote, target: str) -> List[WebElement]: 
    driver.get(target)
    return []

def waitSec(driver: webdriver.Remote, target: str) -> List[WebElement]: 
    time.sleep(int(target))
    return []




defaultActionLocateFuncMap: ActionLocateFuncMap = {
    "findElementByXpath": findElementsByXpath,
    "findLinkByContainText": lambda d, target: to1D([findElementsByXpath(d, f"//a[contains(.,'{t}')]") for t in target.split("|")]),
    "findElementByContainText": lambda d, target: to1D([findElementsByXpath(d, f"//*[contains(.,'{t}')]") for t in target.split("|")]),
    "go": goToPage,
    "waitSec": waitSec
}


### ActionExecute_Definition
def confirmElementIsSingle(elements: List[WebElement]) -> None: 
    if len(elements) > 1:
        raise ValueError("CAN'T CLICK MULTI BUTTON IN THE SAME TIME")
def confirmElementIsExist(elements: List[WebElement]) -> None: ...

def clickElement(elements: List[WebElement]) -> Dict[str, Any]:
    elements[0].click()
    return {}
    
defaultActionExecuteFuncMap: ActionExecuteFuncMap = {
    "clickElement": clickElement,
    "saveContent": lambda es: {
         "article_titles":[e.text for e in es if e.text != '']
    },
    "none": lambda es: {},
}