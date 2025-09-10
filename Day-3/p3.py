def second_largest(lst):
    if len(lst) < 2:
        return None
    first = second = lst[0]
    for num in lst:
        if num > first:
            second = first
            first = num
        elif num > second and num != first:
            second = num
    if first == second:  
        return None
    return second
numbers = [1, 5, 8, 2, 8, 3]
print("Second largest:", second_largest(numbers))