# main.py
from driverTool import RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, ActionConfig
from commonTool import loadJsonFile
from selenium import webdriver
from driverTool import ActionConfig, ActionStorge, RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, runAction
from typing import List, Tuple

cm: RemoteDriverConfig = {
  "hostUrl": "http://selenium:4444",
  "chromeVersion": "107.0",
  "platformType": "Linux"
}

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


def runSteps(d: webdriver.Remote, ts: List[ActionConfig], storage: ActionStorge = {"store": {}}) -> Tuple[webdriver.Remote, ActionStorge]:
  for c in ts:
    print(c["target"], c["targetArgs"])
    # print(f"Windows: {d.window_handles}")
    storage = runAction(d, storage, c)
  # print(storage)
       
  return d, storage


###
###
###

driver = initRemoteDriver(cm)
Links: List[str] = []
try:
  driver, storage = runSteps(driver, tests)
  driver, storage = runSteps(driver, loadJsonFile("Common-wait.json"))
except Exception as e:
  quitRemoteDriver(driver)