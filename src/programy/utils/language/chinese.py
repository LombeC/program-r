# This code was pulled from another AIML processor in Github
# https://github.com/Decalogue/aiml3/blob/master/aiml/LangSupport.py
# Thanks to Benny Shang for the info and help supporting chinese

class ChineseLanguage (object):

    @staticmethod
    def is_language(c):
        # http://www.iteye.com/topic/558050

        if isinstance(c, str):
            if len(c) == 0 or len(c) > 1:
                return False

        r = [
            # 标准CJK文字
            (0x3400, 0x4DB5), (0x4E00, 0x9FA5), (0x9FA6, 0x9FBB), (0xF900, 0xFA2D),
            (0xFA30, 0xFA6A), (0xFA70, 0xFAD9), (0x20000, 0x2A6D6), (0x2F800, 0x2FA1D),
            # 全角ASCII、全角中英文标点、半宽片假名、半宽平假名、半宽韩文字母
            (0xFF00, 0xFFEF),
            # CJK部首补充
            (0x2E80, 0x2EFF),
            # CJK标点符号
            (0x3000, 0x303F),
            # CJK笔划
            (0x31C0, 0x31EF)]

        return any(s <= ord(c) <= e for s, e in r)
    
    @staticmethod
    def split_language(s):
        result = []
        for c in s:
            if ChineseLanguage.is_language(c):
                result.extend([" ", c, " "])
            else:
                result.append(c)
        ret = ''.join(result)
        return ret.split()
    
    @staticmethod
    def split_unicode(s):
        segs = s.split()
        result = []
        for seg in segs:
            if any(map(ChineseLanguage.is_language, seg)):
                result.extend(ChineseLanguage.split_language(seg))
            else:
                result.append(seg)
        return result
    
    @staticmethod
    def split_with_spaces(s):
        segs = ChineseLanguage.split_language(s)
        result = []
        for seg in segs:
            # English marks
            if seg[0] not in ".,?!":
                try:
                    str(seg[0]) and result.append(" ")
                except:
                    pass
            result.append(seg)
            try:
                str(seg[-1]) and result.append(" ")
            except:
                pass
        return ''.join(result).strip()