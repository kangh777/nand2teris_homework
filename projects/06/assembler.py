# -*- coding: utf-8 -*-

#########################################################################
# File Name: assembler.py
# Created on : 2021-08-27 21:25:02
# Author: kangheng
# Last Modified: 2021-08-28 21:17:11
# Description: 汇编到机器码的翻译
#########################################################################

import sys

class Assembler:
    def __init__(self,source_file):

        self._init_codes(source_file)
        self._init_symbol()
        self._init_code_dict()

    def _init_codes(self,source_file):
        self.lines = []
        with open(source_file) as f:
            for line in f:
                line = line[:line.find("//")].strip()
                if line:
                    self.lines.append(line)

    def _init_symbol(self):
        self.symbol = {"SCREEN":16384,"KBD":24576,"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4}
        for i in range(16):
            self.symbol["R"+str(i)] = i
        lines_cleaned = []
        for code in self.lines:
            if code.startswith("("):
                s = code[1:-1]
                self.symbol[s] = len(lines_cleaned)
            else:
                lines_cleaned.append(code)
        self.lines = lines_cleaned
        current_addr = 16
        for code in self.lines:
            if code.startswith("@") and code[1:] not in self.symbol and not code[1:].isdigit():
                self.symbol[code[1:]] = current_addr
                current_addr += 1

    def _init_code_dict(self):
        self.comp2code = {"0":"0101010",
                          "1":"0111111",
                          "-1":"0111010",
                          "D":"0001100",
                          "A":"0110000",
                          "!D":"0001101",
                          "!A":"0110001",
                          "-D":"0001111",
                          "-A":"0110011",
                          "D+1":"0011111",
                          "A+1":"0110111",
                          "D-1":"0001110",
                          "A-1":"0110010",
                          "D+A":"0000010",
                          "D-A":"0010011",
                          "A-D":"0000111",
                          "D&A":"0000000",
                          "D|A":"0010101",
                          "M":"1110000",
                          "!M":"1110001",
                          "-M":"1110011",
                          "M+1":"1110111",
                          "M-1":"1110010",
                          "D+M":"1000010",
                          "D-M":"1010011",
                          "M-D":"1000111",
                          "D&M":"1000000",
                          "D|M":"1010101",
                          }
        self.dest2code = {"null":"000",
                          "M":"001",
                          "D":"010",
                          "MD":"011",
                          "A":"100",
                          "AM":"101",
                          "AD":"110",
                          "AMD":"111"}
        self.jump2code = {"null":"000",
                          "JGT":"001",
                          "JEQ":"010",
                          "JGE":"011",
                          "JLT":"100",
                          "JNE":"101",
                          "JLE":"110",
                          "JMP":"111"}

    def _parse_comp(self,code):
        if "=" in code and ";" in code:
            comp = code[code.find("=")+1:code.find(";")].strip()
        elif "=" in code :
            comp = code[code.find("=")+1:].strip()
        elif ";" in code :
            comp = code[:code.find(";")].strip()
        else:
            comp = code.strip()
        return comp 


    def _parse_dest(self,code):
        if "=" in code :
            return code.split("=")[0].strip()
        else:
            return "null"

    def _parse_jump(self,code):
        if ";" in code :
            return code.split(";")[-1].strip()
        else:
            return "null"

    def encode(self,output_file):
        codes = []
        for line in self.lines:
            # type a command
            if line.startswith("@"):
                if line[1:] in self.symbol:
                    addr = self.symbol[line[1:]]
                else:
                    addr = int(line[1:])
                addr_bin = str(bin(addr))[2:]
                if len(addr_bin) < 15:
                    addr_bin = "0"*(15-len(addr_bin)) + addr_bin
                else:
                    addr_bin = addr_bin[-15:]
                code = "0"+addr_bin
                codes.append(code)
            # type c command
            else:
                comp = self._parse_comp(line)
                dest = self._parse_dest(line)
                jump = self._parse_jump(line)
                code = "111" + self.comp2code[comp] + self.dest2code[dest] + self.jump2code[jump]
                codes.append(code)

        with open(output_file,"w") as f:
            for code in codes:
                f.write(code+"\n")





if __name__ == "__main__":
    assembler = Assembler(sys.argv[1])
    assembler.encode(sys.argv[2])
        
