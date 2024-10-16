# 《德克萨斯送快递》游戏设计文档

作者：atoposyz, [Christine-wxx](https://github.com/Christine-wxx)

鸣谢：[GGM_2015](https://github.com/GGN-2015)（提供了人物形象素材）

## 1. 游戏介绍

- 名称：德克萨斯送快递

- 类型：动作类游戏

- 游戏背景：

  又是平常的一天，德克萨斯身为企鹅物流的员工，又要去派送快递了！
  但是今天的路上依旧不那么太平啊，就像是误入了什么游戏一样，一把把刀剑从前面飞来！作为一名尖兵，躲过这些自然是易如反掌，但是有时候也会遇到不明确的BUFF与DEBUFF,让人措手不及！
  请你和德克萨斯合作，将快递安全送到目的地吧！

- 游戏技术实现

  - 游戏使用 C# 语言编写，采用了 .Net Framework框架实现。

  - 游戏中的人物和发射物等游戏元素通过自定义类实现的。

  - 游戏中的音效和图像等资源通过引用外部文件实现的。

  - 游戏中使用了定时器和缓冲区等技术，实现了游戏元素的动态效果和画面流畅度。

  - 游戏中使用了多线程技术，实现了游戏画面和游戏逻辑的分离，提高了游戏的运行效率。

  - 游戏中使用了随机数生成器和碰撞检测等技术，实现了游戏元素的随机生成和交互效果。

  > **游戏中的背景以及发射物等通过从网上找素材（树木、草地、路、动物、房子等），由画图工具合成。**
  >
  > **游戏中的人物形象由郭冠男同学贡献。**

## 2. 游戏界面设计

### 2.1 主界面

可以点击主界面的按钮，进入不同的界面，以及退出游戏。

<img src="C:\Users\Atoposyz\AppData\Roaming\Typora\typora-user-images\image-20230606220718284.png" alt="image-20230606220718284" style="zoom:70%;" />

### 2.2 游戏界面（关卡模式界面、随机模式界面）

游戏主界面分为两部分：游戏区域和游戏控制区域。

游戏区域是游戏的主要操作区域，包括一个固定的游戏角色（德克萨斯<img src="Document\mod_003.png" alt="mod_003" style="zoom:15%;" />）和随机出现的障碍物（![sword](Document\sword.png)）以及一些BUFF（<img src="Document\BUFF.png" alt="BUFF" style="zoom:25%;" />)、DEBUFF（<img src="Document\DEBUFF.png" alt="DEBUFF" style="zoom:25%;" />)。

<img src="C:\Users\Atoposyz\Desktop\图片1.png" alt="图片1" style="zoom:50%;" />

游戏控制区域包括**`开始游戏`**按钮、**`重置`**、**`排行榜`**、得分计数器以及一些人物当前状态、BUFF、DEBUFF状态等。单击**`开始游戏`**按钮可以开始游戏，此时，该按钮变为**`暂停`**键（**`关卡模式`**不能暂停），再次单击该按钮，游戏暂停，该按钮变为**`开始`**键，**`重置`**按钮可以重新开始当前游戏，**`排行榜`**按钮可以打开排行榜，**`返回`**按钮可以返回主界面。

<img src="C:\Users\Atoposyz\Desktop\图片2.png" alt="图片2" style="zoom: 50%;" />

### 2.3 排行榜界面

展示所有玩家闯关模式的得分排行榜

<img src="Document\image-20230606160810337.png" style="zoom:67%;" />

## 3. 游戏玩法

### 3.1 概述

在闯关模式中，玩家通过控制人物的移动，在 $3$ 个赛道中切换，以躲避飞来的剑（![sword](Document\sword.png))，并坚持更多的时间，最终穿过出口(<img src="Document\goal.png" alt="goal" style="zoom:10%;" />) 获取游戏胜利。

<img src="C:\Users\Atoposyz\Desktop\图片3.png" alt="图片3" style="zoom:50%;" />

### 3.2 详细规则

游戏开始后，会生成一些剑（![sword](Document\sword.png))、BUFF（<img src="Document\BUFF.png" alt="BUFF" style="zoom:20%;" />)、DEBUFF（<img src="Document\DEBUFF.png" alt="DEBUFF" style="zoom:20%;" />)，玩家需要控制德克萨斯（<img src="Document\mod_003.png" alt="mod_003" style="zoom:15%;" />）在 $3$ 个赛道中切换来躲避剑（![sword](Document\sword.png))和DEBUFF（<img src="Document\DEBUFF.png" alt="DEBUFF" style="zoom:20%;" />)，获得一些BUFF（<img src="Document\BUFF.png" alt="BUFF" style="zoom:20%;" />)。

如果玩家被剑（![sword](Document\sword.png)）击中（一个护盾值可以抵消一次伤害)，游戏结束。

如果玩家成功穿过出口 (<img src="Document\goal.png" alt="goal" style="zoom:10%;" />) ，游戏胜利。

玩家可以通过吸收BUFF（<img src="Document\BUFF.png" alt="BUFF" style="zoom:20%;" />)来增强自己的能力，例如增加护盾值、获得无敌效果，获得冲刺效果（以无敌状态冲刺）、减慢障碍物到来的速度等。

### 3.3 操作说明

玩家通过键盘上的`w`、`s`键控制人物（德克萨斯<img src="Document\mod_003.png" alt="mod_003" style="zoom:15%;" />）的移动。

`w`键：人物移动到上面的赛道。

`s`键：人物移动到下面的赛道。

## 4. 游戏逻辑

游戏开始的时候，会弹出“输入用户名”的弹窗，若玩家输入了非空的用户名，则在闯关模式获胜后会记录到排行榜中。若不输入用户名，则获胜后不会有记录。

<img src="Document\image-20230606154911876.png" alt="image-20230606154911876" style="zoom:67%;" />

游戏初始时默认显示主界面，在主界面可以进入**`关卡模式`**或**`随机模式`**开始游戏，也可以单击**`帮助`**按钮获取帮助说明，或者单击**`退出`**按钮，退出游戏。

<img src="C:\Users\Atoposyz\AppData\Roaming\Typora\typora-user-images\image-20230606220718284.png" alt="image-20230606220718284" style="zoom:70%;" />

在**`关卡模式`**界面或**`随机模式`**界面，可以进行开始游戏、暂停游戏、重置、查看排行榜、返回主界面操作。

<img src="C:\Users\Atoposyz\Desktop\图片4.png" alt="图片4" style="zoom:50%;" />

## 5. 游戏元素定义

### 5.1 赛道

本游戏中，玩家控制的德克萨斯（<img src="Document\mod_003.png" alt="mod_003" style="zoom:15%;" />）和飞来的剑（![sword](Document\sword.png))，BUFF（<img src="Document\BUFF.png" alt="BUFF" style="zoom:20%;" />)、DEBUFF（<img src="Document\DEBUFF.png" alt="DEBUFF" style="zoom:20%;" />)等被限制在 3 行中，这 3 行就是赛道。

<img src="Document\image-20230606163143312.png" alt="image-20230606163143312" style="zoom:60%;" />

### 5.2 人物

即玩家控制的德克萨斯（<img src="Document\mod_003.png" alt="mod_003" style="zoom:15%;" />），通过`w`和`s`能够控制上下移动。

德克萨斯仅能上下移动，无法左右（横向，子弹飞来的方向）移动，但是可以通过触碰 BUFF（<img src="Document\BUFF.png" alt="BUFF" style="zoom:20%;" />)、DEBUFF（<img src="Document\DEBUFF.png" alt="DEBUFF" style="zoom:20%;" />), UNKNOWNEVENT（特殊道具<img src="Document\RandomEffect.png" alt="RandomEffect" style="zoom:20%;" />)改变自身在横向的位置：后部，中部，前部。3 个位置依次靠近子弹飞来的方向。

### 5.3 发射物

发射物是从屏幕右侧向左随机飞来的物体，拥有一定速度。

发射物碰到玩家控制的德克萨斯，或者到屏幕左侧，或者被特殊能力作用就会消失。

发射物包括：剑（![sword](Document\sword.png))，特殊道具（ BUFF<img src="Document\BUFF.png" alt="BUFF" style="zoom:20%;" />、DEBUFF<img src="Document\DEBUFF.png" alt="DEBUFF" style="zoom:20%;" />、UNKNOWNEVENT<img src="Document\RandomEffect.png" alt="RandomEffect" style="zoom:20%;" />)。

### 5.4 剑

剑（![sword](Document\sword.png))，或称障碍，在触碰到玩家控制的德克萨斯（<img src="Document\mod_003.png" alt="mod_003" style="zoom:15%;" />)后会对其造成一定伤害，护盾值减1或在护盾值为0时直接死亡。

### 5.5 特殊道具

特殊道具包括BUFF（<img src="Document\BUFF.png" alt="BUFF" style="zoom:20%;" />)和DEBUFF（<img src="Document\DEBUFF.png" alt="DEBUFF" style="zoom:20%;" />)，触碰到德克萨斯（<img src="Document\mod_003.png" alt="mod_003" style="zoom:15%;" />)后会造成特殊效果。

## 6. 特殊道具一览

### 6.1 BUFF

1. 护盾SHIELD。具有层数，可抵消一次子弹。
2. 磁铁MAGNET。具有持续时间，在持续时间内可以吸收经过的 3 条赛道的 BUFF, 金币, 红心 。
3. 回防DEFENSE。一次性效果，若方块后方有位置，则退到当前赛道的后一个位置，并无敌小段时间。
4. 缓时TIMESLACK。具有持续时间，持续时间内发射物速度变慢。
5. 无敌INVINCIBILITY。具有持续时间，持续时间内抵消所有子弹和特殊道具。
6. 净化PURE。一次性效果，清空所有已获得的特殊效果。
7. 冲刺SPRINT。具有持续时间，持续时间内获得磁铁和无敌并加速游戏时间。

### 6.2 DEBUFF

1. 勇猛BRAVE。一次性效果，若方块前方有位置，则前进到当前赛道的前一个位置，并无敌小段时间。
2. 无畏FEARLESS。具有持续时间，持续时间内子弹数量变多。
3. 强运GOODLUCK。一次性效果，立刻发射 3 个并排的未知效果。
4. 迅捷QUICK。具有持续时间，持续时间内发射物速度变快。
5. 夜行NIGHTWALK。具有持续时间，持续时间内游戏画面黑白闪烁。

### 6.3 未知效果

1. 所有BUFF
2. 所有DEBUFF

## 7. 具体实现

### 7.1 主界面

主界面包括一个背景图片、四个按钮。

在Form1_Load()函数中，初始时使用InputBox()函数弹出一个提示框，要求用户输入用户名。如果用户输入了用户名，函数将返回该用户名；否则返回空字符串。然后创建了一个Panel控件作为游戏主界面，设置了其大小和背景颜色。接着，创建了一个PictureBox控件作为背景图片，设置其大小、位置和显示模式，并将其添加到Panel控件中。然后，创建了四个Button控件，分别表示**`关卡模式`**、**`随机模式`**、**`帮助`**和**`退出`**功能，并设置其文本、位置、大小和字体等属性。将四个Button控件添加到背景图片控件中，再将背景图片控件添加到Panel控件中，最后将Panel控件添加到Form控件中。

单击**`关卡模式`**、**`随机模式`**按钮，会跳转到**`关卡模式`**、**`随机模式`**页面；单击**`帮助`**按钮，显示帮助文本；单击**`退出`**按钮关闭游戏。

### 7.2 游戏界面（关卡模式和随机模式）

游戏界面包括背景、人物、发射物、开始游戏按钮、重置按钮、排行榜按钮、返回按钮。

1.游戏元素
游戏中包含了多个元素，包括背景、人物、剑、BUFF、DEBUFF等，通过判断它们之间的交互实现游戏逻辑。其中，玩家通过键盘控制移动。游戏中还包含了一个Transmitter类，负责生成发射物等功能。

2.游戏逻辑
游戏逻辑主要包括碰撞检测、分数计算和排行榜更新等。在碰撞检测方面，通过判断发射物和玩家之间的碰撞，控制游戏的进行和结束。在分数计算方面，通过对玩家状态（如时间等）进行判断，并计算分数。在排行榜更新方面，通过调用Form2类的AddOrUpdateRankItem方法，将当前用户的得分和用户名更新到排行榜中。

3.UI设计
游戏的UI使用一个线程单独绘制，并使用双缓存。在游戏逻辑进行的同时，通过DrawGame方法将游戏界面的绘制缓存在buffer变量中，减少了不必要的重复绘制，提高了游戏的效率。

以下是涉及的主要类：

1. Player类继承自DrawableObject类，表示游戏中的人物元素。该类包含了人物的位置、状态、属性等信息。其中，Points数组表示了游戏地图中的三个位置点，玩家可以通过changepos方法来改变位置。reset方法用于重置人物属性，使其回到游戏起始状态。Draw方法用于将人物绘制在游戏界面上。
  
2. Bullet类同样继承自DrawableObject类，表示游戏中的发射物元素。该类包含了发射物的位置、伤害类型、移动等信息。Move方法用于控制发射物的移动，CollidesWith方法用于判断发射物是否与人物发生碰撞，LeaveScreen方法用于判断发射物是否已经超出游戏界面。Draw方法用于将发射物绘制在游戏界面上。
  
3. 一些BUFF类，如SHIELD、MAGNET、DEFENSE等。这些效果可以对角色造成一定的影响，如增强角色的能力、减弱角色的能力等。这些效果都是继承自基类Effect，并且实现了基类中的抽象方法CauseEffect，用于触发这些效果。同时，这些效果都有一个EffectType属性，用于指明效果的类型，包括OnceEffect、TimesEffect和ContinuousEffect。在这些类中，还有一些静态方法，如LoseEfficacy，用于在效果的持续时间结束后失效。

4. Final类，继承自BUFF，触发这个效果可以让玩家胜利。

5. Tool类，主要定义了一些静态变量和计时器。其中，静态变量包括了一些数组和常量，用于存储游戏中的一些位置、速度、时间等信息；计时器用于实现游戏中的一些效果，比如磁铁效果、时间减缓效果、无敌效果等。

   具体来说，这个类中的静态变量包括：

   - trackposY：一个包含三个整数的数组，表示游戏中三条轨道的纵坐标；
   - blockposX：一个包含三个整数的数组，表示游戏中三个人物所在位置的横坐标；
   - points：一个包含9个Point类型的二维数组，表示游戏中人物在每条轨道上的位置；
   - BULLETSPEED：一个常量，表示游戏中子弹的速度；
   - block：一个Player类型的静态变量，表示游戏中的人物德克萨斯；
   - form：一个Form1类型的静态变量，表示游戏中的主窗口；
   - transmitter：一个Transmitter类型的静态变量，表示游戏中的一个Transmitter类的对象；
   - score：一个整型静态变量，表示游戏中的得分。

   这个类中的计时器包括：

   - MainTimer：一个每500毫秒触发一次的计时器，用于计算游戏中的得分和一些效果的持续时间；
   - TransmitterTimer：一个每50毫秒触发一次的计时器；
   - MagnetTimer、TimeslackTimer、InvincibilityTimer、SprintTimer、FearlessTimer、QuickTimer、NightwalkTimer：每个计时器的作用分别为磁铁效果、时间减缓效果、无敌效果、冲刺效果、无惧效果、加速效果和夜行效果的持续时间计时。

   此外，这个类还包含了两个方法：

   - reset()：用于重置游戏中的所有计时器和静态变量；
   - MainTimerCount()：是MainTimer计时器的回调函数，用于更新游戏中的得分和各种效果的持续时间。

   通过这两个类的定义，可以在游戏中实现玩家和发射物的交互、移动、碰撞等逻辑。同时，这两个类也继承了DrawableObject类，可以通过Draw方法将它们绘制在游戏界面上，实现游戏元素的显示效果。


6.  Transmitter类，用于控制发射物的发射。以下是该类的主要特征和方法：

   - 私有字段 `interval`、`speed`、`startX`、`path`、`timecount`、`endtransmit`等，以及公共字段 `bullets` 和 `bullets2`等，分别表示发射的时间间隔、速度、发射的初始位置、发射序列的配置文件路径、时间计数器、是否结束发射等。
   - 公共构造函数 `Transmitter` 接受两个参数：赛道数量和发射的起始位置，以及一个可选参数 `interval`，表示发射间隔。在构造函数中，会初始化一些字段，并根据赛道的数量初始化赛道列表。
   - 公共方法 `LoadTrack` 和 `LoadRandomTrack` 用于加载发射物。`LoadTrack` 方法可以从指定的配置文件中读取发射物信息序列，`LoadRandomTrack` 方法则随机生成一个长度为 `timelength` 的发射物序列。
   - 公共方法 `Reset` 用于重置 Transmitter 的状态，将一些字段初始化为默认值。
   - 公共方法 `TransmitterCheck` 是一个事件处理方法，用于检查是否需要发射。在该方法中，会根据时间计数器和发射间隔计算当前是否需要发射，并根据配置发射相应的发射物。在特定的时间段，还会发射一些随机效果的发射物。在发射结束后，Transmitter 会在终点位置生成一个“终点线”表示已经全部发射完毕。
