print('【能量护盾小星团】 Load Successfully')
def filter(item: str) -> bool:
    #炽焰 六翼天使 六翼天使 
    usefulWord=0
    if item.count('脉冲')>0:
        usefulWord+=1
    if item.count('强大')>0:
        usefulWord+=1
    return usefulWord>0,item.count('前缀')>0