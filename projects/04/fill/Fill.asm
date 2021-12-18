// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(MAIN)
    @KBD 
    D=M
    @NEXT
    D;JEQ
    @FILL1
    0;JMP
    @MAIN
    0;JMP
(NEXT)
    @FILL0
    0;JMP
    @MAIN
    0;JMP


(FILL1)
    @8192
    D=A
    @j
    M=D
    @i
    M=0
    (LOOP1)
        @i
        D=M
        @SCREEN
        A=A+D
        M=-1
        @i
        M=M+1
        D=M
        @j
        D=M-D                  
        @LOOP1
        D;JGT
        @MAIN
        0;JMP

(FILL0)
    @i
    M=0
    @8192
    D=A
    @j
    M=D
(LOOP0)
        @i
        D=M
        @SCREEN
        A=A+D
        M=0
        @i
        M=M+1
        D=M
        @j
        D=M-D
        @LOOP0
        D;JGT
        @MAIN
        0;JMP        