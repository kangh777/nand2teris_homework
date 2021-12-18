# -*- coding: utf-8 -*- import sys
import sys
import os
from tokenizer import Tokenizer
from SymboTabel import SymbolTabel

class CompilationEngine():

    def __init__(self,input_file,output_file):
        self.file_name = os.path.basename(input_file).rstrip(".jack")
        self.tokenizer = Tokenizer(input_file)
        self.symbols = SymbolTabel()
        self.functions = set()
        self.fout = open(output_file,"w")
        self.kind2vmName = {"static":"static","arg":"argument","var":"local","field":"this"}
        self.binaryop2vmName = {"+":"add","-":"sub","=":"eq","&":"and","|":"or",">":"gt","<":"lt"}
        self.unaryop2vmName = {"-":"neg","~":"not"}

    def compileClass(self):
        self.eat("keyword","class")
        class_name = self.eat("identifier")
        assert self.file_name == class_name
        self.eat("symbol","{")
        while self.peek()[0] in ["static","field"]:
            self.compileClassVarDec()
        while self.peek()[0] in ["constructor","function","method"]:
            self.compileSubroutineDec()
        self.eat("symbol","}")
        
    def compileClassVarDec(self):
        var_pos = self.eat("keyword")
        if self.peek()[1] == "keyword":
            var_type = self.eat("keyword")
        elif self.peek()[1] == "identifier":
            var_type = self.eat("identifier")
        var_name = self.eat("identifier")
        self.symbols.define(var_name,var_type,var_pos)
        while self.peek()[0] == ",":
            self.eat("symbol",",")
            var_name = self.eat("identifier")
            self.symbols.define(var_name,var_type,var_pos)
        self.eat("symbol",";")
    def compileSubroutineDec(self):
        func_type = self.eat("keyword")
        if self.peek()[1] == "keyword":
            return_type = self.eat("keyword")
        elif self.peek()[1] == "identifier":
            return_type = self.eat("identifier")
        else:
            raise Exception('unexpect return type')
        func_name = self.eat("identifier")
        if func_type == "function":
            self.functions.add("{}.{}".format(self.file_name,func_name))
        func_label = "{}.{}".format(self.file_name,func_name)
        self.eat("symbol","(")
        self.symbols.startSuboutine()
        if func_type == "method":
            self.symbols.define("this",self.file_name,"arg")
        self.compileParameterList()
        self.eat("symbol",")")
        if func_type == "function":
            self.compileSubroutineBody(func_label)
        if func_type == "constructor":
            self.compileConstructorBody(func_label)
        if func_type == "method":
            self.compileMethodBody(func_label)
    def compileParameterList(self):
        var_type = None
        while self.peek()[0] in ["int","char","boolean"] or self.peek()[1] == "identifier":
            if self.peek()[0] in ["int","char","boolean"]:
                var_type = self.eat("keyword")
            else:
                var_type = self.eat("identifier")
            var_name = self.eat("identifier")
            self.symbols.define(var_name,var_type,"arg")
            if self.peek()[0] == ",":
                self.eat("symbol")

    def compileSubroutineBody(self,func_label):
        self.eat("symbol","{")
        while self.peek()[0]  == "var":
            self.compileVarDec()
        self.fout.write("function {} {} \n".format(func_label,self.symbols.VarCount("var")))
        self.compileStatements()
        self.eat("symbol","}")

    def compileConstructorBody(self,func_label):
        self.eat("symbol","{")
        while self.peek()[0]  == "var":
            self.compileVarDec()
        self.fout.write("function {} {} \n".format(func_label,self.symbols.VarCount("var")))
        field_num = self.symbols.VarCount("field")
        self.fout.write("push constant {} \n".format(field_num))
        self.fout.write("call Memory.alloc 1 \n")
        self.fout.write("pop pointer 0 \n")
        self.compileStatements()
        self.eat("symbol","}")

    def compileMethodBody(self,func_label):
        self.eat("symbol","{")
        while self.peek()[0]  == "var":
            self.compileVarDec()
        self.fout.write("function {} {} \n".format(func_label,self.symbols.VarCount("var")))
        self.fout.write("push argument 0 \n")
        self.fout.write("pop pointer 0 \n")
        self.compileStatements()
        self.eat("symbol","}")

    def compileVarDec(self):
        self.eat("keyword","var")
        if self.peek()[0] in ["int","char","boolean"]:
            var_type = self.eat("keyword")
        elif self.peek()[1] == "identifier":
            var_type = self.eat("identifier")
        else:
            raise Exception('unexpect in var dec')
        var_name = self.eat("identifier")
        self.symbols.define(var_name,var_type,"var")
        while self.peek()[0] == ",": 
            self.eat("symbol",",")
            var_name = self.eat("identifier")
            self.symbols.define(var_name,var_type,"var")
        self.eat("symbol",";")
        
    def compileStatements(self):
        while self.peek()[0] in ["let","if","while","do","return"]:
            if self.peek()[0] == "let":
                self.compileLet()
            if self.peek()[0] == "if":
                self.compileIf()
            if self.peek()[0] == "while":
                self.compileWhile()
            if self.peek()[0] == "do":
                self.compileDo()
            if self.peek()[0] == "return":
                self.compileReturn()
        
    def compileLet(self):
        self.eat("keyword","let")
        var_name = self.eat("identifier")
        kind = self.symbols.KindOf(var_name)
        index = self.symbols.IndexOf(var_name)
        is_array = False
        if self.peek()[0] == "[":
            is_array = True
            self.eat("symbol","[")
            self.compileExpression()
            self.eat("symbol","]")
            self.fout.write("push {} {} \n".format(self.kind2vmName[kind],index))
            self.fout.write("add \n")
        self.eat("symbol","=")
        self.compileExpression()
        self.eat("symbol",";")
        if not is_array:
            self.fout.write("pop {} {} \n".format(self.kind2vmName[kind],index))
        else:
            self.fout.write("pop temp 0 \n")
            self.fout.write("pop pointer 1 \n")
            self.fout.write("push temp 0 \n")
            self.fout.write("pop that 0 \n")
            
            

        
    def compileIf(self):
        self.eat("keyword","if")
        self.eat("symbol","(")
        self.compileExpression()
        self.fout.write("not \n")
        if_label_str = "IF.{}.{}".format(self.file_name,self.tokenizer.index)
        self.fout.write("if-goto {} \n".format(if_label_str))
        self.eat("symbol",")")
        self.eat("symbol","{")
        self.compileStatements()
        self.eat("symbol","}")
        if self.peek()[0] == "else":
            else_label_str = "ELSE.{}.{}".format(self.file_name,self.tokenizer.index)
            self.fout.write("goto {} \n".format(else_label_str))
        self.fout.write("label {} \n".format(if_label_str))
        if self.peek()[0] == "else":
            self.eat("keyword","else")
            self.eat("symbol","{")
            self.compileStatements()
            self.eat("symbol","}")
            self.fout.write("label {} \n".format(else_label_str))
    def compileWhile(self):
        while_label_str1 = "while.{}.{}.1".format(self.file_name,self.tokenizer.index)
        while_label_str2 = "while.{}.{}.2".format(self.file_name,self.tokenizer.index)
        self.eat("keyword","while")
        self.eat("symbol","(")
        self.fout.write("label {} \n".format(while_label_str1))
        self.compileExpression()
        self.fout.write("not \n")
        self.fout.write("if-goto {} \n".format(while_label_str2))
        self.eat("symbol",")")
        self.eat("symbol","{")
        self.compileStatements()
        self.eat("symbol","}")
        self.fout.write("goto {} \n".format(while_label_str1))
        self.fout.write("label {} \n".format(while_label_str2))
        
    def compileDo(self):
        self.eat("keyword","do")
        func_name = self.eat("identifier")
        if self.peek()[0] == "(":
            self.eat("symbol","(")
            if func_name in self.functions:
                n = self.compileExpressionList()
                self.fout.write("call {} {} \n".format(self.file_name+"."+func_name,n))
            else:
                self.fout.write("push pointer 0 \n")
                n = self.compileExpressionList()
                self.fout.write("call {} {} \n".format(self.file_name+"."+func_name,n+1))
            self.eat("symbol",")")
            self.fout.write("pop temp 0 \n")
        elif self.peek()[0] == ".":
            self.eat("symbol",".")
            subroutine_name = self.eat("identifier")
            self.eat("symbol","(")
            if func_name in self.symbols.Name2info:
                kind = self.symbols.KindOf(func_name)
                index = self.symbols.IndexOf(func_name)
                self.fout.write("push {} {} \n".format(self.kind2vmName[kind],index))
                n = self.compileExpressionList()
                self.eat("symbol",")")
                class_name = self.symbols.TypeOf(func_name)
                self.fout.write("call {}.{} {} \n".format(class_name,subroutine_name,n+1))
                self.fout.write("pop temp 0 \n")
            else:
                n = self.compileExpressionList()
                self.eat("symbol",")")
                self.fout.write("call {}.{} {} \n".format(func_name,subroutine_name,n))
                self.fout.write("pop temp 0 \n")
        else:
            raise Exception('error in Do')
        self.eat("symbol",";")
    def compileReturn(self):
        self.eat("keyword","return")
        if self.peek()[0] == ";":
            self.eat("symbol",";")
            self.fout.write("push constant 0 \n")
            self.fout.write("return \n")
        else:
            self.compileExpression()
            self.eat("symbol",";")
            self.fout.write("return \n")
        
    def compileExpression(self):
        self.compileTerm()
        while self.peek()[0] in ["+","-","*","/","&","|","<",">","="]:
            op = self.eat("symbol")
            self.compileTerm()
            if op in self.binaryop2vmName:
                self.fout.write("{} \n".format(self.binaryop2vmName[op]))
            elif op == "*":
                self.fout.write("call Math.multiply 2 \n")
            elif op == "/":
                self.fout.write("call Math.divide 2 \n")

        
    def compileTerm(self):
        if self.peek()[1] == "integerConstant":
            number = self.eat("integerConstant")
            self.fout.write("push constant {} \n".format(number))
        elif self.peek()[0] in ["true","false","null","this"]:
            if self.peek()[0] == "true":
                self.fout.write("push constant 1 \n")
                self.fout.write("neg \n")
            if self.peek()[0] == "false":
                self.fout.write("push constant 0 \n")
            if self.peek()[0] == "null":
                self.fout.write("push constant 0 \n")
            if self.peek()[0] == "this":
                self.fout.write("push pointer 0 \n")
            keyword_constant = self.eat("keyword")
        elif self.peek()[1] == "stringConstant":
            string_constant = self.eat("stringConstant")
            self.fout.write("push constant {} \n".format(len(string_constant)))
            self.fout.write("call String.new 1 \n")
            for c in string_constant:
                self.fout.write("push constant {} \n".format(ord(c)))
                self.fout.write("call String.appendChar 2 \n")
        elif self.peek()[1] == "identifier":
            var_name = self.eat("identifier")
            if self.peek()[0] == "[":
                self.eat("symbol","[")
                kind = self.symbols.KindOf(var_name)
                index = self.symbols.IndexOf(var_name)
                self.fout.write("push {} {} \n".format(self.kind2vmName[kind],index))
                self.compileExpression()
                self.fout.write("add \n".format(self.kind2vmName[kind],index))
                self.fout.write("pop pointer 1 \n")
                self.fout.write("push that 0 \n")
                self.eat("symbol","]")
            elif self.peek()[0] == "(":
                self.eat("symbol","(")
                if self.file_name+"."+var_name in self.functions:
                    n = self.compileExpressionList()
                    self.fout.write("call {} {} \n".format(self.file_name+"."+var_name,n))
                else:
                    self.fout.write("push pointer 0 \n")
                    n = self.compileExpressionList()
                    self.fout.write("call {} {} \n".format(self.file_name+"."+var_name,n+1))
                self.eat("symbol",")")
            elif self.peek()[0] == ".":
                self.eat("symbol",".")
                subroutine_name = self.eat("identifier")
                self.eat("symbol","(")
                if var_name in self.symbols.Name2info:
                    kind = self.symbols.KindOf(var_name)
                    index = self.symbols.IndexOf(var_name)
                    class_name = self.symbols.TypeOf(var_name)
                    self.fout.write("push {} {} \n".format(self.kind2vmName[kind],index))
                    n = self.compileExpressionList()
                    self.fout.write("call {}.{} {} \n".format(class_name,subroutine_name,n+1))
                else:
                    n = self.compileExpressionList()
                    self.fout.write("call {}.{} {} \n".format(var_name,subroutine_name,n))
                self.eat("symbol",")")
            else:
                kind = self.symbols.KindOf(var_name)
                index = self.symbols.IndexOf(var_name)
                self.fout.write("push {} {} \n".format(self.kind2vmName[kind],index))
        elif self.peek()[0] == "(":
            self.eat("symbol","(")
            self.compileExpression()
            self.eat("symbol",")")
        elif self.peek()[0] in ["-","~"]:
            unaryOp = self.eat("symbol")
            self.compileTerm()
            if unaryOp == "-":
                self.fout.write("neg \n")
            elif unaryOp == "~":
                self.fout.write("not \n")
        else:
            raise Exception('error in term')

    def compileExpressionList(self):
        expression_num = 0
        if self.peek()[1] in ["identifier","stringConstant","integerConstant"] or \
                self.peek()[0] in ["-","~","(","true","false","this","null"]:
            self.compileExpression()
            expression_num += 1
            while self.peek()[0] == ",":
                self.eat("symbol")
                self.compileExpression()
                expression_num += 1
        return expression_num
        
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
