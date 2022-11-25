# ActionDefination
from typing import List, Dict, Any, Callable
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from commonTool import to1D
import time

ActionFuncDefinitionLabel = str
ActionLocateFunc = Callable[[webdriver.Remote, str], List[WebElement]]
ActionExecuteFunc = Callable[[List[WebElement], str], Dict[str, Any]]
ActionLocateFuncMap = Dict[ActionFuncDefinitionLabel, ActionLocateFunc]
ActionExecuteFuncMap = Dict[ActionFuncDefinitionLabel, ActionExecuteFunc]

### ActionLocate_Definition


def findElementsByXpath(driver: webdriver.Remote,
                        target: str) -> List[WebElement]:
  return driver.find_elements(By.XPATH, target)  # type: ignore


def findLastElementsByXpath(driver: webdriver.Remote,
                            target: str) -> List[WebElement]:
  return driver.find_elements(By.XPATH, f"({target})[last()]")  # type: ignore


def goToPage(driver: webdriver.Remote, target: str) -> List[WebElement]:
  driver.get(target)
  return []


def waitSec(driver: webdriver.Remote, target: str) -> List[WebElement]:
  time.sleep(int(target))
  return []


def switchLatestWindow(driver: webdriver.Remote,
                       target: str) -> List[WebElement]:
  maxTime = 0
  while len(driver.window_handles) == 1 and maxTime < 20:
    time.sleep(0.3)
    maxTime += 1
  driver.switch_to.window(driver.window_handles[-1])  #type: ignore
  return []


def switchDefaultWindow(driver: webdriver.Remote,
                        target: str) -> List[WebElement]:
  driver.switch_to.window(driver.window_handles[0])  #type: ignore
  return []


def switchAlertWindow(driver: webdriver.Remote,
                      target: str) -> List[WebElement]:
  driver.switch_to.alert  #type: ignore
  return []


defaultActionLocateFuncMap: ActionLocateFuncMap = {
  "findElementByXpath":
  findElementsByXpath,
  "findLastElementsByXpath":
  findLastElementsByXpath,
  "findButtonByContainText":
  lambda d, target: to1D([
    findElementsByXpath(d, f"//button[contains(.,'{t}')]")
    for t in target.split("|")
  ]),
  "findLinkByContainText":
  lambda d, target: to1D([
    findElementsByXpath(d, f"//a[contains(.,'{t}')]")
    for t in target.split("|")
  ]),
  "findElementByContainText":
  lambda d, target: to1D([
    findElementsByXpath(d, f"//*[contains(.,'{t}')]")
    for t in target.split("|")
  ]),
  "findInputById":
  lambda d, target: to1D(
    [findElementsByXpath(d, f"//input[@id='{t}']")
     for t in target.split("|")]),
  "findElementById":
  lambda d, target: to1D(
    [findElementsByXpath(d, f"//*[@id='{t}']") for t in target.split("|")]),
  "go":
  goToPage,
  "waitSec":
  waitSec,
  "switchLatestWindow":
  switchLatestWindow,
  "switchAlertWindow":
  switchAlertWindow,
  "switchDefaultWindow":
  switchDefaultWindow,
}


### ActionExecute_Definition
def confirmElementIsSingle(elements: List[WebElement], agrs: str) -> None:
  if len(elements) > 1:
    raise ValueError("CAN'T CLICK MULTI BUTTON IN THE SAME TIME")


def confirmElementIsExist(elements: List[WebElement], agrs: str) -> None:
  ...


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


defaultActionExecuteFuncMap: ActionExecuteFuncMap = {
  "click": clickElement,
  "clickAll": clickAllElement,
  "saveContent": lambda es, a: {
    "article_titles": [e.text for e in es if e.text != '']
  },
  "typing": typingElement,
  "none": lambda es, a: {},
}