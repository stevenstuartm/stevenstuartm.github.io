---
title: "Practical Decision Guide"
category: Data Structures & Algorithms
description: "Practical guide for choosing the right data structure and algorithm for your problem, comparing interview practices with production best practices."
---

## Quick Data Structure Selection

| Need | First Choice | Alternative | Avoid |
|------|-------------|-------------|-------|
| **Fast lookups by key** | Hash Map (Dictionary<K,V>) | Sorted array + binary search | Linear search in array |
| **Fast insertion/removal at ends** | Dynamic Array (List<T>) | Deque | Linked list (unless memory critical) |
| **Maintain sorted order during insertions** | Balanced BST or SortedDictionary<K,V> | Sorted list + binary insertion | Unbalanced BST |
| **Priority-based processing** | Heap (PriorityQueue<T,P>) | Sorted list | Unsorted array |
| **Function call management** | Stack | Array with index | Queue |
| **Task queue/scheduling** | Queue | Array with indices | Stack |
| **Undo/Redo operations** | Stack of states | Array | Queue |
| **Cache with size limit** | LRU Cache (dict + doubly linked) | Hash map only | Array |

## Algorithm Selection Guide

| Problem Type | First Try | If That Fails | Never Use |
|--------------|-----------|---------------|-----------|
| **Sorting small data** (<50 items) | Language built-in | Insertion sort | Bubble sort |
| **Sorting large data** | Language built-in | Merge sort | Selection sort |
| **Searching unsorted** | Linear search (built-in) | Hash set conversion | Binary search |
| **Searching sorted** | Binary search | Built-in search | Linear search |
| **Shortest path (unweighted)** | BFS | Library pathfinding | DFS |
| **Shortest path (weighted)** | Dijkstra's | A* with heuristic | BFS on weighted |
| **Finding any path** | DFS | BFS | Complex pathfinding |
| **Tree traversal** | Built-in iterator | Recursive DFS/BFS | Manual stack |

## Modern Reality Check

### Always Use Built-ins For:
- **Sorting:** `Array.Sort()` and `List<T>.Sort()`
- **Basic searching:** `Contains()`, `IndexOf()`, `Find()`
- **Standard collections:** `List<T>`, `Dictionary<K,V>`, `HashSet<T>`
- **String operations:** `Split()`, `string.Join()`, `Replace()`, Regex class

### Implement Yourself For:
- **Interview questions** (they want to see you can think algorithmically)
- **Highly specialized performance needs** (after profiling proves bottleneck)
- **Learning/educational purposes**
- **Custom data structures** for specific domain logic

### Study But Rarely Implement:
- **Advanced tree balancing** (AVL, Red-Black trees)
- **Complex graph algorithms** beyond DFS/BFS/Dijkstra
- **String matching** beyond naive approach (use regex)
- **Advanced sorting algorithms** (languages have hybrid algorithms)

## Language-Specific Advice

### C#
**Use:** `List<T>` for arrays, `Dictionary<K,V>` for maps, `HashSet<T>` for sets, `Queue<T>`/`Stack<T>`
**Built-in sorting:** `Array.Sort()` and `List<T>.Sort()` use introsort (quicksort + heapsort hybrid)
**Searching:** `Contains()`, `IndexOf()`, `Array.BinarySearch()` for sorted data
**Avoid implementing:** LINQ often provides what you need (`.Where()`, `.OrderBy()`, etc.)
**Collections:** Use `List<T>` instead of arrays for dynamic sizing, `Dictionary<K,V>` for O(1) lookups
**Performance:** Built-in collections are highly optimized with excellent cache performance

## Performance Reality

### Hash Maps Win Most Cases
- **Average O(1)** lookup, insertion, deletion
- **Powers most algorithms** - counting, caching, lookup tables
- **Default choice** unless you need ordering or have memory constraints

### Arrays/Lists Are Your Workhorse
- **O(1) access** by index
- **Great cache performance** due to memory locality
- **Built-in operations** are highly optimized
- **Use instead of linked lists** 99% of the time

### Trees Are Specialized
- **Use only when** you need sorted iteration with dynamic insertions
- **Most databases** use B-trees internally, not binary search trees
- **For interviews:** Know BST operations, but use `SortedDictionary` in production

### Graphs Are Domain-Specific  
- **Learn DFS/BFS deeply** - they apply to many problems beyond graphs
- **Use libraries** for complex graph algorithms (QuikGraph, Microsoft.Msagl for C#)
- **Common in:** Social networks, maps, dependency management, game AI

## Interview vs Production Mindset

### In Interviews:
1. **Start with brute force** - get working solution first
2. **Optimize iteratively** - identify bottlenecks, improve step by step  
3. **Implement from scratch** - show algorithmic thinking
4. **State complexity** - always analyze time/space trade-offs
5. **Consider edge cases** - empty input, single element, duplicates

### In Production:
1. **Use well-tested libraries** - don't reinvent wheels
2. **Profile before optimizing** - measure actual bottlenecks
3. **Prioritize readability** - maintainable code beats clever code
4. **Consider total cost** - development time, maintenance, bug risk
5. **Plan for scale** - but don't over-engineer for problems you don't have

## Red Flags - When You're Probably Overthinking

- **Implementing your own hash table** (unless writing a database)
- **Writing custom sorting** (unless for embedded systems with constraints)
- **Building complex tree structures** (use language built-ins first)
- **Optimizing before measuring** (profile first, then optimize)
- **Choosing exotic algorithms** without clear performance requirements

## Green Lights - When Custom Implementation Makes Sense

- **Interview/educational context** (they want to see your thinking)
- **Profiled performance bottleneck** with clear improvement path
- **Domain-specific constraints** (memory, real-time, embedded systems)
- **Algorithm doesn't exist** in standard libraries for your use case
- **Learning exercise** to understand concepts deeply

## Bottom Line Philosophy

**Modern software development** is about choosing the right abstraction and using well-tested libraries. **Understanding algorithms deeply** makes you better at recognizing patterns and solving new problems, even when you use existing implementations.

**Focus your learning** on understanding when and why to use different approaches, rather than memorizing implementation details you can look up.