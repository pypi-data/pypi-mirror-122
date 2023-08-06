


def Lowerbound(arr,value):
    ini = 0
    end = len(arr)
    while ini < end:
        middle = ini + (end - ini)/2
        middle = int(middle)
        if value <= arr[middle]:
            end = middle
        else: ini  = middle + 1

    if ini < len(arr) and arr[ini] < value:ini+=1
    return ini

