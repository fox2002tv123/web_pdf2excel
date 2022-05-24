# %%
'''
Author: bob
Date: 2022-05-24 16:59:52
LastEditors: bob
LastEditTime: 2022-05-24 19:31:18
FilePath: \任务22-开发网络版对账单转换工具\对账单转换工具.py
Description: 使用python编写的网络版对账单转换工具

Copyright (c) 2022 by bob, All Rights Reserved. 
'''


# %%
# open读取txt文件

with open('data.txt', 'r',encoding='utf-8') as f:
    data = f.read()

data

# %%
# 预留-数据data提取的第二种方法
# data=input('请输入数据：')
# data


# %%
# 1.通过re模块提取数据-表头
import re
p=r'(\d{5,6}) (\S{17}) (\S{6})'
res_head=re.findall(p,data)
res_head


# %%
# 2.通过re模块提取数据-表体
# import re
p=r'\*( 赔付)(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*)'
res_body=re.findall(p,data)
res_body

# %%
# 3.通过re模块提取数据-对账单序列号
# import re
p=r'Credit Note Number (\d{7})'
res_number=re.findall(p,data)
res_number=res_number[0]
res_number

# %%
# 4.通过re模块提取数据-对账单日期
# import re
p=r'Date: (\S{10})'
res_date=re.findall(p,data)
res_date=res_date[0]
res_date

# %%
# 5.判断国产还是进口
first_char=res_head[0][1][0]
if first_char=='L':
    s='BBA'
else:
    s='GIS'
s

# %%
# 通过pandas转换成dataframe
import pandas as pd
import numpy as np
df1=pd.DataFrame(res_head,columns=['保修单号','车架号','DWP保修单号'])
df1
df2=pd.DataFrame(res_body,columns=list('A1234567'))
df2
# 合并两个dataframe concat axis=1
df=pd.concat([df1,df2],axis=1)
df

# 去掉',',并转换成float
df.loc[:,'1':'7']=df.loc[:,'1':'7'].applymap(lambda x:str(x).replace(',',''))

# 转换成float
for i in range(1,8):
    df.loc[:,'{}'.format(i)]=pd.to_numeric(df.loc[:,'{}'.format(i)],errors='coerce')

# 添加汇总列
df['总计']=df.loc[:,'1':'7'].max(axis=1)

# 添加各种'对账单序列号','对账单日期'列
df['对账单序列号']=res_number
df['对账单日期']=res_date.replace('.','/')

df.head()
# df.info()

# %%
# 写入excel
# 改变列的顺序
alist=['DWP保修单号','保修单号','车架号','对账单序列号','对账单日期','1','2','3','4','5','总计']
df[alist].to_excel(f'{res_number}DATE{res_date}{s}.xlsx',index=False)


