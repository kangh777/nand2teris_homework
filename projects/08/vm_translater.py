# -*- coding: utf-8 -*-

#########################################################################
# File Name: vm_translater.py
# Created on : 2021-08-29 10:32:16
# Author: kangheng
# Last Modified: 2021-10-01 11:33:36
# Description: VM code translate to asm code 
#########################################################################


import sys
import os

C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_IF = 3
C_FUNCTION = 4
C_RETURN = 5
C_CALL = 6
C_LABEL = 7
C_GOTOIF = 9
C_GOTO = 10

class Parser():
    commands = ["add","sub","neg","eq","gt","lt","and","or","not"]
    def __init__(self,source_file):
        self.files = []
        if os.path.isfile(source_file):
            self.files = [source_file]
        if os.path.isdir(source_file):
            self.files = [os.path.join(source_file,f) for f in os.listdir(source_file) if f.endswith(".vm")]
        self.file_names = [f.replace("/",".") for f in self.files]
        self._init_codes()
        self.current_index = 0
    def _init_codes(self):
        self.lines = []
        self.file_line_begin = []
        for source_file in self.files:
            self.file_line_begin.append(len(self.lines))
            with open(source_file) as f:
                for line in f:
                    line = line[:line.find("//")].strip()
                    if line:
                        self.lines.append(line)
    def hasMoreCommands(self):
        return self.current_index < len(self.lines)
    def advance(self):
        self.current_index += 1
    def current_file(self):
        for i,start_idx in enumerate(self.file_line_begin):
            if i == len(self.file_line_begin) - 1 or \
                self.current_index > start_idx and self.current_index < self.file_line_begin[i+1]:
                return self.file_names[i]    
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
        if parts[0] == "label":
            return C_LABEL,parts[1],None
        if parts[0] == "if-goto":
            return C_GOTOIF,parts[1],None
        if parts[0] == "goto":
            return C_GOTO,parts[1],None
        if parts[0] == "call":
            return C_CALL,parts[1],parts[2]
        if parts[0] == "function":
            return C_FUNCTION,parts[1],parts[2]
        if parts[0] == "return":
            return C_RETURN,None,None
        


class CoderWriter():
    def __init__(self,target_file,debug=False):
        self.f = open(target_file,"w")
        self.debug = debug

    def close(self):
        self.f.close()

    def writeArithmetic(self,line_num,command):
        if self.debug:
            self.f.write("\n//"+command+"\n")
        else:
            self.f.write("\n")
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
                   D=M-D
                   @{0}
                   D;JEQ
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
                   """.format("line"+"_"+str(line_num)+"eq",\
                              "line"+"_"+str(line_num)+"_exit")

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
                   """.format("line"+"_"+str(line_num)+"gt",\
                              "line"+"_"+str(line_num)+"_exit")
        elif command == "lt":
            code = """
                   @SP
                   M=M-1
                   A=M
                   D=M
                   @SP
                   M=M-1
                   A=M
                   D=M-D
                   @{0}
                   D;JLT
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
                   """.format("line"+"_"+str(line_num)+"gt",\
                              "line"+"_"+str(line_num)+"_exit")

        code = "\n".join(code.split())
        self.f.write(code)

    def writePush(self,source_name,line_num,segment,value):
        if self.debug:
            self.f.write("\n//"+"push "+segment+" "+value+"\n")
        else:
            self.f.write("\n")
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
                   """.format(source_name + "."+str(value))
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

    def writePop(self,source_name,line_num,segment,value):
        if self.debug:
            self.f.write("\n//"+"pop "+segment+" "+value+"\n")
        else:
            self.f.write("\n")
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
                   """.format(source_name + "."+str(value))
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
    def writeLabel(self,source_name,label):
        if self.debug:
            self.f.write("\n//"+"label "+label+"\n")
        else:
            self.f.write("\n")
        code = """
               ({})
               """.format(source_name+"."+label)
        code = "\n".join(code.split())
        self.f.write(code)
    def writeGotoIf(self,source_name,address):
        if self.debug:
            self.f.write("\n//"+"if-goto "+address+"\n")
        else:
            self.f.write("\n")
        code = """
               @SP
               AM=M-1
               D=M
               @{0}
               D;JNE
               """.format(source_name+"."+address)
        code = "\n".join(code.split())
        self.f.write(code)
    def writeGoto(self,source_name,address):
        if self.debug:
            self.f.write("\n//"+"goto "+address+"\n")
        else:
            self.f.write("\n")
        code = """
               @{0}
               0;JMP
               """.format(source_name+"."+address)
        code = "\n".join(code.split())
        self.f.write(code)
    def writeCall(self,line_num,func,n_args):
        if self.debug:
            self.f.write("\n//"+"call "+func+" "+n_args+"\n")
        else:
            self.f.write("\n")
        code = """
               @SP
               A=M
               M=0
               @SP
               M=M+1
               @{0}
               D=A
               @SP
               A=M
               M=D
               @SP
               M=M+1
               @LCL
               D=M
               @SP
               A=M
               M=D
               @SP
               M=M+1
               @ARG
               D=M
               @SP
               A=M
               M=D
               @SP
               M=M+1
               @THIS
               D=M
               @SP
               A=M
               M=D
               @SP
               M=M+1
               @THAT
               D=M
               @SP
               A=M
               M=D
               @SP
               M=M+1
               @SP
               D=M
               @5
               D=D-A
               @{1}
               D=D-A
               D=D-1
               @ARG
               M=D
               @SP
               D=M
               @LCL
               M=D
               @{2}
               0;JMP
               ({0})
               """.format("func.{}.{}.return".format(func,line_num),
                          n_args,
                          "func.{}".format(func))
                          
        code = "\n".join(code.split())
        self.f.write(code)

    def writeFunc(self,line_num,func,n_vars):
        if self.debug:
            self.f.write("\n//"+"function "+func+" "+n_vars+"\n")
        else:
            self.f.write("\n")
        code = """
               ({0})
               @LCL
               D=M
               @{1}
               A=D+A
               M=0
               ({2})
               @{1}
               D=A
               @LCL
               A=M+D
               D=M
               @{1}
               D=A-D
               @{3}
               D;JLE
               @LCL
               D=M
               @{1}
               A=D+A
               M=M+1
               @SP
               A=M
               M=0
               @SP
               M=M+1
               @{2}
               0;JMP
               ({3})
               """.format("func.{}".format(func),
                          n_vars,
                          "func.{}.initloop".format(func),
                          "func.{}.exit".format(func))
        code = "\n".join(code.split())
        self.f.write(code)
    def writeReturn(self):
        if self.debug:
            self.f.write("\n//"+"return"+"\n")
        else:
            self.f.write("\n")
        code = """
               @SP
               AM=M-1
               D=M
               @ARG
               A=M
               M=D
               @ARG
               D=M
               @SP
               A=M
               M=D
               @SP
               M=M+1
               @LCL
               D=M
               @SP
               A=M
               M=D
               A=D-1
               D=M
               @THAT
               M=D
               @SP
               A=M
               D=M
               @2
               A=D-A
               D=M
               @THIS
               M=D
               @SP
               A=M
               D=M
               @3
               A=D-A
               D=M
               @ARG
               M=D
               @SP
               A=M
               D=M
               @4
               A=D-A
               D=M
               @LCL
               M=D
               @SP
               A=M
               D=M
               @5
               A=D-A
               D=M
               @SP
               A=M-1
               A=M+1
               M=D
               D=A
               @SP
               M=D
               @SP
               A=M
               A=M
               0;JMP
               """
        code = "\n".join(code.split())
        self.f.write(code)
    def writeInit(self):
        if self.debug:
            self.f.write("\n//"+"INIT"+"\n")
        else:
            self.f.write("\n")
        code = """
               @256
               D=A
               @SP
               M=D
               //@func.Sys.init
               //0;JMP
               """
        code = "\n".join(code.split())
        self.f.write(code)
        self.writeCall(-1,"Sys.init","0")

if __name__ == "__main__":
    source_file = sys.argv[1]
    target_file = sys.argv[2]
    parser = Parser(source_file)
    writer = CoderWriter(target_file,debug=True)
    line = 1
    writer.writeInit()
    while parser.hasMoreCommands():
        command,op1,op2 = parser.currentCommand()
        file_name = parser.current_file()
        if command == C_ARITHMETIC:
           writer.writeArithmetic(line,op1)
        if command == C_PUSH:
           writer.writePush(file_name,line,op1,op2)
        if command == C_POP:
           writer.writePop(file_name,line,op1,op2)
        if command == C_LABEL:
           writer.writeLabel(file_name,op1)
        if command == C_GOTOIF:
           writer.writeGotoIf(file_name,op1)
        if command == C_GOTO:
           writer.writeGoto(file_name,op1)
        if command == C_CALL:
           writer.writeCall(line,op1,op2)
        if command == C_FUNCTION:
           writer.writeFunc(line,op1,op2)
        if command == C_RETURN:
           writer.writeReturn()
        parser.advance()
        line += 1

    writer.close()



    
