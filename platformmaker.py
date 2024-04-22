import numpy as np

class platform:

    def calculate_platform_offset(previous_x:int, previous_y:int):

        offset_x = random_number = np.random.randint(-100, 100)
        offset_y = random_number = np.random.randint(40, 151)
        print(f'Offset x: {offset_x}, Offset y: {offset_y}')

        new_x = previous_x + offset_x
        new_y = previous_y + offset_y

        offset = [new_x, new_y]

        print(offset)

        return offset
    
    def create_platform_list(current_x:int, current_y:int, lenght:int):
        current_list = []
        for count in range(lenght):
            offset = platform.calculate_platform_offset(current_x, current_y)
            current_list.append(offset)
            current_x = offset[0]
            current_y = offset[1]

        return current_list