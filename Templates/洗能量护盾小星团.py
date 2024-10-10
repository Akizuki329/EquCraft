#isCrafted,Currency = self.filter_func(item_info)
print('【能量护盾小星团】 Load Successfully')
word_prefix=['强大的','脉冲的']
word_suffix=['哲学家之']
def filter(item: str) -> bool:
    #炽焰 六翼天使 六翼天使 
    useful_prefix=0
    useful_suffix=0
    for word in word_prefix:
        if item.count(word)>0:
            useful_prefix+=1
    for word in word_suffix:
        if item.count(word)>0:
            useful_suffix+=1

    currency = ''
    if item.count('前缀')>0 and item.count('后缀')>0:
        currency = 'Alt'
    else:
        currency = 'Aug'


    return useful_prefix>0 and useful_suffix>0,currency