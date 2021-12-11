1. 为了加速，minmax最后一层用的循环，所以实际深度为depth+1
2. 由于递归非常非常耗时，所以ab剪枝的效果甚至不如minmax
3. 当然如果全改成迭代的话ab剪枝的优势还是很大的，直接把minmax最后一层的循环拿过来都能加速不少
4. 注意向下分支时，如果已经任意一方已经连成5子，应立即停止分支并返回正无穷或负无穷（因为此时游戏已经结束了）（也算是一种加速）
5. 随着后期有效落子位置的增多，算法速度会越来越慢
6. 有效落子位置只考虑了与现有子紧邻的位置（否则根本跑不动。。。）
7. u1s1，深度为2的minmax算法已经能和百度搜索第一个的五子棋下平了。。。
8. 最后，ab剪枝怎么递归的我其实没怎么看懂，照着网上的代码改了下发现能跑就没管了