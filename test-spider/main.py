# main.py
from driverTool import RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, ActionConfig
from commonTool import loadJsonFile
from selenium import webdriver
from driverTool import ActionConfig, ActionStorge, RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, runAction
from typing import List

cm: RemoteDriverConfig = {
  "hostUrl": "http://127.0.0.1:4444",
  "chromeVersion": "103.0",
  "platformType": "Linux"
}

tests: List[ActionConfig] = [
  {
    "target": "go",
    "execute": "none",
    "targetArgs": "https://......",
    "executeArgs": "",
  },
  {
    "target": "findElementByContainText",
    "execute": "click",
    "targetArgs": "<Button-Label>",
    "executeArgs": "",
  },
]


def runSteps(d: webdriver.Remote, ts: List[ActionConfig]) -> webdriver.Remote:
  storage: ActionStorge = {"store": {}}
  for c in ts:
    print(c["target"], c["targetArgs"])
    # print(f"Windows: {d.window_handles}")
    storage = runAction(d, storage, c)
  print(storage)

  return d


###
###
###

driver = initRemoteDriver(cm)
driver = runSteps(driver, tests)
driver = runSteps(driver, loadJsonFile("Common-wait.json"))
quitRemoteDriver(driver)
