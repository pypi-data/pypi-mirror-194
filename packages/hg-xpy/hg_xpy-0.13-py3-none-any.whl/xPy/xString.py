# coding=utf-8
import os
from typing import Callable
import logging
import codecs
import sys

try:
    sys.path.append('./')
    import x
except Exception as e:
    import func
    import func.x as x
finally:
    pass

try:
    import regex  # 导入模块
except Exception as e:
    print('installing regex')
    os.system('pip3 install regex')
    import regex  # 导入模块
finally:
    pass


class xString:
    @staticmethod
    def Replace(s: str, search: str, new: str) -> regex.Regex:
        return regex.sub(search, new, s)

    @staticmethod
    def Replace2(s: str, search: str, new: str, flags=0) -> (str, bool):
        # 替换字符串直至没有替换为止
        ret = False
        i = 1
        for i in range(10):
            s, n = regex.subn(search, new, s, flags=flags)
            if n <= 0:
                break
            ret = True
        if i >= 10:
            logging.error("Replace2 too many times %s->%s" % (search, new))
        return s, ret

    @staticmethod
    def ReplaceFile(filePath: str, rules: dict, flags=0):
        # 文件内容替换，支持正则表达式
        # rules, key: 正则表达式，value: 替换后的字符串
        old_encoding = x.GetCharset(filePath)
        content = ''
        try:
            fd = open(filePath, "r", encoding=old_encoding)
            content = fd.read()
            fd.close()
        except Exception as e:
            logging.error("file:%s exception:%s" % (filePath, e))
            return

        Change = False
        for search, new in rules.items():
            content, ret = xString.Replace2(content, search, new, flags)
            if ret:
                Change = True
        if not Change:
            return

        try:
            # if old_encoding != 'UTF-8-SIG':
            #     logging.info('%s conver %s to UTF-8-SIG' %
            #                  (filePath, old_encoding))
            #     b = content.encode(old_encoding)
            #     content = b.decode('UTF-8-SIG', 'ignore')
            # codecs.open(filePath, 'w', encoding='UTF-8-SIG').write(content)
            with open(filePath, "w", encoding=old_encoding) as fd:
                fd.write(content)
            logging.info('%s replace done' % filePath)
        except Exception as e:
            logging.error("file:%s exception:%s" % (filePath, e))
            return

    @staticmethod
    def IsStrInFile(filePath: str, rules: list[str], flags=0)->bool:
        # 文件内容查找，支持正则表达式
        old_encoding = x.GetCharset(filePath)
        content = ''
        try:
            fd = open(filePath, "r", encoding=old_encoding)
            content = fd.read()
            fd.close()
        except Exception as e:
            logging.error("file:%s exception:%s" % (filePath, e))
            return False

        Find = False
        for r in rules:
            ret = regex.search(r, content)
            if ret:
                return True
        return False

    @staticmethod
    def ReplaceDir(dirPath: str, search: str, new: str, include='', exclude=''):
        # 将目录内符合条件的文件内容替换，支持正则表达式
        xString.IterDir(dirPath, lambda filePath: xString.ReplaceFile(
            filePath, {search: new}), include, exclude)

    @staticmethod
    def ReplaceDir2(dirPath: str, rule: dict, include='', exclude='', flags=0):
        # 将目录内符合条件的文件内容替换，支持正则表达式和多个规则
        xString.IterDir(dirPath, lambda filePath: xString.ReplaceFile(
            filePath, rule, flags), include, exclude)

    # exclude = "*.log;*.txt"
    # include = "*.log;*.txt"

    @staticmethod
    def GetFileTree(dirPath: str, include='', exclude='') -> list:
        result = []
        xString.IterDir(dirPath, lambda x: result.append(
            x), include, exclude)
        return result

    @staticmethod
    def IterDir(dirPath: str, func: Callable, include="", exclude=""):
        s = ''
        isExclude = False

        if exclude:
            exclude = xString.parseFilterStrToList(exclude)

        if include:
            include = xString.parseFilterStrToList(include)

        for curDir, _, files in os.walk(dirPath):
            for file in files:
                isExclude = False
                s = os.path.join(curDir, file)

                if include:
                    isExclude = True
                    for rule in include:
                        if GNURule.IsFilePathMatch(rule, s):
                            isExclude = False
                            break

                if exclude:
                    isExclude = False
                    for rule in exclude:
                        if GNURule.IsFilePathMatch(rule, s):
                            isExclude = True
                            break

                if not isExclude:
                    func(s)

    # a;b;c => [a,b,c]

    @staticmethod
    def parseFilterStrToList(s: str):
        if s == "":
            return None

        return s.split(";")


class GNURule:
    """
    example:
    list is
    [
    file1.ext
    file1.ext.bak
    file2.ext
    file3
    ]

    *.ext => [file1.ext file2.ext]
    *.ext* => [file1.ext file1.ext.bak file2.ext]
    * => [file1.ext file1.ext.bak file2.ext file3]
    *ext => [file1.ext file1.ext file2.ext]
    *ex => []
    file* => [file1.ext file1.ext.bak file2.ext file3]
    file1* => [file1.ext file1.ext.bak]


    * -> '[\s\S]*'
    . -> \.

    """
    @staticmethod
    def IsFilePathMatch(rule: str, s: str):
        return regex.match(GNURule.TransRuleToRegexExp(rule), os.path.basename(s)) != None

    # 将GNU规则转换为正则规则
    @staticmethod
    def TransRuleToRegexExp(rule: str):
        reStr = ''
        if not rule:
            return reStr

        reStr = rule.replace(".", r"\.")
        reStr = reStr.replace("*", r"[\s\S]*")
        # 不需要开头
        if rule[0] != "*":
            reStr = "^" + reStr

        if rule[len(rule)-1] != "*":
            reStr = reStr + "$"

        return reStr

    @staticmethod
    def TransRuleToRegex(rule: str):
        return regex.compile(GNURule.TransRuleToRegexExp(rule))


def DecodeByte(byte):
    try:
        return byte.decode('utf-8')
    except:
        return byte.decode('gbk')


if __name__ == "__main__":
    # xString.ReplaceDir(
    #     r"D:\Library\xGM\src\xGM\data_model_bak", "import2", "import")
    # for i in xString.GenerateFilesTree(r"D:\Library\xGM\src\xGM", ["go$"]):
    #     print(i)
    # for curDir, dirs, files in os.walk(r"D:\Library\script"):
    # print(curDir)
    # print(dirs)
    # print(files)

    # xString.ReplaceFile(r'd:\xsw\code_gs\md2\md2\xPrj.ps1',
    #                     '_TEMPLATE_FRAME_PATH', r'g:\code_new\md2\md2')
    xString.IterDir("./", print)
    xString.IterDir("./", print, "", "*.pyc")

    template_list = [
        "/usr/include/my_header.h",
        "/usr/include/new_ver/new_header.h",
        "/usr/include/my_header.cpp",
    ]

    for p in template_list:
        b = GNURule.IsFilePathMatch("*", p)
        print(b)

    # xString.IterDir(r"D:\Library\script\py\func", print, "*", "*py")
    xString.ReplaceDir(
        r"D:\Library\xGM\src\xGM\data_model_bak\\", "import2", "import", "*.go")
