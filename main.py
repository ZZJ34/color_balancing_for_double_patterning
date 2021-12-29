from shape import COLOR_BALANCING_CASE



if __name__ == "__main__":

    input_file = "d:\VLSI物理设计\project_3\color-patterning-with-GA\input\iccad2015_input.case1"

    case = COLOR_BALANCING_CASE(input_file, is_show_case=True, is_show_visualization=True)

    print(case.colorbale_groups_num)

    
    
    



    