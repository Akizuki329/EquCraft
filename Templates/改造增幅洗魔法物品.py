#isCrafted,Currency = self.filter_func(item_info)
from Templates.words.AbstractTemplate import AbstractTemplate

class Template(AbstractTemplate):
    def __init__(self):
        super(Template,self).__init__()
        self.introduction()
        self.filterIsInit=False
        #自定义前后缀上限
        # self.prefix_max=1
        # self.suffix_max=1

    def introduction(self):
        #输出模板相关信息
        print('【改造->增幅->崇高洗词缀】 Load Successfully\n\
              改模板仅支持魔法物品状态下词缀容量1p1s，且稀有物品状态下3p3s，其他词缀容量也许会出错')

    #是否使用gui所传入信息，False为不需要
    #和set配套使用
    def use_message_bool(self):
        return True
    
    # 对过滤器进行初始化，每次重新设置时运行，此处无需异常回收
    def filter_init(self):
        # 判断所需的词缀数量是否合理
        assert(self.prefix_need<3)
        assert(self.suffix_need<3)
        self.prefix_max=3
        self.suffix_max=3
        # 判断所需词条数量小于实际提供的可用词条集合


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

        # 判断物品类别
        item_type=0
        if item.count("稀 有 度: 魔法")>0:
            item_type=1
            prefix_curr_max=1
            suffix_curr_max=1
        elif item.count("稀 有 度: 稀有")>0:
            item_type=2
            prefix_curr_max=3
            suffix_curr_max=3
        elif item.count("稀 有 度: 普通")>0:
            return False,'Trans'
        else:
            return True,'Error'

        #分别判断前缀后缀是否符合要求
        prefix_situation=self.situation(useful_prefix,prefix_curr_cnt,self.prefix_need,prefix_curr_max,self.prefix_max,self.prefix_otherwords)
        suffix_situation=self.situation(useful_suffix,suffix_curr_cnt,self.suffix_need,suffix_curr_max,self.suffix_max,self.suffix_otherwords)

        currency = ''
        if item_type==1:
            # print(prefix_situation)
            # print(suffix_situation)
            if prefix_situation<0 or suffix_situation<0:
                currency = 'Alt'
            elif prefix_situation==0 or suffix_situation==0:
                currency = 'Aug'
            elif prefix_situation==2 or suffix_situation==2:
                currency = 'Reg'
            else:
                return True,currency
        elif item_type==2:
            if prefix_situation<0 or suffix_situation<0:
                currency = 'Sco'
            elif prefix_situation==0 or suffix_situation==0:
                currency = 'Exal'
            elif prefix_situation==1 and suffix_situation==1:
                return True,currency


        return False,currency