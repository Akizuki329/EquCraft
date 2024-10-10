print('【能量护盾小星团】 Load Successfully')
def filter(item: str) -> bool:
    #炽焰 六翼天使 六翼天使 
    usefulWord=0
    if item.count('闪闪发光')>0:
        usefulWord+=1
    if item.count('雷电的')>0:
        usefulWord+=1
    if item.count('混沌的')>0:
        usefulWord+=1
    if item.count('冲锋的')>0:
        usefulWord+=1
    return usefulWord>0,item.count('前缀')>0