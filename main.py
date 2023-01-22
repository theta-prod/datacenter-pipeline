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
# goHomePage: List[ActionConfig] = loadJsonFile("news-chdtv-politic-homepage.json")
# goNextPage: List[ActionConfig] = loadJsonFile("news-chdtv-politic-nextpage.json")
# driver = initRemoteDriver(cm)
# Links: List[str] = []
# try:
#   driver, storage = runSteps(driver, goHomePage)
#   Links.extend(storage["store"]["href"])
# except Exception as e:
#   print(e) 
  


# try:
#     for _ in range(3):
#       driver, storage = runSteps(driver, goNextPage)
#       Links.extend(storage["store"]["href"])
# except Exception as e:
#   print(e) 
# finally:
#   quitRemoteDriver(driver)


###
###
###

driver = initRemoteDriver(cm)
driver.implicitly_wait(2)

try:
  for collectionIdx in range(3,1,-1):
    driver, storage = runSteps(driver,[{
        "target": "go",
        "execute": "none",
        "targetArgs": "https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=d",
        "executeArgs": ""
      },
      {
        "target": "findElementByXpath",
        "execute": "saveLink",
        "targetArgs": "//*[@id='hotlv_disp1']/a",
        "executeArgs": "links"
      }
    ])
    topic_url: str = storage["store"]['href'][-1*collectionIdx]
    driver, storage = runSteps(driver,[
      {
        "target": "go",
        "execute": "none",
        "targetArgs": topic_url,
        "executeArgs": ""
      },
      {
        "target": "findElementByXpath",
        "execute": "saveLink",
        "targetArgs": "//*[contains(@class, 'slink')]",
        "executeArgs": "links"
      }
    ])
    page_links: List[str] = storage["store"]['href']
    # print(f"storage: {storage}")
    for page_link in page_links:
      print(f"page_link: {page_link}")
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
        # {
        #   "target": "findElementByXpath",
        #   "execute": "saveContent",
        #   "targetArgs": "//*[@id='format0_disparea']/tbody/tr[4]/td",
        #   "executeArgs": "research.title"
        # },
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
        },
        
      ])
      
      # links: List[str] = storage["store"]['href']
      # print(f"storage: {storage['store']}")
      colNames = ["research.ref","research.sessions","research.sum_zh","research.sum_en"]
      result = {}
      for c in colNames:
        if len(storage['store'][c])>0:
          result[c] = storage['store'][c][0]
      result["research.link"] = storage['store']['value'][0]
      result["research.title"] = driver.title
      # print(result)

      # save_item(result)
      # save_item_to_kibana(result)
except Exception as e:
  print(f"ERROR: {e}")
# closeDB()
quitRemoteDriver(driver)