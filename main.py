# main.py
from driverTool import RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, ActionConfig
from commonTool import cleanHtml, loadJsonFile
from selenium import webdriver
from driverTool import ActionConfig, ActionStorge, RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, runAction
from typing import List, Tuple, Dict
import json
# from crawlab import save_item
# from db import save_item_to_kibana
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
try:
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
  # print(f"storage: {storage}")
  topic_links: List[str] = storage["store"]['href']
  for topic_url in topic_links[-3:]:
    driver, storage = runSteps(driver,[{
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
          "execute": "saveContent",
          "targetArgs": "//*[@id='format0_disparea']/tbody/tr[4]/td",
          "executeArgs": "title"
        },
        {
          "target": "findElementByXpath",
          "execute": "saveByAttr",
          "targetArgs": "//td[contains(@class, 'stdncl2')]/div",
          "executeArgs": "innerHTML"
        }
      ])
      
      # links: List[str] = storage["store"]['href']
      # print(f"storage: {storage['store']['title']}")
      # print(f"storage: {[cleanHtml(text) for text in storage['store']['innerHTML']]}")
      body = {colName: cleanHtml(text) for colName, text in zip(["summary_zh","summary_en","sections","reference"],storage['store']['innerHTML'][:5])}
      body['title']= storage['store']['title'][0]
      print(body)
      raise RuntimeError

      # save_item(result)
      # save_item_to_kibana(result)
  time.sleep(15)
  quitRemoteDriver(driver)
except Exception as e:
  print(f"ERROR: {e}")
  quitRemoteDriver(driver)