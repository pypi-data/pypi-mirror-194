# -*- coding: utf-8 -*-

import unicodedata
import regex as re

class UnicodeTokenizer:
    def __init__(self,  do_lower_case=True, never_split=[], highUnicodePoint=10000):
        self.do_lower_case = do_lower_case
        self.highUnicodePoint = highUnicodePoint
        self.never_split = set(x for x in never_split)

    
    def split_blank(self,line):
        tokens=[x.strip() for x in line.split() if x.strip()]
        return tokens

    def split_marks(self,line,marks):
        tokens = []
        for i, x in enumerate(line):
            if i == 0:
                tokens.append(x)
            elif marks[i] or marks[i-1]:
                tokens.append(x)
            else:
                tokens[-1] += x
        return tokens
        
    def normalize(self, line,  normal_type="NFD"):
        l = unicodedata.normalize(normal_type, line)
        return l
    
    def split_highUnicodePoint(self,line):
        marks = [ord(x) >= self.highUnicodePoint for x in line]
        return self.split_marks(line, marks)

    def split_category(self,line):
        if len(line) == 1:
            return [line]
        elif len(line) == 0:
            return []
        categorys = [unicodedata.category(x) for x in line]
        names = [unicodedata.name(x).split()[0] if categorys[i][0] in 'LN' else None for i, x in enumerate(line)]
        tokens = []
        for i, x in enumerate(line):
            if i == 0:
                tokens.append(x)
            elif categorys[i][0] == categorys[i-1][0] == 'L':
                if names[i]==names[i-1]:
                    tokens[-1] += x
                else:
                    tokens.append(x)
            elif categorys[i][0] == categorys[i-1][0] == 'N':
                if names[i] == names[i-1]:
                    tokens[-1] += x
                else:
                    tokens.append(x)
            else:
                if categorys[i]!='Mn':
                    tokens.append(x)
                if categorys[i-1]=='Mn':
                    tokens.append('')

        return [x.strip() for x in tokens if x.strip()]

    def split_word(self, x):
        tokens=[]
        if self.do_lower_case:
            x = self.normalize(x.lower())
        us = self.split_blank(x)
        for u in us:
            vs = self.split_highUnicodePoint(u)
            for v in vs:
                w = self.split_category(v)
                tokens += w
        return tokens

    def tokenize(self, line):
        words = self.split_blank(line)
        tokens = []
        for x in words:
            if x in self.never_split:
                tokens.append(x)
            else:
                tokens += self.split_word(x)
        return tokens
    
    def detokenize(self,tokens):
        l=''
        for i,x in enumerate(tokens):
            if i>0 and ord(x[-1])<self.highUnicodePoint and  ord(tokens[i-1][-1] )<self.highUnicodePoint:
                l+=' '
            l+=x
        return l


if __name__ == "__main__":
    from logzero import logger


    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏２０１９\U0010ffff"
    # line = "art_new_word=True"
    tokenizer=UnicodeTokenizer()
    logger.info((tokenizer.split_blank(line)))
    # line = "=True"

    tokenizer = UnicodeTokenizer()
    logger.info(tokenizer.tokenize(line))
    import timeit
    # re=timeit.timeit("''.join(chr(x) for x in range(int(1e6))) ")
    # logger.info(re)

    import time
    t0 = time.time()
    for i in range(10000):
        # chr(i)  # ValueError: chr() arg not in range(0x110000)
        tokenizer.tokenize(line)
    t1 = time.time()
    logger.info(t1-t0)
