# NOTES

## 什么是复杂度
​	在设计满足问题要求的算法时，复杂度的估算是非常重要的。我们不可能把每个想到的算法都去实现一遍看看是否足够快。应当通过估算算法的复杂度来判断所想的算法是否足够高效。在分析复杂度时，我们通常考虑它与什么成正比，并称之为算法的阶。例如程序执行了四重循环，每重n次，运行时间与n^4^成正比。我们将与n^4^成正比写作O(n^4^), 将对应的运行时间写作O(n^4^)时间。

​	这里介绍的大O号，严格来说并不是通过正比关系定义的，不过刚开始时这样理解也无妨。另外，我们也常常省略“时间”二字，用O(n^4^)来表示与n^4^成正比的运行时间。

## 关于运行时间
​	程序的运行时间不光取决于复杂度，也会受诸如循环体的复杂性等因素的影响。但是，因此造成的差距多数情况下最多也就几十倍。另一方面，忽略其余因素，n=1000时，O(n^3^)时间的算法和O(n^2^)时间的算法的差距就是1000倍。因此要缩短程序的运行时间，主要应该从复杂度人手。
估算出算法的复杂度后，只要将数值可能的最大值代入复杂度的渐近式中，就能简单地判断算法是否能够满足运行时间限制的要求。例如，考虑O(n^2^)时间的算法，假设题目描述中的限制条件为n≤1000, 将n=1000代入n^2^就得到了1000000。在这个数值的基础上，我们就可以结合下表进行判断了。
​														假设时间限制为1秒

| 1000000   | 游刃有余                     |
| --------- | ---------------------------- |
| 10000000  | 勉勉强强                     |
| 100000000 | 很悬，仅限循环体常简单的情况 |

## 编码规范

PEP 8 — the Style Guide for Python Code, https://pep8.org/

Python 编码规范(Google), https://www.runoob.com/w3cnote/google-python-styleguide.html

## 一维数组可以浅拷贝，二维数组用列表解析创建、复制需要深拷贝

需要清楚，浅拷贝shallow copy会在什么情况下出现问题，二维数组复制需要深拷贝deepcopy。

==二维数组的创建需要用列表解析方式创建，如下面第15行。如果复制需要用深拷贝，如下面第41和42行。记住，python语法就是这样，确实不如C++方便。==

举例：

```python
row =3; col = 4

# 1D array
A1 = [0] * col
A1_copy = A1[:]
A1_copy[1] = 1

# two methods to output
print("#1D array")
print(A1)
print(A1_copy)
print(' '.join(map(str, A1_copy)), sep='\n')
print()

# 2D array    
matrix = [[-1] * col for _ in range(row)]

# two methods to output
print("#2D array")
print("#method1 output")
for i in range(row):
    print(matrix[i])
print()

# ' '.join(row) for row in matrix) returns a string for every row, 
#   e.g. A B when row is ["A", "B"].
#
# *(' '.join(row) for row in matrix), sep='\n') unpacks the generator 
#   returning the sequence 'A B', 'C D', so that print('A B', 'C D', sep='\n') 
#   is called for the example matrix given.
print("#method2 output")
print( *(' '.join(map(str, row)) for row in matrix), sep='\n')
print()

print("#change one element")
matrix[0][1] = 2
for i in range(row):
    print(matrix[i])
print()

import copy
mx_copy = copy.deepcopy(matrix)     # matrix copied
print( *(' '.join(map(str, row)) for row in mx_copy), sep='\n')
print()
```



程序运行，输出结果

```
#1D array
[0, 0, 0, 0]
[0, 1, 0, 0]
0 1 0 0

#2D array
#method1 output
[-1, -1, -1, -1]
[-1, -1, -1, -1]
[-1, -1, -1, -1]

#method2 output
-1 -1 -1 -1
-1 -1 -1 -1
-1 -1 -1 -1

#change one element
[-1, 2, -1, -1]
[-1, -1, -1, -1]
[-1, -1, -1, -1]

-1 2 -1 -1
-1 -1 -1 -1
-1 -1 -1 -1
```



如：

OJ.12560 生存游戏，矩阵创建时候，注意避免浅拷贝创建。

OJ.02754 八皇后，发现一个解的时候，注意避免浅拷贝。



## 需要先申请到内存空间，才能使用

指针是内存地址，类似门牌号，要找人得到具体物理位置，门牌号里面找不到。

例如：ma=[[0]\*(m+2)]*(n+2) 只是一个指针，还没有拿到空间。

在Python中，变量 `ma` 的赋值 `[[0]*(m+2)]*(n+2)` 只是创建了一个指向空间的引用，并没有实际申请到内存空间。

需要注意的是，这种方式创建二维列表时，内层列表的元素实际上是共享的，它们指向同一块内存空间。这意味着如果你修改了其中一个内层列表的元素，会影响到其他内层列表中对应位置的元素。

如果你想创建独立的内层列表，可以使用列表推导式来实现，例如：

```
ma = [[0] * (m + 2) for _ in range(n + 2)]
```

这样每个内层列表都会有自己独立的内存空间，避免了共享元素的问题。

![image-20231021105913274](https://raw.githubusercontent.com/GMyhf/img/main/img/image-20231021105913274.png)



## 变量名起的有意义

可以按照题面描述中用到的符号，起变量名，或者起有意义的变量名。

避免程序写长后，混淆使用变量名。尤其是二维数组的行列变量，注意不要混淆

## 数据结构dict, set时间复杂度是O(1)

dict, set的时间复杂度低，能用的时候优先使用。

## 通常使用split()，而不是split(' ')

对于codeforces，或者openjudge，接收输入，通常不需要自己指定分隔符。

## 函数默认参数

可以参考 OJ 1756 八皇后的递归函数，第一次调用，使用了默认参数。def queen(A, cur=0):

## 精确到小数点后9位

print(f'{x:.9f}')	# x 是变量

## enumerate函数

The basic syntax is is *enumerate(sequence, start=0)*

The output object includes a counter like so: (0, thing[0]), (1, thing[1]), (2, thing[2]),！

如在 OJ.21554 排队做实验 中使用。

## 浮点数判断相等

通常是 return abs(f1 - f2) <= allowed_error 。例如：OJ12065方程求解，可以allowed_error = 1e-12

## 不同进制输出

例如：http://cs101.openjudge.cn/practice/18224/  找魔数的输出。print(bin(num), oct(num), hex(num))

## **在终端中调试Python程序**

打开终端窗口，并进入到程序所在的目录。

输入python -m pdb 文件名.py，其中文件名.py是您的程序文件名。

运行命令后，终端会进入pdb调试器的交互界面。可以看到一个 (Pdb) 提示符。

可以使用 pdb 提供的命令来进行调试，例如：

l：显示当前代码的上下文环境，即查看当前位置附近的代码。

n：执行下一行代码。

s：进入函数内部。

p 变量名：打印变量的值。

c：继续执行程序直到下一个断点或程序结束。


