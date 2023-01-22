# 
# main.py
from driverTool import RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, ActionConfig
from commonTool import cleanHtml, loadJsonFile
from selenium import webdriver
from driverTool import ActionConfig, ActionStorge, RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, runAction
from typing import List, Tuple, Dict, Any
import json
# from crawlab import save_item
# from db import save_item_to_kibana, closeDB
import time


cm: RemoteDriverConfig = {
  "hostUrl": "http://140.115.126.20:8000",
  "chromeVersion": "108.0",
  "platformType": "Linux"
}
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
driver.implicitly_wait(5)

page_link = "https://hdl.handle.net/11296/89j8te"
driver, storage = runSteps(driver,[{
    "target": "go",
    "execute": "none",
    "targetArgs": page_link,
    "executeArgs": ""
},
{
    "target": "waitSec",
    "execute": "none",
    "targetArgs": "1",
    "executeArgs": ""
},
{
    "target": "findElementByXpath",
    "execute": "saveByAttr",
    "targetArgs": "//input[@id='fe_text1']",
    "executeArgs": "value"
},
{
    "target": "ex_findContentBlock",
    "execute": "saveContent",
    "targetArgs": "外文摘要",
    "executeArgs": "research.sum_en"
},
{
    "target": "ex_findContentBlock",
    "execute": "saveContent",
    "targetArgs": "摘要",
    "executeArgs": "research.sum_zh"
},
{
    "target": "ex_findContentBlock",
    "execute": "saveContent",
    "targetArgs": "目次",
    "executeArgs": "research.sessions"
},
{
    "target": "ex_findContentBlock",
    "execute": "saveContent",
    "targetArgs": "參考文獻",
    "executeArgs": "research.ref"
},])
    
# links: List[str] = storage["store"]['href']
# print(f"storage: {storage['store']}")
colNames = ["research.ref","research.sessions","research.sum_zh","research.sum_en"]
result = {}
for c in colNames:
    if len(storage['store'][c])>0:
        result[c] = storage['store'][c][0]
    result["research.link"] = storage['store']['value'][0]
    result["research.title"] = driver.title
print(result)

quitRemoteDriver(driver)