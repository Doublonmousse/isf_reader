from typing import List
from copy import copy

def delta_delta(list_el:List[float]):
    # modifies the list in place

    current_delta = 0
    previous_delta = 0

    for k in range(len(list_el)):

        current_item = copy(list_el[k]) # just to be safe

        list_el[k] = list_el[k] + previous_delta - (current_delta * 2)

        previous_delta = current_delta
        current_delta = current_item

def inverse_delta_delta(list_el:List[float]):
    current_delta = 0
    previous_delta = 0
    
    for k in range(len(list_el)):
        delta = (current_delta * 2) - previous_delta + list_el[k]

        previous_delta = current_delta
        current_delta = delta
        
        list_el[k] = delta


#in_out_list = [k for k in range(100)]

#delta_delta(in_out_list)
#print(in_out_list)
#inverse_delta_delta(in_out_list)
#print(in_out_list)