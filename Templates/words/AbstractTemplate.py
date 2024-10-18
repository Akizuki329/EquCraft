from abc import ABC, abstractmethod

class AbstractTemplate(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def introduction(self):
        pass
    
    def set(self,information):
        try:
            self.__set_detail(information)
        except Exception as e:
            print(e)
        
    #失败应抛出异常
    def __set_detail(self,information):
        [_,self.prefix,self.suffix,self.prefix_otherwords,self.suffix_otherwords,self.prefix_need,self.suffix_need]=information
        self.prefix=str.split(self.prefix,' ')
        self.suffix=str.split(self.suffix,' ')
        if type(self.prefix_need)!=type(0):
            raise Exception
        if type(self.suffix_need)!=type(0):
            raise Exception

    @abstractmethod       
    def use_message_bool(self):
        pass
    
    # -1表示不符合要求，0表示词条不足，1表示符合要求
    def situation(self,words_useful_cnt,words_curr_cnt,words_need_cnt,words_max,allowed_other_words):
        # 出现杂词
        if allowed_other_words==False and words_useful_cnt<words_curr_cnt:
            return -1
        # 词缀数量达到上限，但是仍未达到要求
        if words_useful_cnt<words_need_cnt and words_curr_cnt>=words_max:
            return -1
        # 所需词缀数量不足
        if words_useful_cnt<words_need_cnt:
            return 0
        # 满足要求
        return 1
        
