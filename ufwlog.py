import re
import pandas as pd
from datetime import datetime
Year = datetime.strftime(datetime.today(),'%Y')
file1 = 'ufw-1.log'
file2 = 'ufw-2.log'
with open(file1,'r') as file:
    ufw1 = file.readlines()
with open(file2,'r') as file:
    ufw2 = file.readlines()
ufw = ufw1 + ufw2
time = []
Ip = []
for con in ufw:
    date = datetime.strptime(Year+con[0:14],'%Y%b %d %H:%M:%S',)
    time.append(date)
    Ip.append(re.findall(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}',con)[0])
result = {"time":time,"Ip":Ip}
# print(result)
df = pd.DataFrame(result)
print(df)
df.to_csv("ufw_log.csv",encoding="utf-8")