


def Upperbound(arr,value):

    ini = 0
    end = len(arr) - 1

    while ini < end:
        middle = ini + (end - ini)/2
        middle = int(middle)

        if value >= arr[middle]:
            ini = middle + 1
        else: end = middle

        if ini < len(arr) and arr[ini] <= value:
            ini+=1
        if arr[ini] < value : return 'last'
        return ini
