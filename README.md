# color_balancing_for_double_patterning

保证距离约束的情况下（即相邻的图案颜色不同）尽可能上色均匀（即不同窗口内的不同颜色密度尽快能相同）

题目详细参考 ICCAD2015赛题 Color Balancing for Double Patterning 或者 Project-Color-Balancing.pdf

---

## 说明

使用遗传算法(GA)

仅作为兴趣探索，使用 python 尽可能详细展示整体的步骤流程

参考连接：https://github.com/kevinkevin556/color-patterning-with-GA

### Getting Started

直接运行 main.py
    
    python3 main.py

### 文件结构

* main.py    主函数
* shape.py   相关数据结构类定义
* genetic.py 遗传算法相关类定义

## 备注

* 相关参数没有细致调整 

  * `chromosome_num` 
  * `max_generations_num`
  * `max_get_result_num`
  * `cross_rate`
  * `mutation_rate`
  

* 遗传算法
  
  * 个体选择（轮盘法，roulette wheel selection；竞争法，tournament selection；等级轮盘法，Rank Based Wheel Selection）
  * 选择其他优化算法
