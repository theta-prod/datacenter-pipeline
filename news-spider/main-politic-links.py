# main.py
from driverTool import RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, ActionConfig
from commonTool import loadJsonFile
from selenium import webdriver
from driverTool import ActionConfig, ActionStorge, RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, runAction
from typing import List, Tuple, Dict
import json
# from crawlab import save_item



cm: RemoteDriverConfig = {
  "hostUrl": "http://selenium:4444",
  "chromeVersion": "107.0",
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
goHomePage: List[ActionConfig] = loadJsonFile("news-chdtv-politic-homepage.json")
goNextPage: List[ActionConfig] = loadJsonFile("news-chdtv-politic-nextpage.json")
driver = initRemoteDriver(cm)
Links: List[str] = []
try:
  driver, storage = runSteps(driver, goHomePage)
  Links.extend(storage["store"]["href"])
except Exception as e:
  print(e) 
  


try:
    for _ in range(3):
      driver, storage = runSteps(driver, goNextPage)
      Links.extend(storage["store"]["href"])
except Exception as e:
  print(e) 
finally:
  quitRemoteDriver(driver)


###
###
###
print(f"Links: {json.dumps(Links, ensure_ascii=False)}")
for url in Links:
  try:
    driver = initRemoteDriver(cm)
    if url.startswith("https://www.chinatimes.com/"):
      driver, storage = runSteps(driver,[{
          "target": "go",
          "execute": "none",
          "targetArgs": url,
          "executeArgs": ""
        },
        {
          "target": "findElementByXpath",
          "execute": "saveContent",
          "targetArgs": "//*/h1[contains(@class, 'article-title')]",
          "executeArgs": "article-title"
        },
        {
          "target": "findElementByXpath",
          "execute": "saveContent",
          "targetArgs": "//*/div[contains(@class, 'article-body')]/p",
          "executeArgs": "article-body"
        }]
      )
      tilte:str = storage["store"]["article-title"][0]
      body:str = "\n".join(storage["store"]["article-body"])
      result = {
          "tilte": tilte,
          "url": url,
          "content":body
        }
        
      # save_item(result)
      print(result)
    quitRemoteDriver(driver)
  except Exception as e:
    print(e) 
  
