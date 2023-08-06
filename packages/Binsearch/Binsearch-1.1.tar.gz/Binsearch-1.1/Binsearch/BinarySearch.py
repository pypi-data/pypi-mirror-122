def BinarySearchList(arr, l, r, x):

    if r >= l:

        mid = l + (r - l) // 2

        if arr[mid] == x:
            return mid

        elif arr[mid] > x:
            result = BinarySearchList(arr, l, mid - 1, x)
            if result != -1:
                return result
            else:
                print("No element in array")

        else:
            result = BinarySearchList(arr, mid + 1, r, x)
            if result != -1:
                return result
            else:
                print("No element in array")

    else:

        return -1


def binaryLogic(arr, x):

    l = 0
    r = len(arr)

    while l <= r:

        m = l + ((r - l) // 2)

        res = (x == arr[m])


        if res == 0:
            return m - 1


        if res > 0:
            l = m + 1


        else:
            r = m - 1

    return -1


def BinarySearchString(arr, x):
    result = binaryLogic(arr, x)

    if result == -1:
        return "String not in array"
    else:
        return result
