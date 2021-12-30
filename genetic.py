# 遗传算法
import random
import copy

# 定义全局变量
cross_rate = 0.7        # 交叉率
mutation_rate = 0.001   # 变异率
max_generations = 400   # 最大进化次数


# 个体类
class CHROMOSOME:
    def __init__(self, length, case, bits=""):
        self.bits = ''
        self.fitness = 0
        
        if len(bits) == 0:
            self.gen_random_bits(length)
        else:
            self.bits = bits

        self.cal_fitness(case)

    def get_bits(self): 
        return self.bits
    def get_fitness(self):
        return self.fitness
    
    # 随机生成个体
    def gen_random_bits(self, length):
        for i in range(0, length):
            if random.random() > 0.5:
                self.bits += "1"
            else:
                self.bits += "0"

    # 计算当前个体的适应度
    def cal_fitness(self, case):
        # 根据当前的个体上色
        case.color_all_groups(self.bits)
        # 获取当前的上色结果的评分作为适应度
        self.fitness = case.cal_score()

# 种群类
class GENOME:

    def __init__(self, chromosomes, case, chromosome_length, genome_length):
        self.chromosomes = chromosomes
        self.case = case
        self.chromosome_length = chromosome_length  
        self.genome_length = genome_length         # 种群大小
        self.total_fitness = 0

    # 变异
    def mutate(self, chromosome_bits):
        global mutation_rate
        for index, bit  in enumerate(chromosome_bits):
            if random.random() < mutation_rate:
                if bit == '0':
                    chromosome_bits[index] = '1'
                else:
                    chromosome_bits[index] = '0'

    # 交叉
    def crossover(self, chromosome_bits_1, chromosome_bits_2):
        global cross_rate
        if random.random() < cross_rate:
            # 随机产生交叉点
            crossover_point = random.randint(0, self.chromosome_length-1)
            t1 = chromosome_bits_1[0:crossover_point] + chromosome_bits_2[crossover_point:]
            t2 = chromosome_bits_2[0:crossover_point] + chromosome_bits_1[crossover_point:]
            # 深度拷贝
            chromosome_bits_1 = copy.deepcopy(t1)
            chromosome_bits_2 = copy.deepcopy(t2)
    
    # 筛选个体（轮盘法，roulette wheel selection）
    def roulette_wheel_selecte(self):
        pass


