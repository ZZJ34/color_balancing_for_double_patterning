import matplotlib.pyplot as plt
import matplotlib.patches as patches


def original_pic(rect_array):

    xlim_min, ylim_min, xlim_max, ylim_max = float("inf"), float("inf"), float ("-inf"), float ("-inf")
    
    coords = []

    for rect in rect_array:
        # [x1,y1,x2,y2]坐标转换成[left,top,width,height]
        [x1, y1, x2, y2] = rect
        width  = x2 - x1       
        height = y2 - y1   
        left   = x1                 
        bottom = y1                   

        coords.append([left, bottom, width, height])

        xlim_min = x1 if x1 < xlim_min else xlim_min
        ylim_min = y1 if y1 < ylim_min else ylim_min

        xlim_max = x2 if x2 > xlim_max else xlim_max
        ylim_max = y2 if y2 > ylim_max else ylim_max
    

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    
    # 绘制矩形
    for index, coord in enumerate(coords):
        [left, bottom, width, height] = coord

        rect = patches.Rectangle((left, bottom), width, height,  linewidth=0.1, edgecolor='r',facecolor='gray')
        ax1.add_patch(rect)
        

    plt.xlim(xlim_min-20, xlim_max+20)
    plt.ylim(ylim_min-20, ylim_max+20)


    plt.show()


def result_pic(rect_array):
    print(rect_array)
