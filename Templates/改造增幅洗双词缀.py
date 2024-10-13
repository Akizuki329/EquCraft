#isCrafted,Currency = self.filter_func(item_info)
import Templates.words.words as wd

print('【改造增幅洗双词缀】 Load Successfully')

#是否使用gui所传入信息，False为不需要
#和set配套使用
#后续可使用抽象类，用重写的方式构造模板
#失败应抛出异常
def use_message_bool():
    return False
def set():
    if len(wd.word_prefix)<1 and len(wd.word_suffix)<1:   
        raise Exception('不合法的词缀数量')



def filter(item: str) -> bool:
    #炽焰 六翼天使 六翼天使 
    useful_prefix=0
    useful_suffix=0
    for word in wd.word_prefix:
        if item.count(word)>0:
            useful_prefix+=1
    for word in wd.word_suffix:
        if item.count(word)>0:
            useful_suffix+=1

    currency = ''
    if useful_prefix>0 and useful_suffix>0:
        return True,currency
    elif (item.count('前缀属性') + item.count('后缀属性'))==useful_prefix+useful_suffix:
        currency = 'Aug'
    else:
        currency = 'Alt'


    return useful_prefix>0 and useful_suffix>0,currency