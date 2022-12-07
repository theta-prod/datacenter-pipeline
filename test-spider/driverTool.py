# DriverTool
from typing import TypedDict, Dict, Any, Tuple
from selenium import webdriver
from actionDefination import ActionFuncDefinitionLabel, ActionLocateFunc, ActionExecuteFunc, defaultActionLocateFuncMap, defaultActionExecuteFuncMap


class RemoteDriverConfig(TypedDict):
  hostUrl: str
  chromeVersion: str
  platformType: str


class ActionConfig(TypedDict):
  target: ActionFuncDefinitionLabel
  execute: ActionFuncDefinitionLabel
  targetArgs: str
  executeArgs: str


class ActionStorge(TypedDict):
  store: Dict[str, Any]


def initRemoteDriver(c: RemoteDriverConfig) -> webdriver.Remote:
  chrome_options = webdriver.ChromeOptions()
  chrome_options.set_capability("browserVersion",
                                c["chromeVersion"])  #type: ignore
  chrome_options.set_capability("platformName",
                                c["platformType"])  #type: ignore
  chrome_options.add_argument("ignore-certificate-errors")  #type: ignore

  driver = webdriver.Remote(command_executor=c["hostUrl"],
                            options=chrome_options)
  driver.implicitly_wait(25)  # seconds
  return driver


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


def quitRemoteDriver(driver: webdriver.Remote):
  driver.quit()
