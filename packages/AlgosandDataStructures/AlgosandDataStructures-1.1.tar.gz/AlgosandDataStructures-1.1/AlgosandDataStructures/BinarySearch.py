
def Binarysearch(arr,value):
    ini = 0
    end = len(arr) - 1
    while ini<=end:
        middle = ini + ((end - ini) / 2)
        middle = int(middle)
        if arr[middle] == value:
            return middle

        if arr[middle] > value:
            end = middle - 1
        else: ini = middle + 1
    return -1


