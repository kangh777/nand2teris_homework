# -*- coding: utf-8 -*- import sys
import sys
from tokenizer import Tokenizer

class CompilationEngine():

    def __init__(self,input_file,output_file):
        self.tokenizer = Tokenizer(input_file)
        self.fout = open(output_file,"w")

    def compileClass(self,black=""):
        self.eat("keyword","class")
        self.fout.write(black+"<class>"+"\n")
        self.fout.write(black+"  <keyword> class </keyword>"+"\n")
        class_name = self.eat("identifier")
        self.fout.write(black+"  <identifier> {} </identifier>\n".format(class_name))
        self.eat("symbol","{")
        self.fout.write(black+"  <symbol> { </symbol>\n")
        while self.peek()[0] in ["static","field"]:
            self.compileClassVarDec("  ")
        while self.peek()[0] in ["constructor","function","method"]:
            self.compileSubroutineDec("  ")

        self.fout.write(black+"  <symbol> } </symbol>\n")
        self.fout.write(black+"</class>\n")
        
    def compileClassVarDec(self,black=""):
        self.fout.write(black+"<classVarDec>\n")
        var_pos = self.eat("keyword")
        self.fout.write(black+"  <keyword> {} </keyword>".format(var_pos)+"\n")
        if self.peek()[1] == "keyword":
            var_type = self.eat("keyword")
            self.fout.write(black+"  <keyword> {} </keyword>".format(var_type)+"\n")
        elif self.peek()[1] == "identifier":
            var_type = self.eat("identifier")
            self.fout.write(black+"  <identifier> {} </identifier>".format(var_type)+"\n")
        var_name = self.eat("identifier")
        self.fout.write(black+"  <identifier> {} </identifier>".format(var_name)+"\n")
        while self.peek()[0] == ",":
            self.eat("symbol",",")
            self.fout.write(black+"  <symbol> , </symbol>"+"\n")
            var_name = self.eat("identifier")
            self.fout.write(black+"  <identifier> {} </identifier>".format(var_name)+"\n")
        self.eat("symbol",";")
        self.fout.write(black+"  <symbol> ; </symbol>".format(var_name)+"\n")
        self.fout.write(black+"</classVarDec>\n")
    def compileSubroutineDec(self,black=""):
        self.fout.write(black+"<SubroutineDec>\n")
        func_type = self.eat("keyword")
        if self.peek()[1] == "keyword":
            return_type = self.eat("keyword")
        elif self.peek()[1] == "identifier":
            return_type = self.eat("identifier")
        else:
            raise Exception('unexpect return type')
        func_name = self.eat("identifier")
        self.fout.write(black+"  <keyword> {} </keyword>".format(func_type)+"\n")
        self.fout.write(black+"  <keyword> {} </keyword>".format(return_type)+"\n")
        self.fout.write(black+"  <keyword> {} </keyword>".format(func_name)+"\n")
        self.eat("symbol","(")
        self.fout.write(black+"  <symbol> ( </symbol>".format(func_name)+"\n")
        self.compileParameterList(black+"  ")
        self.eat("symbol",")")
        self.fout.write(black+"  <symbol> ) </symbol>".format(func_name)+"\n")
        self.compileSubroutineBody(black+"  ")
        self.fout.write(black+"</SubroutineDec>\n")
    def compileParameterList(self,black=""):
        self.fout.write(black+"<ParameterList>\n")
        while self.peek()[0] in ["int","char","boolean"] or self.peek()[1] == "identifier":
            if self.peek()[0] in ["int","char","boolean"]:
                var_type = self.eat("keyword")
                self.fout.write(black+"  <keyword> {} </keyword>".format(var_type)+"\n")
            else:
                var_type = self.eat("identifier")
                self.fout.write(black+"  <identifier> {} </identifier>".format(var_type)+"\n")
            var_name = self.eat("identifier")
            self.fout.write(black+"  <identifier> {} </identifier>".format(var_name)+"\n")
            if self.peek()[0] == ",":
                self.eat("symbol")
                self.fout.write(black+"  <symbol> , </symbol>"+"\n")
        self.fout.write(black+"</ParameterList>\n")

    def compileSubroutineBody(self,black=""):
        self.fout.write(black+"<SubroutineBody>\n")
        self.eat("symbol","{")
        self.fout.write(black+"  <symbol> { </symbol>"+"\n")
        while self.peek()[0]  == "var":
            self.compileVarDec(black+"  ")
        self.compileStatements(black+"  ")
        self.eat("symbol","}")
        self.fout.write(black+"  <symbol> } </symbol>"+"\n")
        self.fout.write(black+"</SubroutineBody>\n")
    def compileVarDec(self,black=""):
        self.fout.write(black+"<VarDec>\n")
        self.eat("keyword","var")
        self.fout.write(black+"  <keyword> var </keyword>"+"\n")
        if self.peek()[0] in ["int","char","boolean"]:
            var_type = self.eat("keyword")
            self.fout.write(black+"  <keyword> {} </keyword>".format(var_type)+"\n")
        elif self.peek()[1] == "identifier":
            var_type = self.eat("identifier")
            self.fout.write(black+"  <identifier> {} </identifier>".format(var_type)+"\n")
        else:
            raise Exception('unexpect in var dec')
        var_name = self.eat("identifier")
        self.fout.write(black+"  <identifier> {} </identifier>".format(var_name)+"\n")
        while self.peek()[0] == ",": 
            self.eat("symbol",",")
            self.fout.write(black+"  <symbol> , </symbol>"+"\n")
            var_name = self.eat("identifier")
            self.fout.write(black+"  <identifier> {} </identifier>".format(var_name)+"\n")
        self.eat("symbol",";")
        self.fout.write(black+"  <symbol> ; </symbol>"+"\n")
        self.fout.write(black+"</VarDec>\n")
        
    def compileStatements(self,black=""):
        self.fout.write(black+"<Statements>\n")
        while self.peek()[0] in ["let","if","while","do","return"]:
            if self.peek()[0] == "let":
                self.compileLet(black+"  ")
            if self.peek()[0] == "if":
                self.compileIf(black+"  ")
            if self.peek()[0] == "while":
                self.compileWhile(black+"  ")
            if self.peek()[0] == "do":
                self.compileDo(black+"  ")
            if self.peek()[0] == "return":
                self.compileReturn(black+"  ")
        self.fout.write(black+"</Statements>\n")
        
    def compileLet(self,black=""):
        self.fout.write(black+"<Let>\n")
        self.eat("keyword","let")
        self.fout.write(black+"  <keyword> let </keyword>"+"\n")
        var_name = self.eat("identifier")
        self.fout.write(black+"  <identifier> {} </identifier>".format(var_name)+"\n")
        if self.peek()[0] == "[":
            self.eat("symbol","[")
            self.fout.write(black+"  <symbol> [ </symbol>"+"\n")
            self.compileExpression(black+"  ")
            self.eat("symbol","]")
            self.fout.write(black+"  <symbol> ] </symbol>"+"\n")
        self.eat("symbol","=")
        self.fout.write(black+"  <symbol> = </symbol>"+"\n")
        self.compileExpression(black+"  ")
        self.eat("symbol",";")
        self.fout.write(black+"  <symbol> ; </symbol>"+"\n")
        self.fout.write(black+"</Let>\n")
        
    def compileIf(self,black=""):
        self.fout.write(black+"<If>\n")
        self.eat("keyword","if")
        self.fout.write(black+"  <keyword> if </keyword>"+"\n")
        self.eat("symbol","(")
        self.fout.write(black+"  <symbol> ( </symbol>"+"\n")
        self.compileExpression(black+"  ")
        self.eat("symbol",")")
        self.fout.write(black+"  <symbol> ) </symbol>"+"\n")
        self.eat("symbol","{")
        self.fout.write(black+"  <symbol> { </symbol>"+"\n")
        self.compileStatements(black+"  ")
        self.eat("symbol","}")
        self.fout.write(black+"  <symbol> } </symbol>"+"\n")
        if self.peek()[0] == "else":
            self.eat("keyword","else")
            self.fout.write(black+"  <keyword> else </keyword>"+"\n")
            self.eat("symbol","{")
            self.fout.write(black+"  <symbol> { </symbol>"+"\n")
            self.compileStatements(black+" ")
            self.eat("symbol","}")
            self.fout.write(black+"  <symbol> } </symbol>"+"\n")
        self.fout.write(black+"</If>\n")
    def compileWhile(self,black=""):
        self.fout.write(black+"<While>\n")
        self.eat("keyword","while")
        self.fout.write(black+"  <keyword> while </keyword>"+"\n")
        self.eat("symbol","(")
        self.fout.write(black+"  <symbol> ( </symbol>"+"\n")
        self.compileExpression(black+"  ")
        self.eat("symbol",")")
        self.fout.write(black+"  <symbol> ) </symbol>"+"\n")
        self.eat("symbol","{")
        self.fout.write(black+"  <symbol> { </symbol>"+"\n")
        self.compileStatements(black+" ")
        self.eat("symbol","}")
        self.fout.write(black+"  <symbol> } </symbol>"+"\n")
        self.fout.write(black+"</While>\n")
        
    def compileDo(self,black=""):
        self.fout.write(black+"<Do>\n")
        self.eat("keyword","do")
        self.fout.write(black+"  <keyword> do </keyword>"+"\n")
        func_name = self.eat("identifier")
        self.fout.write(black+"  <identifier> {} </identifier>".format(func_name)+"\n")
        if self.peek()[0] == "(":
            self.eat("symbol","(")
            self.fout.write(black+"  <symbol> ( </symbol>"+"\n")
            self.compileExpressionList(black+"  ")
            self.eat("symbol",")")
            self.fout.write(black+"  <symbol> ) </symbol>"+"\n")
        elif self.peek()[0] == ".":
            self.eat("symbol",".")
            self.fout.write(black+"  <symbol> . </symbol>"+"\n")
            var_name = self.eat("identifier")
            self.fout.write(black+"  <identifier> {} </identifier>".format(var_name)+"\n")
            self.eat("symbol","(")
            self.fout.write(black+"  <symbol> ( </symbol>"+"\n")
            self.compileExpressionList(black+"  ")
            self.eat("symbol",")")
            self.fout.write(black+"  <symbol> ) </symbol>"+"\n")
        else:
            raise Exception('error in Do')
        self.eat("symbol",";")
        self.fout.write(black+"  <symbol> ; </symbol>"+"\n")
        self.fout.write(black+"</Do>\n")
    def compileReturn(self,black=""):
        self.fout.write(black+"<Return>\n")
        self.eat("keyword","return")
        self.fout.write(black+"  <keyword> return </keyword>"+"\n")
        if self.peek()[0] == ";":
            self.eat("symbol",";")
            self.fout.write(black+"  <symbol> ; </symbol>"+"\n")
        else:
            self.compileExpression(black+"  ")
            self.eat("symbol",";")
            self.fout.write(black+"  <symbol> ; </symbol>"+"\n")
        self.fout.write(black+"</Return>\n")
        
    def compileExpression(self,black=""):
        self.fout.write(black+"<expression>\n")
        self.compileTerm(black+"  ")
        while self.peek()[0] in ["+","-","*","/","&","|","<",">","="]:
            op = self.eat("symbol")
            self.fout.write(black+"  <symbol> {} </symbol>".format(op)+"\n")
            self.compileTerm(black+" ")
        self.fout.write(black+"</expression>\n")
        
    def compileTerm(self,black=""):
        self.fout.write(black+"<term>\n")
        if self.peek()[1] == "integerConstant":
            number = self.eat("integerConstant")
            self.fout.write(black+"  <integerConstant> {} </integerConstant>".format(number)+"\n")
        elif self.peek()[0] in ["true","false","null","this"]:
            keyword_constant = self.eat("keyword")
            self.fout.write(black+"  <keyword> {} </keyword>".format(keyword_constant)+"\n")
        elif self.peek()[1] == "stringConstant":
            string_constant = self.eat("stringConstant")
            self.fout.write(black+"  <stringConstant> {} </stringConstant>".format(string_constant)+"\n")
        elif self.peek()[1] == "identifier":
            var_name = self.eat("identifier")
            self.fout.write(black+"  <identifier> {} </identifier>".format(var_name)+"\n")
            if self.peek()[0] == "[":
                self.eat("symbol","[")
                self.fout.write(black+"  <symbol> [ </symbol>"+"\n")
                self.compileExpression(black+"  ")
                self.eat("symbol","]")
                self.fout.write(black+"  <symbol> ] </symbol>"+"\n")
            elif self.peek()[0] == "(":
                self.eat("symbol","(")
                self.fout.write(black+"  <symbol> ( </symbol>"+"\n")
                self.compileExpressionList(black+"  ")
                self.eat("symbol",")")
                self.fout.write(black+"  <symbol> ) </symbol>"+"\n")
            elif self.peek()[0] == ".":
                self.eat("symbol",".")
                self.fout.write(black+"  <symbol> . </symbol>"+"\n")
                subroutine_name = self.eat("identifier")
                self.fout.write(black+"  <identifier> {} </identifier>".format(subroutine_name)+"\n")
                self.eat("symbol","(")
                self.fout.write(black+"  <symbol> ( </symbol>"+"\n")
                self.compileExpressionList(black+"  ")
                self.eat("symbol",")")
                self.fout.write(black+"  <symbol> ) </symbol>"+"\n")
        elif self.peek()[0] == "(":
            self.eat("symbol","(")
            self.fout.write(black+"  <symbol> ( </symbol>"+"\n")
            self.compileExpression(black+"  ")
            self.eat("symbol",")")
            self.fout.write(black+"  <symbol> ) </symbol>"+"\n")
        elif self.peek()[0] in ["-","~"]:
            unaryOp = self.eat("symbol")
            self.fout.write(black+"  <symbol> {} </symbol>".format(unaryOp)+"\n")
            self.compileTerm(black+"  ")
        else:
            raise Exception('error in term')
            
        self.fout.write(black+"</term>\n")

    def compileExpressionList(self,black=""):
        self.fout.write(black+"<expressionList>\n")
        if self.peek()[1] in ["identifier","stringConstant","integerConstant"] or \
                self.peek()[0] in ["-","~","(","true","false","this","null"]:
            self.compileExpression(black+"  ")
            while self.peek()[0] == ",":
                self.eat("symbol")
                self.fout.write(black+"  <symbol> , </symbol>"+"\n")
                self.compileExpression(black+"  ")
        self.fout.write(black+"</expressionList>\n")
        
    def eat(self,token_type,token=None):
        this_token,this_type = self.tokenizer.thisToken()
        if token:
            assert (this_token == token and this_type == token_type)
        else:
            assert this_type == token_type , this_type
        self.tokenizer.advance()
        return this_token
    def peek(self,n=0):
        return self.tokenizer.peek(n)

if __name__ == "__main__":
    engine = CompilationEngine(sys.argv[1],sys.argv[2])
    engine.compileClass()
