from shape import COLOR_BALANCING_CASE
from genetic import *

# 种群大小
chromosome_num = 50
# 最大进化次数
max_generations_num = 20
max_get_result_num = 10

if __name__ == "__main__":

    print("\n数据准备............\n")

    input_file = "d:\VLSI物理设计\project_3\color-patterning-with-GA\input\iccad2015_input.case1"

    name = input_file.split('\\')[-1].replace('input', 'output')

    print(name)

    case = COLOR_BALANCING_CASE(input_file, is_show_case=False, is_show_visualization=True)

    
    print("\n遗传算法............\n")

    # 种群个体的大小
    chromosome_length = case.colorbale_groups_num

    #生成初始种群个体
    chromosomes = []
    for i in range(0, chromosome_num):
        chromosomes.append(CHROMOSOME(case, length=chromosome_length))

    # 初始化种群
    gemo = GENOME(chromosomes=chromosomes, case=case, chromosome_length=chromosome_length, chromosome_num=chromosome_num)
    
    # 初始化最佳结果
    bset_result = gemo.get_best_chromosome()

    for i in range(0, max_get_result_num):
        
        # 进行一次迭代
        for j in range(0, max_generations_num):
            gemo.gen_new_chromosome()
        
        # 获取一次迭代后的最佳结果
        bset_result_temp = gemo.get_best_chromosome()

        # 保存最佳结果
        if bset_result_temp.get_fitness() > bset_result.get_fitness():
            bset_result = copy.deepcopy(bset_result_temp)

    print('最佳结果 \n上色模式: %s  \n适应度: %f' % (bset_result.get_bits(), bset_result.get_fitness()))


    print("\n结果输出............\n")

    case.color_all_groups(bset_result.get_bits())
    print('最终得分: %f' % case.cal_score())






    

    
    
    



    