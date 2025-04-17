def Count_Inversion(arr : list):
    if(len(arr) <= 1):
        return arr, 0
    
    start = 0
    end = len(arr)
    mid = (start + end) // 2
    arr1, inv1 = Count_Inversion(arr[start:mid])
    arr2, inv2 = Count_Inversion(arr[mid:end])
    i, j, merge_inv = 0, 0, 0
    curr_arr = []
    while (i < len(arr1) and j < len(arr2)):
        if(arr1[i] <= arr2[j]):
            curr_arr.append(arr1[i])
            i += 1
        else:
            merge_inv += len(arr1) - i
            curr_arr.append(arr2[j])
            j += 1
    
    #copy remaining array
    if(i == len(arr1)):
        while j < len(arr2):
            curr_arr.append(arr2[j])
            j += 1
    else:
        while i < len(arr1):
            curr_arr.append(arr1[i])
            i += 1


    return curr_arr, (inv1 + inv2 + merge_inv)
    
