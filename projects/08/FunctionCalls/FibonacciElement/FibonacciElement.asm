
//INIT
@256
D=A
@SP
M=D
//@func.Sys.init
//0;JMP
//call Sys.init 0
@SP
A=M
M=0
@SP
M=M+1
@func.Sys.init.-1.return
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
@0
D=D-A
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@func.Sys.init
0;JMP
(func.Sys.init.-1.return)
//function Main.fibonacci 0
(func.Main.fibonacci)
@LCL
D=M
@0
A=D+A
M=0
(func.Main.fibonacci.initloop)
@0
D=A
@LCL
A=M+D
D=M
@0
D=A-D
@func.Main.fibonacci.exit
D;JLE
@LCL
D=M
@0
A=D+A
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@func.Main.fibonacci.initloop
0;JMP
(func.Main.fibonacci.exit)
//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@line_4gt
D;JLT
@SP
A=M
M=0
@SP
M=M+1
@line_4_exit
0;JMP
(line_4gt)
@SP
A=M
M=-1
@SP
M=M+1
(line_4_exit)
//if-goto IF_TRUE
@SP
AM=M-1
D=M
@FunctionCalls.FibonacciElement.Main.vm.IF_TRUE
D;JNE
//goto IF_FALSE
@FunctionCalls.FibonacciElement.Main.vm.IF_FALSE
0;JMP
//label IF_TRUE
(FunctionCalls.FibonacciElement.Main.vm.IF_TRUE)
//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//return
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
//label IF_FALSE
(FunctionCalls.FibonacciElement.Main.vm.IF_FALSE)
//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
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
//call Main.fibonacci 1
@SP
A=M
M=0
@SP
M=M+1
@func.Main.fibonacci.14.return
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
@1
D=D-A
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@func.Main.fibonacci
0;JMP
(func.Main.fibonacci.14.return)
//push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
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
//call Main.fibonacci 1
@SP
A=M
M=0
@SP
M=M+1
@func.Main.fibonacci.18.return
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
@1
D=D-A
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@func.Main.fibonacci
0;JMP
(func.Main.fibonacci.18.return)
//add
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
//return
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
//function Sys.init 0
(func.Sys.init)
@LCL
D=M
@0
A=D+A
M=0
(func.Sys.init.initloop)
@0
D=A
@LCL
A=M+D
D=M
@0
D=A-D
@func.Sys.init.exit
D;JLE
@LCL
D=M
@0
A=D+A
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@func.Sys.init.initloop
0;JMP
(func.Sys.init.exit)
//push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
//call Main.fibonacci 1
@SP
A=M
M=0
@SP
M=M+1
@func.Main.fibonacci.23.return
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
@1
D=D-A
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@func.Main.fibonacci
0;JMP
(func.Main.fibonacci.23.return)
//label WHILE
(FunctionCalls.FibonacciElement.Sys.vm.WHILE)
//goto WHILE
@FunctionCalls.FibonacciElement.Sys.vm.WHILE
0;JMP