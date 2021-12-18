# -*- coding: utf-8 -*-

class SymbolTabel():
    def __init__(self):
        self.Name2info = {}
        self.kind2Array = {"static":[],"field":[],"arg":[],"var":[]}
    def startSuboutine(self):
        for arg_info in self.kind2Array["arg"]:
            self.Name2info.pop(arg_info)
        for var_info in self.kind2Array["var"]:
            self.Name2info.pop(var_info)
        self.kind2Array["arg"] = []
        self.kind2Array["var"] = []
    def define(self,name,type,kind):
        if name in self.Name2info:
            raise Exception("same name : {}".format(name))
        self.Name2info[name] = (type,kind,len(self.kind2Array[kind]))
        self.kind2Array[kind].append(name)
    def VarCount(self,kind):
        return len(self.kind2Array[kind])
    def KindOf(self,name):
        return self.Name2info[name][1]
    def TypeOf(self,name):
        if name == "this":
            return "field"
        return self.Name2info[name][0]
    def IndexOf(self,name):
        if name == "this":
            return 0
        return self.Name2info[name][2]
