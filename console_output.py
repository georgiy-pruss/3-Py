# encoding: utf-8

## export:
## ww([str]) print new line w/o arg
## cc([color]) default white, colors are F_ B_ * _K _B _G _R _M _C _Y _W _I
## xx([row[,col]]) 0-based, default 0

import ctypes,win32console,atexit

co_kernel32 = ctypes.windll.kernel32
co_orig_cp = win32console.GetConsoleOutputCP()
win32console.SetConsoleOutputCP(65001)
co_stdout = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
co_stdout_int = ctypes.windll.kernel32.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
def co_exit(): win32console.SetConsoleOutputCP(co_orig_cp)
atexit.register(co_exit)

def ww(s='\n'):
  co_stdout.WriteConsole(s)

F_K = 0
F_B = win32console.FOREGROUND_BLUE
F_G = win32console.FOREGROUND_GREEN
F_R = win32console.FOREGROUND_RED
F_I = win32console.FOREGROUND_INTENSITY
F_M = F_R|F_B
F_C = F_B|F_G
F_Y = F_G|F_R
F_W = F_R|F_G|F_B
B_K = 0
B_B = win32console.BACKGROUND_BLUE
B_G = win32console.BACKGROUND_GREEN
B_R = win32console.BACKGROUND_RED
B_I = win32console.BACKGROUND_INTENSITY
B_M = B_R|B_B
B_C = B_B|B_G
B_Y = B_G|B_R
B_W = B_R|B_G|B_B

def cc( c=F_W ):
  co_stdout.SetConsoleTextAttribute(c) # won't work in cygwin

def xx( row=0, col=0 ):
  ctypes.windll.kernel32.SetConsoleCursorPosition(co_stdout_int,row*65536+col)


if __name__=="__main__":
  cc(F_W|F_I)
  ww( "\n \xC2 \xe2 \xce \xee \u0102 \u0103 " )    # A^ a^ I^ i^ A( a(
  ww( "\u0218 \u0219 \u021a \u021b " )             # S, s, T, t, with comma, right ones
  ww( "(\u015e \u015f \u0162 \u0163) \u2013 " )    # S, s, T, t, with cedilas, wrong ones
  ww( "á é í ó ú â î ă ș ț Ș Ț (Ş ş Ţ ţ) ☺\n\n" )  # the last is :-)
  for b in range(16):
    cc(F_W|F_I)
    ww(' %x_ '%b)
    cc(b*16); ww(' ')
    for f in range(16):
      cc(b*16+f)
      ww('%x '%f)
    cc(0)
    ww('\n')
  cc(F_W|B_K)
  ww()

  def wr(x,y):
    for c in range(x,y):
      if 450<=c<500 or 550<=c<700 or 750<=c<850: continue
      if 7850<=c<7900 or 7950<=c<8200 or 8400<=c<8450: continue
      if 8650<=c<8700 or 8850<=c<8950 or 9000<=c<9450: continue
      if 9700<=c<9750: continue
      if c%50==00: ww("%4d "%(c))
      ww( chr(c) )
      if c%50==49: ww()

  wr( 150, 1200)
  wr(7800, 9850)

  ww()
