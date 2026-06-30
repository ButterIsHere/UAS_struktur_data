# ==============================================================================
# MODULE: SORTING ALGORITHMS
# Mengimplementasikan rumpun O(n^2) dasar dan O(n log n) Divide & Conquer.
# ==============================================================================

def bubble_sort(arr, key='id'):
    """O(n^2) Family - Cocok untuk dataset skala kecil."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][key] > arr[j+1][key]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quick_sort(arr, key='id'):
    """O(n log n) Family - Divide and conquer efisiensi skala besar."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2][key]
    left = [x for x in arr if x[key] < pivot]
    middle = [x for x in arr if x[key] == pivot]
    right = [x for x in arr if x[key] > pivot]
    return quick_sort(left, key) + middle + quick_sort(right, key)
