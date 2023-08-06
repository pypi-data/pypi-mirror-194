# coding=utf-8
import chardet
import logging
import codecs


def GetCharset(filePath: str):
    from chardet.universaldetector import UniversalDetector
    with open(filePath, "rb") as f:
        data = f.read()
        charset = chardet.detect(data)['encoding']
    if charset == 'ascii':
        return 'gbk'
    return charset


def GetFileContent(filePath: str):
    old_encoding = GetCharset(filePath)
    content = ''
    try:
        fd = open(filePath, "r", encoding=old_encoding)
        content = fd.read()
        fd.close()
    except Exception as e:
        raise (e)
        return '', ''
    return content, old_encoding


def Convert2Utf8(filename: str) -> bool:
    content, old_encoding = GetFileContent(filename)
    if old_encoding == None:
        logging.warn(f'detect encoding fail:{filename}')
        return False

    if old_encoding == 'utf-8':
        return True

    f = codecs.open(filename, 'w', encoding='utf-8')
    f.write(content)
    return True
