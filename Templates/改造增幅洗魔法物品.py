#isCrafted,Currency = self.filter_func(item_info)
from Templates.words.AbstractTemplate import AbstractTemplate

class Template(AbstractTemplate):
    def __init__(self):
        super(Template,self).__init__()
        self.introduction()
        #自定义前后缀上限
        self.prefix_max=1
        self.suffix_max=1

    def introduction(self):
        #输出模板相关信息
        print('【改造增幅洗词缀】 Load Successfully')

    #是否使用gui所传入信息，False为不需要
    #和set配套使用
    def use_message_bool(self):
        return True

    def filter(self,item: str) -> bool:
        #记录有效词缀数量
        useful_prefix=0
        useful_suffix=0
        for word in self.prefix:
            if item.count(word)>0:
                useful_prefix+=1
        for word in self.suffix:
            if item.count(word)>0:
                useful_suffix+=1

        #记录现有词缀数量
        prefix_curr_cnt=item.count('前缀属性')
        suffix_curr_cnt=item.count('后缀属性')

        prefix_situation=self.situation(useful_prefix,prefix_curr_cnt,self.prefix_need,self.prefix_max,self.prefix_otherwords)
        suffix_situation=self.situation(useful_suffix,suffix_curr_cnt,self.suffix_need,self.suffix_max,self.suffix_otherwords)

        currency = ''
        if prefix_situation==-1 or suffix_situation==-1:
            currency = 'Alt'
        elif prefix_situation==0 or suffix_situation==0:
            currency = 'Aug'
        else:
            return True,currency


        return False,currency