from shape import COLOR_BALANCING_CASE
from genetic import *
import time

# 种群大小
chromosome_num = 100
# 最大进化次数
max_generations_num = 25
max_get_result_num = 15

if __name__ == "__main__":

    print("\n数据准备............\n")

    input_file = "d:\VLSI物理设计\project_3\input\iccad2015_input.case3"

    name = input_file.split('\\')[-1].replace('input', 'output')

    case = COLOR_BALANCING_CASE(input_file, is_show_case=True, is_show_visualization=True)

    
    print("\n遗传算法............\n")

    T1 = time.time()

    # 种群个体的大小
    chromosome_length = case.colorbale_groups_num

    #生成初始种群个体
    chromosomes = []
    for i in range(0, chromosome_num):
        chromosomes.append(CHROMOSOME(case, length=chromosome_length))

    # 初始化种群
    gemo = GENOME(chromosomes=chromosomes, case=case, chromosome_length=chromosome_length, chromosome_num=chromosome_num)
    
    # 初始化最佳结果
    best_result = gemo.get_best_chromosome()

    for i in range(0, max_get_result_num):
        
        # 进行一次迭代
        for j in range(0, max_generations_num):
            gemo.gen_new_chromosome()
        
        # 获取一次迭代后的最佳结果
        best_result_temp = gemo.get_best_chromosome()

        # 保存最佳结果
        if best_result_temp.get_fitness() > best_result.get_fitness():
            best_result = best_result_temp

    T2 = time.time()

    print('最佳结果 \n上色模式: %s  \n适应度: %f' % (best_result.get_bits(), best_result.get_fitness()))


    print("\n结果输出............\n")

    case.color_all_groups(best_result.get_bits())

    print('最终得分: %f' % case.cal_score())
    print('耗时: %f ms' % ((T2 - T1)*1000))
    
    case.write_file(name)
    case.show_result()

    print("\n完成................\n")







    

    
    
    



    