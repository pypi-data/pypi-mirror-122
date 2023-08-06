def binarySearchlist(arr, l, r, x):
    # Check base case
    if r >= l:

        mid = l + (r - l) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

        # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] > x:
            result = binarySearchlist(arr, l, mid - 1, x)
            if result != -1:
                return result
            else:
                print("No element in array")

        # Else the element can only be present
        # in right subarray
        else:
            result = binarySearchlist(arr, mid + 1, r, x)
            if result != -1:
                return result
            else:
                print("No element in array")

    else:
        # Element is not present in the array
        return -1