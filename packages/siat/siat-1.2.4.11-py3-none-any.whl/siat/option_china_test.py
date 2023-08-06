# -*- coding: utf-8 -*-

# 绝对引用指定目录中的模块
import sys
sys.path.insert(0,r'S:\siat\siat')
from option_china import *
#==============================================================================
dct=option_comm_dict_china('黄金期权')

df1=option_comm_china()

df2=option_comm_china('黄金')

ualist=['豆粕','玉米','铁矿石','棉花','白糖','PTA','甲醇','橡胶','沪铜','黄金','菜籽粕','液化石油气','动力煤']
for ua in ualist:
    df2b=option_comm_china(ua)

df3=option_comm_china('黄金','au2204')

df4=option_comm_trend_china('au2112C328')
df4b=option_comm_trend_china('au2112C328','2021-8-1','2021-9-30')
df5=option_comm_trend_china('au2112C328',power=4)

df6=option_comm_trend_china(['au2112C328','au2112P328'])
df7=option_comm_trend_china(['au2112C328','au2112P328'],twinx=False)
df8=option_comm_trend_china(['au2112C328','au2112P328'],'2021-7-1','2021-9-30')
df8a=option_comm_trend_china(['au2112C328','au2112P328'],'2021-7-1','2021-9-30')

dictau=option_contract_decode_china('Au2112c235')

#==============================================================================
df2b=option_comm_china('动力煤')
df3b=option_comm_china('动力煤','zc2205')
df4b=option_comm_trend_china('zc2205C1000','2021-1-1','2021-9-30')
df6b=option_comm_trend_china(['zc2205C1000','zc2205P1000'],'2021-1-1','2021-9-30')
x