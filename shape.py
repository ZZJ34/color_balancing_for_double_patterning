from enum import Enum
from queue import Queue
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 定义全局变量
x_spacing = 0
y_spacing = 0
dens_win_size = 0

# 定义颜色填充枚举值
class COLOR(Enum):
    UNCOLORABLE = -1   # 不可填充
    NOCOLOR = 0        # 无颜色填充
    CA = 1             # 颜色填充 CA
    CB = 2             # 颜色填充 CB


# 定义坐标类
class COOR:

    def __init__(self, **kargs):
        # 两种初始化方式
        if 'x' in kargs.keys() and 'y' in kargs.keys():
            # 直接设置坐标点
            self.x = float(kargs['x'])
            self.y = float(kargs['y'])
        elif 'COOR' in kargs.keys():
            # 传入 COOR 类对象
            self.x = kargs['COOR'].x
            self.y = kargs['COOR'].y
        else:
            print('COOR 类初始化参数不足')

# 定义窗口类
class COLOR_DENSITY_WINDOWS:

    def __init__(self, length, left_bottom_coor):
        self.length = length                      # 窗口大小
        self.left_bottom_coor = COOR(x=left_bottom_coor.x, y=left_bottom_coor.y)  # 窗口左下角坐标
        self.shapes = []                          # 所包含的图案
        self.density_A = 0                        # 颜色 A 密度
        self.density_B = 0                        # 颜色 B 密度

    # 计算 shape 和此 windows 的重合面积
    def overlap_area(self, shape_item):

        [shape_left, shape_bottom] = [shape_item.left(), shape_item.bottom()]
        [window_left, window_bottom] = [self.left_bottom_coor.x, self.left_bottom_coor.y]

        overlay_left = max(shape_left, window_left)
        overlay_bottom = max(shape_bottom, window_bottom)

        [shape_right, shape_top] = [shape_item.right(), shape_item.top()]
        [window_right, window_top] = [self.left_bottom_coor.x+self.length, self.left_bottom_coor.y+self.length]

        overlay_right = min(shape_right, window_right)
        overlay_top = min(shape_top, window_top)

        overlay_area = (overlay_right-overlay_left) * (overlay_top-overlay_bottom)

        if overlay_area <= 0:
            print("数据错误 该 SHAPE 不在此 WINDOWS 当中")
        else:
            return overlay_area
    
    # 计算颜色密度
    def cal_density(self):
        area_A = 0  # color = 0
        area_B = 0  # color = 1

        for i in range(0, len(self.shapes)):
            if self.shapes[i].color == COLOR.CA:
                area_A += self.overlap_area(self.shapes[i])
            elif self.shapes[i].color == COLOR.CB:
                area_B += self.overlap_area(self.shapes[i])

        self.density_A = float( area_A / ( self.length * self.length ))
        self.density_B = float( area_B / ( self.length * self.length ))

# 定义形状类
class SHAPE:

    def __init__(self, **kargs):
        # 两种初始化的方式
        if 'left' in kargs.keys() and 'bottom' in kargs.keys() and 'right' in kargs.keys() and 'top' in kargs.keys():
            # 四个坐标值
            self.left_bottom_coor = COOR(x=kargs['left'], y=kargs['bottom'])
            self.right_top_coor = COOR(x=kargs['right'], y=kargs['top'])
        elif 'left_bottom_coor' in kargs.keys() and  'right_top_coor' in kargs.keys():
            # 两个坐标对
            self.left_bottom_coor = COOR(x=kargs['left_bottom_coor'].x, y=kargs['left_bottom_coor'].y)
            self.right_top_coor = COOR(x=kargs['right_top_coor'].x, y=kargs['right_top_coor'].y)
        else:
            print("SHAPE 类初始化参数不足")

        self.group_id = -1
        self.color = None
        self.neighbor = []
        self.window = None
        self.is_checked = False
    
    # 获取四个坐标值
    def top(self):
        return self.right_top_coor.y
    def right(self):
        return self.right_top_coor.x
    def bottom(self):
        return self.left_bottom_coor.y
    def left(self):
        return self.left_bottom_coor.x

    # 判断 self 相对 shape_item 的位置关系
    def is_above(self, shape_item):
        return self.bottom() > shape_item.top()
    def is_below(self, shape_item):
        return self.top() < shape_item.bottom()
    def is_left_to(self, shape_item):
        return self.right() < shape_item.left()
    def is_right_to(self, shape_item):
        return self.left() > shape_item.right()

    # 判断 self 与 shape_item 是否相邻
    def is_neighbor(self, shape_item):
        global x_spacing
        global y_spacing

        if (not self.is_above(shape_item)) and (not self.is_below(shape_item)):
            if self.is_right_to(shape_item):
                delta = self.left() - shape_item.right()
            elif self.is_left_to(shape_item):
                delta = shape_item.left() - self.right()
            else:
                return False

            if delta <= x_spacing:
                return True
            else:
                return False
        elif (not self.is_right_to(shape_item)) and (not self.is_left_to(shape_item)):
            if self.is_above(shape_item):
                delta = self.bottom() - shape_item.top()
            elif self.is_below(shape_item):
                delta = shape_item.bottom() - self.top()
            else:
                return False

            if delta <= y_spacing:
                return True
            else:
                return False
    # 记录相邻的 shape
    def set_neighbor(self, shape_item):
        self.neighbor.append(shape_item)
    
    # 打印 shape 信息
    def show_shape(self):
        print("%f, %f, %f, %f" % (self.left(), self.bottom(), self.right(), self.top()))
        print("color    : %s" % self.color.name)
        print("group_id : %s" % self.group_id)

# 定义形状组类
class SHAPE_GROUP:

    def __init__(self) :
        self.id = -1
        self.area_A = 0
        self.area_B = 0
        self.shapes = []
        self.is_colorable = False

    def color_shapes(self, initial_color):
        # 初始颜色可以是 CA 或者 CB
        if not self.is_colorable:
            print(" 当前 group %d 不可上色" % self.id)
        else:
            self.shapes[0].color = initial_color
            for shape_item in self.shapes:
                # 对当前 shape 的 neighbor 进行遍历
                for shape_item.neighbor_item in shape_item.neighbor:
                    if shape_item.neighbor_item.color == COLOR.NOCOLOR:
                        if shape_item.color == COLOR.CA:
                            shape_item.neighbor_item.color = COLOR.CB
                        elif shape_item.color == COLOR.CB:
                            shape_item.neighbor_item.color = COLOR.CA

# 定义测试案例类
class COLOR_BALANCING_CASE:

    def __init__(self, file_dir, is_show_case=False, is_show_visualization=False):
        self.shapes = []
        self.groups = []
        self.windows = []
        self.colorbale_groups_num = 0

        self.min_left = float("inf")
        self.max_right = float("-inf")
        self.min_bottom = float("inf")
        self.max_top = float("-inf")
        
        # 加载数据
        print("**************  加载数据  **************")
        self.load_data(self.read_file(file_dir))

        # 设置分组
        print("**************  设置分组  **************")
        self.set_groups()

        # 设置组是否可上色
        print("*********  检查分组是否可上色  *********")
        self.set_groups_is_colorable()

        # 设置边界
        print("**************  设置边界  **************")
        self.set_bounding()

        # 设置检查窗口
        print("**************  设置窗口  **************")
        self.set_windows()

        # 设置检查窗口
        print("*********  设置图形属于的窗口  *********")
        self.set_shapes_in_windows()

        if is_show_case:
            self.show_case()
        
        if is_show_visualization:
            self.show_visualization()

    # 读取文件
    def read_file(self, input_file_path):
        
        txt_lines = open(input_file_path).readlines()

        input_data = {}

        rect = []

        for index, txt_line in enumerate(txt_lines):
            if index == 0:
                input_data['ALPHA'] = float(txt_line.strip('\n').split('=')[-1])
            elif index == 1:
                input_data['BETA'] = float(txt_line.strip('\n').split('=')[-1])
            elif index == 2:
                input_data['OMEGA'] = float(txt_line.strip('\n').split('=')[-1])
            else:
                rect.append([float(item) for item in txt_line.strip('\n').split(',')])

        input_data['rect'] = rect

        return input_data

    #写入文件
    def write_file(self, output_file_path):
        
        f = open(output_file_path,'w')
        
        # 输出所有的 window 信息
        for index, window_item in enumerate(self.windows):
            win_left = window_item.left_bottom_coor.x
            win_bottom = window_item.left_bottom_coor.y
            win_right = win_left + window_item.length
            win_top = win_bottom + window_item.length

            f.write("WIN[%d]=" % (index+1))
            f.write("%d, %d, %d, %d" % (win_left, win_bottom, win_right, win_top))
            f.write("(%f, %f)" % (window_item.density_A, window_item.density_B))

            f.write("\n")
        
        for group_item in self.groups:
            f.write("GROUP\n")
            if group_item.is_colorable == True:
                CA_shapes = []
                CB_shapes = []

                for shape_item in group_item.shapes:
                    if shape_item.color == COLOR.CA:
                        CA_shapes.append(shape_item)
                    elif shape_item.color == COLOR.CB:
                        CB_shapes.append(shape_item)
                
                for index, shape_item in enumerate(CA_shapes):
                    f.write("CA[%d]=" % (index+1))
                    f.write("%d, %d, %d, %d" % (shape_item.left_bottom_coor.x, shape_item.left_bottom_coor.y, shape_item.right_top_coor.x, shape_item.right_top_coor.y))
                    f.write("\n")

                for index, shape_item in enumerate(CB_shapes):
                    f.write("CB[%d]=" % (index+1))
                    f.write("%d, %d, %d, %d" % (shape_item.left_bottom_coor.x, shape_item.left_bottom_coor.y, shape_item.right_top_coor.x, shape_item.right_top_coor.y))
                    f.write("\n")

            else:
                for index, shape_item in enumerate(group_item.shapes):
                    f.write("NO[%d]=" % (index+1))
                    f.write("%d, %d, %d, %d" % (shape_item.left_bottom_coor.x, shape_item.left_bottom_coor.y, shape_item.right_top_coor.x, shape_item.right_top_coor.y))
                    f.write("\n")


        f.close()

    # 数据加载
    def load_data(self, data):
        global x_spacing
        global y_spacing
        global dens_win_size

        x_spacing = data['ALPHA']
        y_spacing = data['BETA']
        dens_win_size = data['OMEGA']

        for shape_coor in data['rect']:
            shape_item = SHAPE(left=shape_coor[0], bottom=shape_coor[1], right=shape_coor[2], top=shape_coor[3])
            shape_item.color = COLOR.NOCOLOR
            self.shapes.append(shape_item)

    # 设置边界并可视化
    def set_bounding(self):

        for shape in self.shapes:
            # [x1,y1,x2,y2]坐标转换成[left,top,width,height]
            [x1, y1, x2, y2] = [shape.left(), shape.bottom(), shape.right(), shape.top()]              

            self.min_left = x1 if x1 < self.min_left else self.min_left
            self.min_bottom = y1 if y1 < self.min_bottom else self.min_bottom

            self.max_right = x2 if x2 > self.max_right else self.max_right
            self.max_top = y2 if y2 > self.max_top else self.max_top

    # 设置分组
    def set_groups(self): 
        group_id = 1
        # 通过 queue 实现
        visiting_shapes = Queue(maxsize=0)
        from_shapes = Queue(maxsize=0)

        for i in range(0, len(self.shapes)):
            if self.shapes[i].group_id == -1:
                # 注：如果当前的 shape 没有 group_id，则意味着其和其的相邻 shape 都没有 group_id
                # 此时应该新建一个组
                
                # 创建一个组
                group = SHAPE_GROUP()
                group.id = group_id
                self.groups.append(group)

                self.shapes[i].group_id = group_id

                visiting_shapes.put(self.shapes[i])
                from_shapes.put(None)
                
                # 将当前的 shape 加入到 新创建的 group
                group.shapes.append(self.shapes[i])

                # 遍历所有的 neighbor（包括 neighbor 的 neighbor ）
                while not visiting_shapes.empty():
                    current_shape = visiting_shapes.get()
                    from_shape = from_shapes.get()

                    # 遍历 shape ，找 current_shape 的邻居
                    for j in range(0, len(self.shapes)):

                        # 找到一个 neighbor
                        if current_shape.is_neighbor(self.shapes[j]):
                            current_shape.set_neighbor(self.shapes[j])

                            if (not self.shapes[j] == from_shape) and self.shapes[j].group_id == -1:
                                group.shapes.append(self.shapes[j])
                                self.shapes[j].group_id = group_id
                                visiting_shapes.put(self.shapes[j])
                                from_shapes.put(current_shape)
                
                group_id = group_id + 1

    # 设置 group 是否可上色
    def set_groups_is_colorable(self):

        # 遍历所有的 group
        for i in range(0, len(self.groups)):
            # 默认当前的 group 可以上色
            is_colorable = True

            visiting_shapes = Queue(maxsize=0)
            from_shapes = Queue(maxsize=0)

            # 获取当前 group 的一个 shape
            first_shape = self.groups[i].shapes[0]
            first_shape.is_checked = True

            # 遍历第一个 shape 的所有 neighbor
            for j in range(0, len(first_shape.neighbor)):
                first_shape.neighbor[0].is_checked = True
                visiting_shapes.put(first_shape.neighbor[0])
                from_shapes.put(first_shape)
            
            while not visiting_shapes.empty():

                current_shape = visiting_shapes.get()

                from_shape = from_shapes.get()

                for j in range(0, len(current_shape.neighbor)):
                    current_shape_neighbor = current_shape.neighbor[j]

                    if current_shape_neighbor.is_checked == False:
                        current_shape_neighbor.is_checked = True
                        visiting_shapes.put(current_shape_neighbor)
                        from_shapes.put(current_shape)
                    
                    # 此时 3 个 shape 彼此相连无法上色
                    if current_shape_neighbor.is_neighbor(from_shape):
                        is_colorable = False
                        # 中止  for j in range(0, len(current_shape.neighbor))  循环
                        break   

                if is_colorable == False:
                    # 中止  while not visiting_shapes.empty()  循环
                    break    

            # 根据 is_colorable 更新状态
            if is_colorable:
                # 该 group 可以上色
                self.groups[i].is_colorable = True
                self.colorbale_groups_num += 1
                for shape_item in  self.groups[i].shapes:
                    shape_item.is_checked = False
                    shape_item.color = COLOR.NOCOLOR
            else:
                # 该 group 可以不上色
                self.groups[i].is_colorable = False
                for shape_item in  self.groups[i].shapes:
                    shape_item.is_checked = False
                    shape_item.color = COLOR.UNCOLORABLE
    
    # 设置 windows
    def set_windows(self):
        global dens_win_size

        width = self.max_right - self.min_left
        height = self.max_top - self.min_bottom

        x_num = math.ceil(width/dens_win_size)
        y_num = math.ceil(height/dens_win_size)

        for i in range(1, x_num+1):
            if i < x_num:
                for j in range(1, y_num):
                    left_bottom_coor = COOR(x=self.min_left+(i-1)*dens_win_size, y=self.min_bottom+(j-1)*dens_win_size)
                    color_density_window = COLOR_DENSITY_WINDOWS(dens_win_size, left_bottom_coor)
                    self.windows.append(color_density_window)
                # 到达 bounding 上边界
                left_bottom_coor = COOR(x=self.min_left+(i-1)*dens_win_size, y=self.max_top-dens_win_size)
                color_density_window = COLOR_DENSITY_WINDOWS(dens_win_size, left_bottom_coor)
                self.windows.append(color_density_window)
            # 到达 bounding 右边界
            else:
                for j in range(1, y_num):
                    left_bottom_coor = COOR(x=self.max_right-dens_win_size, y=self.min_bottom+(j-1)*dens_win_size)
                    color_density_window = COLOR_DENSITY_WINDOWS(dens_win_size, left_bottom_coor)
                    self.windows.append(color_density_window)
                # 到达 bounding 上边界
                left_bottom_coor = COOR(x=self.max_right-dens_win_size, y=self.max_top-dens_win_size)
                color_density_window = COLOR_DENSITY_WINDOWS(dens_win_size, left_bottom_coor)
                self.windows.append(color_density_window)
    
    # 设置 windows 中的 shapes
    def set_shapes_in_windows(self):
        
        for shape_item in self.shapes:
            if not shape_item.color == COLOR.UNCOLORABLE:
                for windows_item in self.windows:
                    
                    if shape_item.top() <= windows_item.left_bottom_coor.y:
                        continue
                    if shape_item.bottom() >= windows_item.left_bottom_coor.y+windows_item.length:
                        continue
                    if shape_item.right() <= windows_item.left_bottom_coor.x:
                        continue
                    if shape_item.left() >= windows_item.left_bottom_coor.x+windows_item.length:
                        continue

                    windows_item.shapes.append(shape_item)

    # 打印信息
    def show_case(self):
        global x_spacing
        global y_spacing
        global dens_win_size

        print("x_spacing : %f" % x_spacing)
        print("y_spacing : %f" % y_spacing)
        print("dens_win_size : %f \n" % dens_win_size)

        for group_item in self.groups:
            print("GROUP %d" % group_item.id)
            print("is_colorable: %s" % ("true" if group_item.is_colorable else "false"))
            print("group_size: %d" % len(group_item.shapes))

            for shape_item in group_item.shapes:
                shape_item.show_shape()

            print("*****************************************")

    # 可视化
    def show_visualization(self):
        
        shape_coords = []
        windows_coords = []

        for rect in self.shapes:
            # [x1,y1,x2,y2]坐标转换成[left,top,width,height]
            [x1, y1, x2, y2] = [rect.left(), rect.bottom(), rect.right(), rect.top()]
            width  = x2 - x1       
            height = y2 - y1   
            left   = x1                 
            bottom = y1                   
            shape_coords.append([left, bottom, width, height])

        for rect in self.windows:
            width  = rect.length
            height = rect.length  
            left   = rect.left_bottom_coor.x                 
            bottom = rect.left_bottom_coor.y
            windows_coords.append([left, bottom, width, height])   

        # 展示所有的 shape
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        for index, coord in enumerate(shape_coords):
            [left, bottom, width, height] = coord

            rect = patches.Rectangle((left, bottom), width, height,  linewidth=0.2, edgecolor='r', facecolor='gray')
            ax1.add_patch(rect)

        plt.xlim(self.min_left-10, self.max_right+10)
        plt.ylim(self.min_bottom-10, self.max_top+10)
        plt.show()

        # 展示所有的 windows 和 shape
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        
        for index, coord in enumerate(shape_coords):
            [left, bottom, width, height] = coord

            rect = patches.Rectangle((left, bottom), width, height,  linewidth=0.2, edgecolor='r', facecolor='gray')
            ax1.add_patch(rect)

        for index, coord in enumerate(windows_coords):
            [left, bottom, width, height] = coord

            rect = patches.Rectangle((left, bottom), width, height,  linewidth=0.5, edgecolor='r', fill=False)
            ax1.add_patch(rect)

        plt.xlim(self.min_left-10, self.max_right+10)
        plt.ylim(self.min_bottom-10, self.max_top+10)
        plt.show()

    # 可视化最终结果
    def show_result(self):
        shape_coords = []
        windows_coords = []

        for rect in self.shapes:
            # [x1,y1,x2,y2]坐标转换成[left,top,width,height]
            [x1, y1, x2, y2] = [rect.left(), rect.bottom(), rect.right(), rect.top()]
            width  = x2 - x1       
            height = y2 - y1   
            left   = x1                 
            bottom = y1                   
            shape_coords.append([left, bottom, width, height, rect.color])

        for rect in self.windows:
            width  = rect.length
            height = rect.length  
            left   = rect.left_bottom_coor.x                 
            bottom = rect.left_bottom_coor.y
            windows_coords.append([left, bottom, width, height])   

        # 展示所有的 windows 和 shape
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        
        for index, coord in enumerate(shape_coords):
            [left, bottom, width, height, color] = coord

            if color == COLOR.UNCOLORABLE:
                rect = patches.Rectangle((left, bottom), width, height,  linewidth=0.2, edgecolor='r', facecolor='gray')
            elif color == COLOR.CA:
                rect = patches.Rectangle((left, bottom), width, height,  linewidth=0.2, edgecolor='g', facecolor='red')
            elif color == COLOR.CB:
                rect = patches.Rectangle((left, bottom), width, height,  linewidth=0.2, edgecolor='g', facecolor='blue')
            ax1.add_patch(rect)

        for index, coord in enumerate(windows_coords):
            [left, bottom, width, height] = coord

            rect = patches.Rectangle((left, bottom), width, height,  linewidth=0.5, edgecolor='r', fill=False)
            ax1.add_patch(rect)

        plt.xlim(self.min_left-10, self.max_right+10)
        plt.ylim(self.min_bottom-10, self.max_top+10)
        plt.show()

    # 给所有的组上色
    def color_all_groups(self, color_sequence):
        # 这里 color_sequence 的长度应该和可以上色的组的数量相同
        index = 0

        for group_item in self.groups:
            if group_item.is_colorable == True:
                # 上色前清空所有已上的色
                for shape_item in group_item.shapes:
                    shape_item.color = COLOR.NOCOLOR
                # 上色
                if color_sequence[index] == '0':
                    group_item.color_shapes(COLOR.CA)
                else:
                    group_item.color_shapes(COLOR.CB)
                index += 1

    # 计算 windows 颜色密度
    def cal_color_density(self):
        for window_item in self.windows:
            window_item.cal_density()

    # 计算评分
    def cal_score(self):
        self.cal_color_density()

        score = 0

        windows_num = len(self.windows)

        for window_item in self.windows:
            
            score += 1-float(abs(window_item.density_A-window_item.density_B))

        return score/windows_num
