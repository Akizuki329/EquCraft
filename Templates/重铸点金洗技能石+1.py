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
        print('【重铸点金洗技能石】 Load Successfully\n')

    #是否使用gui所传入信息，False为不需要
    #和set配套使用
    def use_message_bool(self):
        return False
    
    # 对过滤器进行初始化，每次重新设置时运行，此处无需异常回收
    def filter_init(self):
        # 判断所需的词缀数量是否合理
        assert(self.prefix_need<3)
        assert(self.suffix_need<3)
        self.prefix_max=3
        self.suffix_max=3
        # 判断所需词条数量小于实际提供的可用词条集合


    def filter(self,item: str) -> bool:

        # 判断物品类别
        if item.count("稀 有 度: 稀有")>0:
            pass
        elif item.count("稀 有 度: 普通")>0:
            return False,'Alc'
        else:
            return True,'Error'

        if '交变者的' in item:
            return True,''
        else:
            return False,'Sco'