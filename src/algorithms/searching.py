# ==============================================================================
# MODULE: SEARCHING ALGORITHMS
# Implementasi Linear Search O(n) dan Binary Search O(log n).
# ==============================================================================

def linear_search(data_list, query, key='title'):
    """Pemindaian sekuensial O(n) untuk pencarian teks umum."""
    results = []
    for item in data_list:
        if query.lower() in str(item[key]).lower():
            results.append(item)
    return results

def binary_search(sorted_list, target_id, key='id'):
    """Pencarian logaritmik O(log n) berkinerja tinggi untuk ID terindeks."""
    low = 0
    high = len(sorted_list) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid][key] == target_id:
            return sorted_list[mid]
        elif sorted_list[mid][key] < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return None
