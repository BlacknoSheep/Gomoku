# Gomoku
xjb写的垃圾五子棋
算法：minmax，alpha beta剪枝
评分表只考虑了非常简单的情况
	         1	  2	     3	     4	    >=5
free	    _O_	 _OO_	 _OOO_ 	_OOOO_	  win
half-free	XO_	 XOO_	 XOOO_	XOOOO_    win

	         1	  2	     3	     4	    >=5
free	     10	 100	 1000	  10000	   100000
half-free	  1	  10	  100	   1000	   100000
