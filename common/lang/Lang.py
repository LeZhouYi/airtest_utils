from pandas import read_csv,DataFrame

class LangType(object):
    ZH_HK = 'zh-hk'
    ZH_CN = 'zh-cn'

def loadLangData(path:str,lang:str):
    '''
    加载语言文件
    '''
    with open(path,encoding='UTF-8') as csvData:
        names = ['describe',LangType.ZH_HK,LangType.ZH_CN]
        return read_csv(csvData,names=names).loc[:,['describe',lang]]

def findValue(lang:DataFrame,describe:str):
    '''
    获得当前语言当前文本对应的控件内容
    '''
    data_frame = lang.loc[lang['describe']==describe]
    return data_frame.iat[0,1]

class Lang(dict):
    '''存储语言相关的数据结构'''

    def __init__(self,path:str,lang:str) -> None:
        self.langType = lang
        self.csvData = loadLangData(path,lang)

    def value(self, key:str) -> str:
        if self.csvData!=None:
            return findValue(self.csvData,key)
        return None