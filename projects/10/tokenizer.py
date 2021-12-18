# -*- coding: utf-8 -*-
import sys

class Tokenizer():
    symbols = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    keywords = ['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false',\
                'null','this','let','do','if','else','while','return']
    def __init__(self,source_file):
        self.source_file = source_file
        raw_tokens = self._clean_comment()
        self.tokens = self._tokenize(raw_tokens)
        self.index = 0

    def hasMoreTokens(self):
        return self.index < len(self.tokens)

    def thisToken(self):
        return self.tokens[self.index]

    def peek(self,n):
        return self.tokens[self.index+n]

    def advance(self):
        self.index += 1

    def _clean_comment(self):
        comment_flag = False
        lines = []
        with open(self.source_file) as f:
            for line in f:
                if "/*" in line or "/**" in line:
                    lines.append(line.split("/*")[0])
                    if "*/" in line:
                        lines.append(line.split("*/")[1])
                    else:
                        comment_flag = True
                elif not comment_flag:
                    lines.append(line.split("//")[0])
                else:
                    if "*/" in line:
                        lines.append(line.split("*/")[1])
                        comment_flag = False
        raw_tokens = " ".join(lines)
        return raw_tokens

    def _tokenize(self,raw_tokens):
        tokens = []
        current_token = ""
        index = 0
        while index < len(raw_tokens):
            if raw_tokens[index] in [" ","\n","\t"]:
                if current_token:
                    tokens.append((current_token,self._token_type(current_token)))
                    current_token = ""
            elif raw_tokens[index] in self.symbols:
                if current_token:
                    tokens.append((current_token,self._token_type(current_token)))
                    current_token = ""
                tokens.append((raw_tokens[index],"symbol"))
            elif raw_tokens[index] == '"':
                if current_token:
                    raise Exception('unexpect " '.format(token))
                else:
                    index += 1
                    while not raw_tokens[index] == '"':
                        current_token += raw_tokens[index]
                        index += 1
                    tokens.append((current_token,"stringConstant"))
                    current_token = ""
            else:
                current_token += raw_tokens[index]
            index += 1
        return tokens

    def _token_type(self,token):
        if token in self.keywords:
            return "keyword"
        elif token in self.symbols:
            return "symbol"
        elif token.isdigit():
            return "integerConstant"
        elif not token[0].isdigit():
            return "identifier"
        else:
            raise Exception('unknown token : {}'.format(token))

def test_tokenizer(source_file,output_file):
    tokenizer = Tokenizer(source_file)
    with open(output_file,'w') as f:
        f.write("<tokens>"+"\n")
        while tokenizer.hasMoreTokens():
            token,token_type = tokenizer.thisToken()
            f.write("<{0}> {1} </{0}>".format(token_type,token)+"\n")
            tokenizer.advance()       
        f.write("</tokens>\n")


if __name__ == "__main__":
    #tokenizer = Tokenizer(sys.argv[1])
    test_tokenizer(sys.argv[1],sys.argv[2])

