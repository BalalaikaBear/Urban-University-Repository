from copy import copy

# сортировка методом пузыря
def bubble_sort(ls):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(ls) - 1):
            if ls[i] > ls[i+1]:
                ls[i], ls[i+1] = ls[i+1], ls[i]
                swapped = True
    return ls

def selection_sort(ls):
    for i in range(len(ls)):
        lowest = i
        for j in range(i+1, len(ls)):
            if ls[j] < ls[lowest]:
                lowest = j
        ls[i], ls[lowest] = ls[lowest], ls[i]
    return ls

def insertion_sort(ls):
    for i in range(1, len(ls)):
        key = ls[i]
        j = i - 1
        while ls[j] > key and j >= 0:
            ls[j + 1] = ls[j]
            j -= 1
        ls[j + 1] = key
    return ls

if __name__ == "__main__":
    nums = [5, 6, 2, 1, 3, 4]
    print(nums)

    nums_1 = copy(nums)
    print("Bubble sort:", bubble_sort(nums_1))

    nums_2 = copy(nums)
    print("Selection sort:", selection_sort(nums_2))

    nums_3 = copy(nums)
    print("Insertion sort", insertion_sort(nums_3))