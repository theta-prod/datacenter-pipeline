from typing import List
from driverTool import ActionConfig, ActionStorge, RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, runAction


cm: RemoteDriverConfig = {
    "hostUrl": "http://34.127.47.231:4444",
    "chromeVersion": "107.0",
    "platformType": "Linux"
}
ts: List[ActionConfig] = [
    {
        "target": "go",
        "execute": "none",
        "args": "https://news.google.com/topstories?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    },
    {
        "target": "findLinkByContainText",
        "execute": "clickElement",
        "args": "頭條新聞|焦點新聞"
    },
    {
        "target": "waitSec",
        "execute": "none",
        "args": "25"
    },
    {
        "target": "findElementByXpath",
        "execute": "saveContent",
        "args": "//*[self::h3 or self::h4]"
    },

]


###
###
###
driver = initRemoteDriver(cm)
storage: ActionStorge = {
    "store": {}
}
for c in ts:
    print(c["target"], c["args"])
    storage = runAction(driver, storage, c)
print(storage)





quitRemoteDriver(driver)