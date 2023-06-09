# PecMan_WeirdEdition
We made a weird PacMan game based on MicroBit.

我们基于MicroBit制作了一个（有些奇怪的）（制作者不能通关的）吃豆人小游戏！
你可以通过将程序上传到一块MicroBit板上来进行游戏。

视频演示：https://www.bilibili.com/video/BV1qz4y1v7Mq

![Poster](Poster.png)
游戏规则：<br/>

在一个神秘的迷宫中，住着一群拥有特殊能力的小生物，他们的身体由黄色的圆形和三条黑线组成，就像豆子一样。他们被称为“吃豆人”，因为他们的主要任务就是寻找和吃掉所有的豆子。<br/>
吃豆人生活在一个充满危险的世界里，他们需要不断地躲避各种障碍和敌人的袭击，才能顺利地完成任务。但是，他们拥有非凡的速度和机智，可以通过不同的技巧和战术来应对各种挑战。每当他吃掉一个豆子，就会增加一点能量和力量，让他更加强大。<br/>
1.程序初始化完成后，按下按钮A可以开始游戏，触摸金属Logo可以更改游戏难度，游戏难度从低到高为1-5，默认为1，直接按下A开始游戏的难度为1；<br/>
2.通过改变**单片机倾斜角度**，控制“吃豆人”的位置；<br/>
3.游戏过程中若按下按钮B，游戏强制终止；<br/>
4.每**吃掉一个“目标点”**，也即“吃豆人”与“目标点”位置重合，得分将+1；<br/>
5.初始时，单片机上将显示**3个“目标点”**，**每吃掉2个“目标点”后**，单片机显示面板上将再次生成2个“目标点”，使显示面板上“目标点”总数再次变为3个；<br/>
6.**得分达到8分后**，显示面板上将出现“Killer（地雷）”，且“Killer”数量随得分增加而增加；<br/>
7.每间隔一定时间，**“Killer”位置将改变，游戏难度越高，Killer移动速度越快**；<br/>
8.若踩到“地雷”，也即“吃豆人”与“地雷”位置重合，则游戏结束，“U r dead”，单片机显示面板将显示玩家得分。若想再次游戏，按下按钮A。<br/>
9.若得分超过30，则游戏成功，“U win”，单片机面板将显示玩家得分。若想再次游戏，按下按钮A。<br/>
10.由于单片机显示面板只能显示红色，我们用亮度区分“吃豆人”，“目标点”和“地雷”。**其中“吃豆人”最亮，“目标点”次亮，“地雷”最暗**。<br/>
