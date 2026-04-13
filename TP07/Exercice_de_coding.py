def merge(nums1, m, nums2, n):
    i = m - 1      # fin des éléments utiles de nums1
    j = n - 1      # fin de nums2
    k = m + n - 1  # fin de nums1 total

    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1

    
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1
