# -*- coding: utf-8 -*-

#########################################################################
# File Name: vm_translater.py
# Created on : 2021-08-29 10:32:16
# Author: kangheng
# Last Modified: 2021-09-04 14:12:14
# Description: VM code translate to asm code 
#########################################################################


import sys

C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_IF = 3
C_FUNCTION = 4
C_RETURN = 5
C_CALL = 6

class Parser():
    commands = ["add","sub","neg","eq","gt","lt","and","or","not"]
    def __init__(self,source_file):
        self._init_codes(source_file)
        self.current_index = 0
    def _init_codes(self,source_file):
        self.lines = []
        with open(source_file) as f:
            for line in f:
                line = line[:line.find("//")].strip()
                if line:
                    self.lines.append(line)
    def hasMoreCommands(self):
        return self.current_index < len(self.lines)
    def advance(self):
        self.current_index += 1
    def currentCommand(self):
        """get this command type and args"""
        code = self.lines[self.current_index]
        parts = code.split()
        if parts[0] in self.commands:
            return C_ARITHMETIC,parts[0],None
        if parts[0] == "push":
            return C_PUSH,parts[1],parts[2]
        if parts[0] == "pop":
            return C_POP,parts[1],parts[2]
        


class CoderWriter():
    def __init__(self,source_name,target_file,debug=False):
        self.f = open(target_file,"w")
        self.debug = debug
        self.source_name = source_name.replace("/",".")

    def close(self):
        self.f.close()

    def writeArithmetic(self,line_num,command):
        if self.debug:
            self.f.write("\n//"+command+"\n")
        if command == "add":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @SP
                   M=M-1
                   A=M
                   M=M+D
                   @SP
                   M=M+1
                   """
        elif command == "sub":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @SP
                   M=M-1
                   A=M
                   M=M-D
                   @SP
                   M=M+1
                   """
        elif command == "and":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @SP
                   M=M-1
                   A=M
                   M=M&D
                   @SP
                   M=M+1
                   """
        elif command == "or":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @SP
                   M=M-1
                   A=M
                   M=M|D
                   @SP
                   M=M+1
                   """
        elif command == "neg":
            code = """
                   @SP
                   M=M-1
                   A=M
                   M=-M
                   @SP
                   M=M+1
                   """
        elif command == "not":
            code = """
                   @SP
                   M=M-1
                   A=M
                   M=!M
                   @SP
                   M=M+1
                   """
        elif command == "eq":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @SP
                   M=M-1
                   A=M
                   @{0}
                   M-D;JEQ
                   @SP
                   A=M
                   M=0
                   @SP
                   M=M+1
                   @{1}
                   0;JMP
                   ({0})
                   @SP
                   A=M
                   M=-1
                   @SP
                   M=M+1
                   ({1})
                   """.format(self.source_name+"_"+str(line_num)+"eq",\
                              self.source_name+"_"+str(line_num)+"_exit")

        elif command == "gt":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @SP
                   M=M-1
                   A=M
                   @{0}
                   D-M;JGT
                   @SP
                   A=M
                   M=0
                   @SP
                   M=M+1
                   @{1}
                   0;JMP
                   ({0})
                   @SP
                   A=M
                   M=-1
                   @SP
                   M=M+1
                   ({1})
                   """.format(self.source_name+"_"+str(line_num)+"gt",\
                              self.source_name+"_"+str(line_num)+"_exit")
        elif command == "lt":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @SP
                   M=M-1
                   A=M
                   @{0}
                   D-M;JLT
                   @SP
                   A=M
                   M=0
                   @SP
                   M=M+1
                   @{1}
                   0;JMP
                   ({0})
                   @SP
                   A=M
                   M=-1
                   @SP
                   M=M+1
                   ({1})
                   """.format(self.source_name+"_"+str(line_num)+"gt",\
                              self.source_name+"_"+str(line_num)+"_exit")

        code = "\n".join(code.split())
        self.f.write(code)

    def writePush(self,line_num,segment,value):
        if self.debug:
            self.f.write("\n//"+"push "+segment+" "+value+"\n")
        if segment in ["local","argument","this","that"]:
            segment = {"local":"LCL","argument":"ARG","this":"THIS","that":"THAT"}[segment]
            code = """
                   @{0}
                   D=M
                   @{1}
                   A=D+A
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(segment,value)
        if segment == "constant":
            code = """
                   @{0}
                   D=A
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(value)
        if segment == "static":
            code = """
                   @{0}
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(self.source_name + "."+str(value))
        if segment == "pointer":
            code = """
                   @{0}
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format({"0":"THIS","1":"THAT"}[value])
        if segment == "temp":
            code = """
                   @{0}
                   D=M
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M+1
                   """.format(int(value)+5)
        code = "\n".join(code.split())
        self.f.write(code)

    def writePop(self,line_num,segment,value):
        if self.debug:
            self.f.write("\n//"+"pop "+segment+" "+value+"\n")
        if segment in ["local","argument","this","that"]:
            segment = {"local":"LCL","argument":"ARG","this":"THIS","that":"THAT"}[segment]
            code = """
                   @{0}
                   D=M
                   @{1}
                   D=D+A
                   @SP
                   A=M
                   M=D
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @SP
                   A=M+1
                   A=M
                   M=D
                   """.format(segment,value)
        if segment == "static":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @{0}
                   M=D
                   """.format(self.source_name + "."+str(value))
        if segment == "pointer":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @{0}
                   M=D
                   """.format({"0":"THIS","1":"THAT"}[value])
        if segment == "temp":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @{0}
                   M=D
                   """.format(int(value)+5)
        code = "\n".join(code.split())
        self.f.write(code)


if __name__ == "__main__":
    source_file = sys.argv[1]
    target_file = sys.argv[2]
    parser = Parser(source_file)
    writer = CoderWriter(source_file,target_file,debug=True)
    line = 1
    while parser.hasMoreCommands():
        command,op1,op2 = parser.currentCommand()
        if command == C_ARITHMETIC:
           writer.writeArithmetic(line,op1)
        if command == C_PUSH:
           writer.writePush(line,op1,op2)
        if command == C_POP:
           writer.writePop(line,op1,op2)
        parser.advance()
        line += 1

    writer.close()



    
