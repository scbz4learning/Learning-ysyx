# Digital Circuits

## MOS, nMOS, pMOS, CMOS

简单来说，  

- MOS 相当于自动开关  
- 一相的 MOS 只能导通和断开  
- 数字电路不能悬空，如果想要低电平，必须要接地  
- 所以两相的 MOS 混合用，就能表示导通断开两个状态了。  

!!!note
    早期只用 nMOS，低电平表示 0，所以串一个电阻，默认nMOS截止，电流通过电阻变小，表示 0；如果想要高电平，就导通 MOS，电阻短路，表示高电平。  


## 门电路
![分析门电路](../assets/images/F/分析门电路00.png)
![分析门电路](../assets/images/F/分析门电路01.png)
![分析门电路](../assets/images/F/分析门电路10.png)
![分析门电路](../assets/images/F/分析门电路11.png)


### 或门

首先看之前的与非门。  

![与非门](../assets/images/F/与非门.png)

两个 cmos，nMOS 必须和VCC连接，pMOS 必须和地连接（否则会出现两连通或者两截止）。所以思考的时候，需要：永远 0 对应 VCC 导通

下面要考虑的就是，怎么安排串并联，让  
1. 两个行为相反  
2. 满足逻辑  

与非要求的就是：  

1. 11 时，VCC 截止，地连通   
    - 只有 11 时 VCC 截止，即其他时候导通    
    - nMOS 应该并联 - 一个导通，VCC就导通，只有两个都不导通，才VCC截止     
    - 只有11 地连通，其他时候截止    
    - pMOS 应该串联 - 都导通，才能导通    
2. 其他时候，VCC连通，地截止  

!!!note
    两个 cMOS 只能表示两种状态。  
    为什么这两种状态是 与非 & 或非？因为输入 0 对应 VCC 导通。  
    与 和 或 要更多的cMOS才行。（多一个非）。

所以类似地分析或非：

00时，VCC 连通，地截止  

- 只有 00 时，VCC 连通，nMOS 应该串联
- 所以 pMOS 应该并联

![或非](../assets/images/F/或非.gif)

再加一个非门：

![或](../assets/images/F/或.gif)


### 三输入与非门

最少情况下，全定制电路只需要3对CMOS。

对于半定制门电路，不难想象，对于 与非、或非 的连接，只要按照前缀和顺序安排 nMOS 串并联 和 pMOS 的相反串并联即可。所以任何 与非 和 或非 的表达式，需要的晶体管数量都应该等同于输入信号的两倍。

!!!note
    想到离散数学了吗？一个 Trivial 的思想显然是：  

    对于门电路：任意 n 输入布尔表达式都能化为仅含 NAND / NOR 与若干 NOT 的前缀析构形式。其 CMOS 实现所需的晶体管总数满足：

    $$
    T = 2 \times (\text{NAND/NOR 门的输入总数}) + 2 \times (\text{NOT 门数量})
    $$

    且

    $$
    \text{NOT 门数量} \le n
    $$

    (verified by ChatGPT 5 & Gemini 2.5 Pro)

两个逻辑门需要 4+2+4 = 10 个晶体管，因为需要 与非 (4) + 非 (2) + 与非 (4)。

对于区分上拉下拉网络的全定制电路，每多一个输入，会多一对晶体管，且由于只能对表达式进行有限的化简，可能多更多的非门。

后面可以看到，不区分上下拉网络时，可以用到更少的电路。如 同或 和 异或 都只需要 6 根，而非 8 根。

~~这种成本显然并不大 -- 多 20% 左右的~~ 显然不只有 20%。那为什么不用全定制呢？开发时间长？显然是，但是基于 AI 的自动推理简化程序就像自动布线一样重要了 -- 肯定还是手动更优，但是下降一定比例的冗余晶体管带来的成本优化似乎是显然的。这可能就是为什么 EDA 这么需要 AI 吧。

另一个更重要的方面是效率。多一倍的晶体管带来的成本绝不如性能开销显著，可以猜测我电脑 CPU、GPU、NPU 等肯定用了很大比例的全定制。。。

### 异或门

异或 和 或 很像，但是 11 的结果不同，而 11 可以用 与 表示， 所以 A XOR B 的逻辑可以描述为 `(A OR B) 且 (A AND B) 为假`，由此可以推导出：

$$
\begin{align*}
\text{A XOR B} &= (\text{A OR B}) \text{ AND } (\text{A NAND B}) \\
               &= (\text{NOT } (\text{A NOR B})) \text{ AND } (\text{A NAND B}) \\
               &= \text{NOT } ( (\text{A NOR B}) \text{ OR } (\text{NOT } (\text{A NAND B})) ) \\
               &= (\text{A NOR B}) \text{ NOR } (\text{NOT } (\text{A NAND B}))
\end{align*}
$$

于是只用了 $3 \times 4 + 2 = 14$ 个晶体管。

![XOR](../assets/images/F/异或.gif)

### 同或门

显然 同或门 是上面的取反。

$$
\begin{align*}
\text{A XNOR B} &= \text{NOT} ( (\text{A NOR B}) \text{ NOR } (\text{NOT } (\text{A NAND B})) ) \\
               &= \text{NOT} ( \text{NOT} ( (\text{A NOR B}) \text{ OR } (\text{NOT } (\text{A NAND B})) ) ) \\
               &= \text{NOT} ( (\text{NOT } (\text{A NOR B})) \text{ AND } (\text{A NAND B}) ) \\
               &= (\text{NOT } (\text{A NOR B})) \text{ NAND } (\text{A NAND B})
\end{align*}
$$

![同或](../assets/images/F/同或.gif)


### 最少晶体管同或异或门

事实上，区分上下拉网络的话，用上面相同的思想，考虑信号的布尔式，而非 与非、或非门 的“布尔式”，再分解成串联、并联就行。

从真值表出发

|     | 同或 |
| --- | ---- |
| 00  | 1    |
| 01  | 0    |
| 10  | 0    |
| 11  | 1    |

也就是说

$$
A \text{ XNOR } B = ĀB̄ + AB
$$

!!!note
    $\cdot$ 串  
    $+$ 并

所以需要 2对 (NOT) + 2 x 2对 = 12 根。

!!!note
    真值表直接写出的表达式，很多时候不是最简的，进行化简的方法就是

    - 不用学的 “卡诺图化简”  
    - 现代的 QMC、espresso等  

但是显然，答案说可以 6 对，所以一定不能完全区分上下拉网络。

所以我显然想不到。

好处是 - 异或给了，反过来是同或。。。

先分析 XOR：

![6MOS XOR](../assets/images/F/6MOS-XOR.png)

可以看到，说是 00 输出 0，实际并没有接地，是悬空状态。

这种实现当然不好。模拟一下：

![6MOS XOR Simulation](../assets/images/F/6MOS-XOR-simulation.png)

只有 2.5 v。

事实上，2.5v 也很好了，实际应用控制线 3.3v，电源线12v，发动不了或者直接炸了。。。

直接电源/地，pMOS/nMOS 互换

![6MOS XNOR](../assets/images/F/6MOS-XNOR.png)

显然想不到，也不是好设计。模拟直接崩了。

## 进位计数法 Machine representation of integers


## 通过门电路搭建基本组合逻辑电路

### 译码器

译码器把 $k$ 位整数 变成 OHE。

!!!note
    什么神经？为啥这么干？明明 $k$ 条线就够了，为啥非要搞成 $2^k-1$ 条线？  
    事实上还挺有用，intuitive 的想法是，地址转换器。我想在地址 0x0001 取一个数，那肯定只有该地址的控制线应该被激活。

怎么实现呢？想想海明码？

![24译码器](../assets/images/F/24译码器.gif)

然而这个并不合适，用这个作为 38 DMX 会发下一个问题：

![错误的 38译码器](../assets/images/F/38译码器_WRONG.png)

每个译码器都必定会有一个输出。这显然不好。（谁的内存只有一个颗粒呢？）  

然而很沮丧的是，我居然要为了每一个输出加一个 AND 门。好消息是，之后我不需要门电路来辅助构建新的DMX了。

!!!note
    记得计算机体系吗？片选确实需要线，不需要新的门

![24DMX](../assets/images/F/24DMX.png)

![38DMX](../assets/images/F/38DMX.png)


### Problem of Subcircuit Shape
!!!failure
    ![subcircuit 形状不能保存](../assets/images/F/错误-subcircuit形状不能保存.gif)
