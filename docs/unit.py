


#
# open读取txt文件

# with open('data.txt', 'r',encoding='utf-8') as f:
#     data = f.read()

# data

#
# 预留-数据data提取的第二种方法
# data=input('请输入数据：')
# data
# txt_message = Element("message") # 创建一个文本框
# container = Element("output") # 容器

def run(data):
    # return 1

    # data=txt_message.value # 获取文本框的值
    #
    # 1.通过re模块提取数据-表头
    import re
    p = r'(\d{5,6}) (\S{17}) (\S{6})'
    res_head = re.findall(p, data)
    res_head

    #
    # 2.通过re模块提取数据-表体
    # import re
    p = r'\*( 赔付)(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*)'
    res_body = re.findall(p, data)
    res_body

    #
    # 3.通过re模块提取数据-对账单序列号
    # import re
    p = r'Credit Note Number (\d{7})'
    res_number = re.findall(p, data)
    res_number = res_number[0]
    res_number

    #
    # 4.通过re模块提取数据-对账单日期
    # import re
    p = r'created on (\S{10})'
    res_date = re.findall(p, data)
    res_date = res_date[0]
    res_date

    #
    # 5.判断国产还是进口
    first_char = res_head[0][1][0]
    if first_char == 'L':
        s = 'BBA'
    else:
        s = 'GIS'
    s

    #
    # 通过pandas转换成dataframe
    import pandas as pd
    import numpy as np
    df1 = pd.DataFrame(res_head, columns=['保修单号', '车架号', 'DWP保修单号'])
    df1
    df2 = pd.DataFrame(res_body, columns=list('A1234567'))
    df2
    # 合并两个dataframe concat axis=1
    df = pd.concat([df1, df2], axis=1)
    df

    # 去掉',',并转换成float
    df.loc[:, '1':'7'] = df.loc[:, '1':'7'].applymap(
        lambda x: str(x).replace(',', ''))

    # 转换成float
    for i in range(1, 8):
        df.loc[:, '{}'.format(i)] = pd.to_numeric(
            df.loc[:, '{}'.format(i)], errors='coerce')

    # 添加汇总列
    df['总计'] = df.loc[:, '1':'7'].max(axis=1)

    # 添加各种'对账单序列号','对账单日期'列
    df['对账单序列号'] = res_number
    df['对账单日期'] = res_date.replace('.', '/')

    # return df.head()

    # df.info()

    #
    # 写入excel
    # 改变列的顺序
    alist=['DWP保修单号','保修单号','车架号','对账单序列号','对账单日期','1','2','3','4','5','总计']
    # todo 写入excel
    
    ###
    # 0.re提取每个特征-生成段落
    import re
    detail_list=re.findall(r'[^_]+',data)[:-1]
    detail_list.__len__()
    detail_list[0]
    
    # 1是否有零件特征
    detail_part=[]
    for i in detail_list:
        if re.findall(r'\d{10} \S{11} ',i): # 判断是否有零件特征-添加了空格边界
            detail_part.append(True)
        else:
            detail_part.append(False)
    detail_part
    detail_part.__len__()
    
    # 2是否有工时特征
    detail_FRU=[]
    for i in detail_list:
        if re.findall(r'\d{10} \S{7} ',i): # 判断是否有工时特征--添加了空格边界
            detail_FRU.append(True)
        else:
            detail_FRU.append(False)
    detail_FRU
    detail_FRU.__len__()
    
    # 3是否有辅料特征
    detail_sublit=[]
    for i in detail_list:
        if re.findall(r'\d{10} \S{1} ',i): # 判断是否有辅料特征--添加了空格边界
            detail_sublit.append(True)
        else:
            detail_sublit.append(False)
    # detail_sublit
    detail_sublit.__len__()
    
    # 4是否有 处理费 特征
    detail_handcost=[]
    for i in detail_list: # 如果召回00开头的,也会有处理费特征
        if re.findall(r'\d{9}[^6] \S{11} ',i) or re.findall(r'00\d{6}86 \S{11} ',i): # DC最后一位不能是6--添加了空格边界
            detail_handcost.append(True)
        else:
            detail_handcost.append(False)
    # detail_handcost
    detail_handcost.__len__()
    
    # 5是否有 税费 特征-都有
    detail_tax=[]
    for i in detail_list:
            detail_tax.append(True)
    detail_tax
    detail_tax.__len__()
    
        # 6是否有 合计特征-都有
    detail_total=[]
    for i in detail_list:
            detail_total.append(True)
    detail_total
    detail_total.__len__()
    
    # 7形成一个dataframe
    df_detail=pd.DataFrame({'detail_part':detail_part,'detail_FRU':detail_FRU,'detail_sublit':detail_sublit,'detail_handcost':detail_handcost,'detail_tax':detail_tax,'detail_total':detail_total})
    df_detail.head()
    
    # 8通过true false 填入数据
    import numpy as np
    df_detail_res=df_detail.copy()
    df_value=df.loc[:,'1':'6']
    df_value.head()
    for i in range(df_value.shape[0]):
        k=0
        for j in range(df_value.shape[1]):
            if df_detail.iloc[i,j]:
                df_detail_res.iloc[i,j]=df_value.iloc[i,k]
                k+=1
            else:
                df_detail_res.iloc[i,j]=np.nan    

    df_detail_res.head()
    
    # 9 df和df_detail_res合并 axis=1
    df_res=pd.concat([df,df_detail_res],axis=1)
    df_res.head()
    
    ###
    df1=df_res.copy()
    new_columns=['DWP','CLAIM','VIN','NO','DATE','1','2','3','4','5','TOTAL']
    df1.rename(columns=dict(zip(alist,new_columns)),inplace=True)
    df1[new_columns].head()
    collect_list=['DWP','CLAIM','VIN','NO','DATE','detail_part','detail_FRU','detail_sublit','detail_handcost','detail_tax','TOTAL']
    res=df1[collect_list].to_csv(index=False)
    return res_number,res_date,s,res # 返回对账单序列号和对账单日期
    # return df.head()
