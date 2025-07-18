import bisect

def binary_search_threshold(value_function, t, I_max, c_t):
    """
    Búsqueda binaria del punto de reordenamiento s_t.
    """
    low, high = 0, I_max
    while low < high:
        mid = (low + high) // 2
        if value_function[t][mid] - value_function[t][mid+1] > c_t:
            high = mid
        else:
            low = mid + 1
    return low
