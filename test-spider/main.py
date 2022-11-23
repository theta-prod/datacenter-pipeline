from tool import ActionConfig, ActionStorge, RemoteDriverConfig, initRemoteDriver, quitRemoteDriver, runAction


cm: RemoteDriverConfig = {
    "hostUrl": "http://34.127.47.231:4444",
    "chromeVersion": "107.0",
    "platformType": "Linux"
}
t1: ActionConfig = {
    "target": "go",
    "execute": "none",
    "args": ["https://news.google.com/topstories?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"]
}
t2: ActionConfig = {
    "target": "waitSec",
    "execute": "none",
    "args": ["100"]
}


###
###
###
driver = initRemoteDriver(cm)
storage: ActionStorge = {
    "store": {}
}
for c in [t1, t2]:
    print(c["target"])
    storage = runAction(driver, storage, c)





# quitRemoteDriver(driver)