# [Tutorial] Build CRAWLAB as Date Pipeline Center

- **Metadata** : `type: Tutorial` `scope: CRAWLAB` 
- **Techs Need** : `docker`, `docker-compose` 
- **Status** : `done`

## ✨ You should already know

> Crawlab 是強大的 網絡爬蟲管理平台（WCMP），它能夠運行多種編程語言（包括Python、Go、Node.js、Java、C#）或爬蟲框架（包括Scrapy、Colly、Selenium、Puppeteer）開發的網路爬蟲。它能夠用來運行、管理和監控網絡爬蟲，特別是對可溯性、可擴展性以及穩定性要求較高的生產環境。
> 更多的說明請參考[這裡](https://docs.crawlab.cn/zh/guide/)
👩‍💻 👨‍💻

## ✨ About the wiki

- `Situation:`  我們需要固定的執行資料蒐集任務來推動資料成長
- `Target:`  製作定時任務平台來穩定收集資料
- `Index:`

| Sub title | decription | memo |
| ------ | ------ | ------ |
| System Structure | descript how to build system | CRAWLAB + Selenium Grid |


## ✨  Sections

---
### **System Structure**
> 該系統主要統合兩個資源，分別是`CRAWLAB`和`Selenium Grid`。
> 我們會再`CRAWLAB`上面建立爬蟲/健康檢定等任務，作為維運資料收集的主要構成。
<br/>



####  📝 爬蟲任務
> 爬蟲任務我們使用Python3搭配`Selenium Grid`來驅動`chrome`來蒐集網頁資料。

- Hello World
```
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability("browserVersion", "107.0")
chrome_options.set_capability("platformName", "LINUX")
browser = webdriver.Remote(command_executor='http://127.0.0.1:4444',
                           options=chrome_options)

# navigate to news list page
browser.get('https://36kr.com/information/web_news/')
browser.quit()
```
> [more detail](https://github.com/theta-prod/datacenter-pipeline/tree/master/test-spider)