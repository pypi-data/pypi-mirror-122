import numpy as np

def counting_sort(arr: [int]) -> [int]:
    max_val = max(arr)
    min_val = min(arr)
    counted = np.zeros(max_val - min_val + 1, dtype=int)
    for x in arr:
        counted[x - min_val] += 1
    ans = np.zeros(len(arr), dtype=int)
    ind = 0
    for i in range(len(counted)):
        for j in range(counted[i]):
            ans[ind] = min_val + i
            ind += 1
    return ans

def bubble_sort(arr: [int]) -> [int]:
    arr = np.array(arr)
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                tmp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = tmp
    return arr