"""Phase 2a: parcel prioritisation.

Merge sort is the chosen algorithm: O(n log n) in the best, average AND worst case, and it is
stable. Insertion sort and quick sort are included only so Phase 4 can compare them.
"""


def parcel_key(p):
    # Most urgent first: earliest deadline, then highest priority, then id for determinism.
    return (p.deadline, -p.priority, p.id)


def merge_sort(items, key=lambda x: x):
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    left, right = merge_sort(items[:mid], key), merge_sort(items[mid:], key)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):   # <= keeps equal keys in original order (stable)
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


def insertion_sort(items, key=lambda x: x):
    a = list(items)
    for i in range(1, len(a)):
        cur, k, j = a[i], key(a[i]), i - 1
        while j >= 0 and key(a[j]) > k:
            a[j + 1] = a[j]; j -= 1
        a[j + 1] = cur
    return a


def quick_sort(items, key=lambda x: x):
    if len(items) <= 1:
        return list(items)
    pivot = key(items[len(items) // 2])
    return (quick_sort([x for x in items if key(x) < pivot], key)
            + [x for x in items if key(x) == pivot]
            + quick_sort([x for x in items if key(x) > pivot], key))
