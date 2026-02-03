"""
================================================================================
PYTHON INTERVIEW PREPARATION - MASTER CODE LIST
================================================================================
INSTRUCTIONS:
1. Do not memorize. Understand the PATTERN.
2. Run these in your local VS Code to see how they work.
"""

import math
from collections import Counter, defaultdict, OrderedDict

# ==============================================================================
# SECTION 1: BASICS & NUMBERS (The Warm-up)
# ==============================================================================

# 1. Swap two variables (Pythonic Way)
def swap_vars(a, b):
    a, b = b, a
    return a, b

# 2. Check if a number is Prime
def is_prime(n):
    if n <= 1: return False
    # Only check up to square root of n (Optimization)
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# 3. Factorial (Recursive vs Iterative)
def factorial_recursive(n):
    return 1 if n == 0 else n * factorial_recursive(n-1)

# 4. Fibonacci Series (Generator - Saves Memory!)
def fib_generator(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a+b
# Usage: print(list(fib_generator(10)))

# 5. Reverse an Integer (Handle negatives)
def reverse_integer(n):
    sign = -1 if n < 0 else 1
    reversed_num = int(str(abs(n))[::-1])
    return sign * reversed_num

# ==============================================================================
# SECTION 2: STRING MANIPULATION (Very High Probability)
# ==============================================================================

# 6. Check Palindrome (Works for String or Number)
def is_palindrome(s):
    s = str(s)
    return s == s[::-1]

# 7. Reverse Words in a Sentence
# Input: "The Sky Is Blue" -> Output: "Blue Is Sky The"
def reverse_words(s):
    return " ".join(s.split()[::-1])

# 8. Valid Anagram (Using Counter)
# "listen" vs "silent"
def is_anagram(s1, s2):
    return Counter(s1) == Counter(s2)

# 9. First Non-Repeating Character
def first_unique_char(s):
    counts = Counter(s)
    for i, char in enumerate(s):
        if counts[char] == 1:
            return i  # Returns index
    return -1

# 10. Longest Substring Without Repeating Characters (SLIDING WINDOW PATTERN)
# *** CRITICAL FOR SENIOR ROLES ***
def length_of_longest_substring(s):
    char_map = {}
    left = 0
    max_len = 0
    for right in range(len(s)):
        if s[right] in char_map:
            # Move left pointer to right of the last seen duplicate
            left = max(left, char_map[s[right]] + 1)
        char_map[s[right]] = right
        max_len = max(max_len, right - left + 1)
    return max_len

# ==============================================================================
# SECTION 3: ARRAYS & LISTS
# ==============================================================================

# 11. Two Sum (HASHMAP PATTERN)
# Find two numbers that add up to target
def two_sum(nums, target):
    seen = {} # val -> index
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i

# 12. Find Duplicates in List
def contains_duplicate(nums):
    return len(nums) != len(set(nums))

# 13. Move Zeroes to End
# [0, 1, 0, 3, 12] -> [1, 3, 12, 0, 0]
def move_zeroes(nums):
    pos = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[pos], nums[i] = nums[i], nums[pos]
            pos += 1
    return nums

# 14. Best Time to Buy and Sell Stock
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    for p in prices:
        min_price = min(min_price, p)
        max_profit = max(max_profit, p - min_price)
    return max_profit

# 15. Intersection of Two Arrays
def intersection(nums1, nums2):
    return list(set(nums1) & set(nums2))

# ==============================================================================
# SECTION 4: SEARCHING & SORTING
# ==============================================================================

# 16. Binary Search (Iterative)
# Array MUST be sorted first
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# 17. Merge Sort (Divide & Conquer)
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Merge step
    sorted_arr = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])
    return sorted_arr

# 18. Quick Sort (Pythonic One-Linerish)
def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# ==============================================================================
# SECTION 5: ADVANCED DATA STRUCTURES (Stacks, Queues, Linked Lists)
# ==============================================================================

# 19. Valid Parentheses (STACK PATTERN)
# Input: "{[]}" -> True
def is_valid_parentheses(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
    return not stack

# 20. Reverse Linked List (Pointer Manipulation)
# Class Node: def __init__(self, val=0, next=None): ...
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next  # Save next node
        curr.next = prev # Reverse pointer
        prev = curr      # Move prev forward
        curr = nxt       # Move curr forward
    return prev

# 21. Detect Cycle in Linked List (Floyd’s Cycle Finding)
def has_cycle(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# ==============================================================================
# SECTION 6: SYSTEM DESIGN & SCENARIOS
# ==============================================================================

# 22. LRU Cache (Least Recently Used)
# Essential for System Design rounds
class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key) # Mark as recently used
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False) # Remove LRU item

# 23. Group Anagrams (Data Engineering/ETL common task)
# Input: ["eat", "tea", "tan", "ate", "nat", "bat"]
def group_anagrams(strs):
    anagram_map = defaultdict(list)
    for s in strs:
        # Sort string to use as key: "eat" -> "aet"
        sorted_s = "".join(sorted(s))
        anagram_map[sorted_s].append(s)
    return list(anagram_map.values())