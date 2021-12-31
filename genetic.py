# 遗传算法
import random
import copy

# 定义全局变量
cross_rate = 0.74        # 交叉率
mutation_rate = 0.002   # 变异率



# 个体类
class CHROMOSOME:
    def __init__(self, case, length=0, bits=""):
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

    def __init__(self, chromosomes, case, chromosome_length, chromosome_num):
        self.chromosomes = chromosomes
        self.case = case
        self.chromosome_length = chromosome_length  
        self.chromosome_num = chromosome_num         
        self.total_fitness = 0

    # 计算整体的适应度
    def cal_total_fitness(self):
        self.total_fitness = 0
        for chromosome in self.chromosomes:
            self.total_fitness += chromosome.get_fitness()

    # 变异
    def mutate(self, chromosome_bits):
        global mutation_rate
        chromosome_bits_temp = []
        for bit  in chromosome_bits:
            if random.random() < mutation_rate:
                if bit == '0':
                    chromosome_bits_temp.append('1')
                else:
                    chromosome_bits_temp.append('0')
            else:
                chromosome_bits_temp.append(bit)
        
        return ''.join(chromosome_bits_temp)

    # 交叉
    def crossover(self, chromosome_bits_1, chromosome_bits_2):
        global cross_rate
        if random.random() < cross_rate:
            # 随机产生交叉点
            crossover_point = random.randint(0, self.chromosome_length-1)
            t1 = chromosome_bits_1[0:crossover_point] + chromosome_bits_2[crossover_point:]
            t2 = chromosome_bits_2[0:crossover_point] + chromosome_bits_1[crossover_point:]
            
            return [t1, t2]

        return [chromosome_bits_1, chromosome_bits_2]

    # 筛选个体（轮盘法，roulette wheel selection）
    def roulette_wheel_selecte(self):
        slice = random.random() * self.total_fitness
        fitness_so_far = 0
        for chromosome in self.chromosomes:
            fitness_so_far += chromosome.get_fitness()
            if(fitness_so_far >= slice):
                return chromosome.get_bits()
    
    # 获取当前种群最佳的个体
    def get_best_chromosome(self):
        best_fitness = 0
        best_index = 0
        for index, chromosome in enumerate(self.chromosomes):
            if chromosome.get_fitness() > best_fitness:
                best_fitness = chromosome.get_fitness()
                best_index = index

        return self.chromosomes[best_index]

    # 生成新的种群
    def gen_new_chromosome(self):
        # 计算当前种群总的适应度
        self.cal_total_fitness()
        # 新的种群
        chromosomes_temp = []
        chromosomes_count = 0
        
        while chromosomes_count < self.chromosome_num:

            bits_1 = self.roulette_wheel_selecte()
            bits_2 = self.roulette_wheel_selecte()


            [bits_1, bits_2] = self.crossover(bits_1, bits_2)


            bits_1 = self.mutate(bits_1)
            bits_2 = self.mutate(bits_2)


            chromosomes_temp.append(CHROMOSOME(self.case, bits=bits_1))
            chromosomes_temp.append(CHROMOSOME(self.case, bits=bits_2))
            
            chromosomes_count += 2
        

        self.chromosomes = copy.deepcopy(chromosomes_temp)
