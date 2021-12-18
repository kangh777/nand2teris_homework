import sys
import os

from CompilationEngine import CompilationEngine

class JackCompile():

    def __init__(self,input_path,output_path = None):
        self.input_files = []
        if os.path.isfile(input_path):
            if input_path.endswith(".jack"):
                self.input_files.append(input_path)
            self.output_dir = os.path.dirname(input_path)
        elif os.path.isdir(input_path):
            for f in os.listdir(input_path): 
                if f.endswith(".jack"):
                    self.input_files.append(os.path.join(input_path,f))
            self.output_dir = input_path
        else:
            raise  Exception(f"unknow path : {input_path}")
        if output_path:
            self.output_dir = output_path

    def compile(self):
        for input_file in self.input_files:
            output_file = os.path.basename(input_file.rstrip(".jack")) + ".vm"
            output_file = os.path.join(self.output_dir,output_file)
            engine = CompilationEngine(input_file,output_file)
            engine.compileClass()


if __name__ == "__main__":
    analyze = JackCompile(sys.argv[1],sys.argv[2])
    analyze.compile()


