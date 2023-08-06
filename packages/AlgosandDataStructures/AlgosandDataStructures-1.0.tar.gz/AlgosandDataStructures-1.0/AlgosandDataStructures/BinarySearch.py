
def Binarysearch(arr,value):

    def binarysearch2(arr,value,ini,end):

        while ini<=end:
            middle = ini + ((end - ini) / 2)
            middle = int(middle)
            if arr[middle] == value:
                return middle

            if arr[middle] > value:
                end = middle - 1
            else: ini = middle + 1
        return -1

    return binarysearch2(arr,value,0,len(arr) - 1)


