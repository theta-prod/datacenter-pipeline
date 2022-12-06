#!/usr/bin/env python
import psutil
from crawlab import save_item

# gives a single float value
cpu = psutil.cpu_percent()
# gives an object with many fields
#ram = psutil.virtual_memory()
# you can convert that object to a dictionary 
ram = dict(psutil.virtual_memory()._asdict())
# you can have the percentage of used RAM
# ram = psutil.virtual_memory().percent
#79.2
# you can calculate percentage of available memory
#psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
#20.8

hdd = psutil.disk_usage('/')

print (f"Total: {hdd.total / (2**30)} GiB")
print (f"Used: {hdd.used / (2**30)} GiB" )
print (f"Free: {hdd.free / (2**30)} GiB")



print(f"cpu: {cpu}")
print(f"ram: {ram}")

save_item({
  "cpu": f"{cpu} %",
  "ram": ram,
  "dict": {
    "Total": f"{hdd.total / (2**30)} GiB",
    "Used": f"{hdd.used / (2**30)} GiB",
    "Free": f"{hdd.free / (2**30)} GiB",
    "Used Percent": f"{hdd.used/hdd.total} %"
  }
})

