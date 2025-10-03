---
title: "Asymptotic Notation Study Guide"
category: Data Structures & Algorithms
---

## Table of Contents
- [Introduction](#introduction)
- [Mathematical Foundations](#mathematical-foundations)
  - [Logarithms](#logarithms)
  - [Polynomial vs Exponential Growth](#polynomial-vs-exponential-growth)
- [Types of Asymptotic Notation](#types-of-asymptotic-notation)
  - [Big O (O) - Upper Bound](#big-o-o---upper-bound)
  - [Big Omega (Ω) - Lower Bound](#big-omega-ω---lower-bound)
  - [Big Theta (Θ) - Tight Bound](#big-theta-θ---tight-bound)
- [Common Time Complexities](#common-time-complexities)
- [Detailed Examples](#detailed-examples)
  - [Constant Time - O(1)](#constant-time---o1)
  - [Logarithmic Time - O(log n)](#logarithmic-time---olog-n)
  - [Linear Time - O(n)](#linear-time---on)
  - [Linearithmic Time - O(n log n)](#linearithmic-time---on-log-n)
  - [Quadratic Time - O(n²)](#quadratic-time---on²)
  - [Exponential Time - O(2ⁿ)](#exponential-time---o2ⁿ)
  - [Factorial Time - O(n!)](#factorial-time---on)
- [Space Complexity](#space-complexity)
- [Practical Analysis Tips](#practical-analysis-tips)
- [Quick Reference](#quick-reference)

---

## Introduction

**Asymptotic notation** provides a mathematical framework for analyzing algorithm efficiency without being tied to specific hardware or implementation details. Instead of measuring exact execution time (which varies between computers), we analyze how an algorithm's resource requirements grow relative to input size (n).

**Key Benefits:**
- Hardware-independent performance analysis
- Enables algorithm comparison and selection
- Predicts scalability behavior
- Focuses on growth rate rather than exact values

**Primary Use Cases:**
- **Time Complexity:** How execution time grows with input size
- **Space Complexity:** How memory usage grows with input size

> **Note:** We typically focus on **worst-case scenarios** (Big O) because they provide safety guarantees for performance-critical applications.

---

## Mathematical Foundations

### Logarithms

A **logarithm** answers: *"How many times do I need to divide by 2 to get to 1?"*

**Simple Example:** 
- Start with 8 → divide by 2 → get 4
- Take 4 → divide by 2 → get 2  
- Take 2 → divide by 2 → get 1
- **Answer: 3 steps**, so log₂(8) = 3

**Think of it like this:**
```
1,000,000 items → 500,000 → 250,000 → 125,000 → ... → 1
This takes about 20 steps, so log₂(1,000,000) ≈ 20
```

**Key Properties for Algorithm Analysis:**
- **log₂(n):** Most common in computer science (binary operations)
- **Logarithms grow very slowly:** Even huge numbers need surprisingly few divisions
- **Common in divide-and-conquer algorithms:** Each step cuts problem in half

**Why this matters:** If you're searching through 1 million items by cutting the list in half each time, you only need ~20 comparisons instead of up to 1 million!

### Polynomial vs Exponential Growth

**Think of these like different ways numbers can grow:**

**Polynomial Growth:** n^k (multiply by itself k times)
- n¹ = n (just the number: 10, 100, 1000...)
- n² = n × n (10→100, 100→10,000, 1000→1,000,000)  
- n³ = n × n × n (10→1,000, 100→1,000,000)
- **Pattern:** Grows fast, but predictably

**Exponential Growth:** k^n (a number multiplied by itself n times)
- 2¹ = 2, 2² = 4, 2³ = 8, 2⁴ = 16, 2⁵ = 32...
- **Pattern:** Starts small, then **explodes**

**Visual comparison for n=10:**
- Linear O(n): 10 operations
- Quadratic O(n²): 100 operations  
- Exponential O(2ⁿ): 1,024 operations

**For n=20:**
- Linear: 20 operations
- Quadratic: 400 operations
- Exponential: 1,048,576 operations (over 1 million!)

---

## Types of Asymptotic Notation

### Big O (O) - Upper Bound
**Represents:** "At worst, it will take this long"

**Think of it like a speed limit:** A car *might* go 45 mph on a road with a 55 mph speed limit, but it will *never* go faster than 55 mph.

**Real example:** Linear search might find your item immediately (lucky!) or might have to check every single item (unlucky). Big O describes the unlucky scenario.

**Definition:** f(n) = O(g(n)) means your algorithm will never be slower than g(n) × some constant

**When to Use:** 
- Planning for worst-case scenarios ("What's the slowest this could be?")
- Most commonly used because it's safer to overestimate than underestimate

### Big Omega (Ω) - Lower Bound
**Represents:** "At best, it will take at least this long"

**Think of it like a minimum wage:** You might get paid more, but never less than the minimum.

**Definition:** f(n) = Ω(g(n)) means your algorithm will never be faster than g(n) × some constant

**When to Use:**
- Proving that certain problems are inherently difficult
- Showing theoretical limits ("No algorithm can do better than this")

### Big Theta (Θ) - Tight Bound
**Represents:** "It will always take roughly this long"

**Think of it like a thermostat:** The temperature stays within a tight range around the target.

**Simple rule:** If Big O and Big Omega are the same, then you have Big Theta.

**Definition:** f(n) = Θ(g(n)) means the algorithm is both O(g(n)) AND Ω(g(n))

**When to Use:**
- When performance is consistent regardless of input
- When you want to be precise about complexity

---

## Common Time Complexities

**Ordered from Best to Worst Performance:**

| Notation | Name | Growth Rate | Example Algorithms |
|----------|------|-------------|-------------------|
| O(1) | Constant | No growth | Array access, hash table lookup |
| O(log n) | Logarithmic | Very slow growth | Binary search, balanced tree operations |
| O(n) | Linear | Proportional growth | Linear search, single loop |
| O(n log n) | Linearithmic | Moderate growth | Merge sort, heap sort |
| O(n²) | Quadratic | Rapid growth | Bubble sort, nested loops |
| O(n³) | Cubic | Very rapid growth | Matrix multiplication (naive) |
| O(2ⁿ) | Exponential | Explosive growth | Recursive Fibonacci, subset generation |
| O(n!) | Factorial | Extremely explosive | Traveling salesman (brute force) |

**Scalability Comparison (think of it like cooking for different sized parties):**
- **n = 10 (small dinner party):** All methods work fine
- **n = 1,000 (wedding reception):** O(n²) starts to hurt, exponential becomes impossible  
- **n = 1,000,000 (city festival):** Only O(1), O(log n), O(n), O(n log n) are practical

**Real-world analogy:**
- **O(1):** Turning on a light switch (same effort regardless of room size)
- **O(log n):** Finding a word in a dictionary (flip to middle, eliminate half, repeat)
- **O(n):** Counting people in a line (must count each person once)
- **O(n²):** Shaking hands with everyone at a party (each person shakes hands with every other person)

---

## Detailed Examples

### Constant Time - O(1)
**Characteristic:** Performance independent of input size

```csharp
// Array access
public static T GetFirstElement<T>(T[] array)
{
    return array[0];  // Always one operation, regardless of array size
}

// Dictionary operations (average case)
public static TValue GetValue<TKey, TValue>(Dictionary<TKey, TValue> dictionary, TKey key)
{
    return dictionary[key];  // Direct access via hash
}

// Stack/Queue operations
public static void StackOperations()
{
    var stack = new Stack<int>();
    stack.Push(5);     // O(1) - always same time to add
    int value = stack.Pop();  // O(1) - always same time to remove
}

// Simple calculations
public static int AddNumbers(int a, int b)
{
    return a + b;  // Same time regardless of number size
}
```

### Logarithmic Time - O(log n)
**Characteristic:** Input size reduced by constant factor each step

```csharp
// Binary search - eliminates half the search space each iteration
public static int BinarySearch<T>(T[] sortedArray, T target) where T : IComparable<T>
{
    int left = 0;
    int right = sortedArray.Length - 1;
    
    while (left <= right)
    {
        int mid = left + (right - left) / 2;  // Avoid overflow
        int comparison = sortedArray[mid].CompareTo(target);
        
        if (comparison == 0)
        {
            return mid;  // Found target
        }
        else if (comparison < 0)
        {
            left = mid + 1;   // Eliminate left half
        }
        else
        {
            right = mid - 1;  // Eliminate right half
        }
    }
    return -1;  // Not found
}

// Binary search using built-in method
public static int BinarySearchBuiltIn<T>(T[] sortedArray, T target) where T : IComparable<T>
{
    return Array.BinarySearch(sortedArray, target);  // Also O(log n)
}

// Finding height of balanced binary tree
public class TreeNode<T>
{
    public T Value { get; set; }
    public TreeNode<T> Left { get; set; }
    public TreeNode<T> Right { get; set; }
}

public static int GetTreeHeight<T>(TreeNode<T> root)
{
    if (root == null) return 0;
    
    // Each level down, we eliminate half the remaining nodes to check
    return 1 + Math.Max(GetTreeHeight(root.Left), GetTreeHeight(root.Right));
}
```

### Linear Time - O(n)
**Characteristic:** Must examine each input element once

```csharp
// Linear search - might need to check every element
public static int LinearSearch<T>(T[] array, T target) where T : IEquatable<T>
{
    for (int i = 0; i < array.Length; i++)
    {
        if (array[i].Equals(target))
        {
            return i;
        }
    }
    return -1;
}

// Sum array elements - must process each element once
public static int Sum(int[] array)
{
    int total = 0;
    foreach (int num in array)
    {
        total += num;  // Process each element exactly once
    }
    return total;
}

// Using LINQ (also O(n) under the hood)
public static int SumLinq(int[] array)
{
    return array.Sum();  // Still processes each element once
}

// Find maximum value
public static T FindMax<T>(T[] array) where T : IComparable<T>
{
    if (array.Length == 0) throw new ArgumentException("Array cannot be empty");
    
    T max = array[0];
    for (int i = 1; i < array.Length; i++)  // Check each element once
    {
        if (array[i].CompareTo(max) > 0)
        {
            max = array[i];
        }
    }
    return max;
}

// Copy array - must touch each element
public static T[] CopyArray<T>(T[] source)
{
    T[] copy = new T[source.Length];
    for (int i = 0; i < source.Length; i++)
    {
        copy[i] = source[i];  // One operation per element
    }
    return copy;
}

// Count occurrences
public static int CountOccurrences<T>(T[] array, T target) where T : IEquatable<T>
{
    int count = 0;
    foreach (T item in array)  // Must check every element
    {
        if (item.Equals(target))
            count++;
    }
    return count;
}
```

### Linearithmic Time - O(n log n)
**Characteristic:** Efficient divide-and-conquer algorithms

```csharp
// Merge sort - divides problem in half, then merges linearly
public static void MergeSort(int[] array)
{
    if (array.Length <= 1) return;
    
    MergeSortHelper(array, 0, array.Length - 1);
}

private static void MergeSortHelper(int[] array, int left, int right)
{
    if (left < right)
    {
        int mid = left + (right - left) / 2;
        
        // Divide: O(log n) levels of recursion
        MergeSortHelper(array, left, mid);
        MergeSortHelper(array, mid + 1, right);
        
        // Conquer: O(n) merge operation at each level
        Merge(array, left, mid, right);
    }
}

private static void Merge(int[] array, int left, int mid, int right)
{
    int[] temp = new int[right - left + 1];
    int i = left, j = mid + 1, k = 0;
    
    // Merge the two sorted halves - O(n) operation
    while (i <= mid && j <= right)
    {
        if (array[i] <= array[j])
            temp[k++] = array[i++];
        else
            temp[k++] = array[j++];
    }
    
    while (i <= mid) temp[k++] = array[i++];
    while (j <= right) temp[k++] = array[j++];
    
    for (i = left, k = 0; i <= right; i++, k++)
        array[i] = temp[k];
}

// Using built-in sort (typically O(n log n))
public static void BuiltInSort(int[] array)
{
    Array.Sort(array);  // Introsort: hybrid quicksort/heapsort/insertion sort
}

// Heap sort - guaranteed O(n log n)
public static void HeapSort(int[] array)
{
    int n = array.Length;
    
    // Build heap: O(n)
    for (int i = n / 2 - 1; i >= 0; i--)
        Heapify(array, n, i);
    
    // Extract elements: O(n log n)
    for (int i = n - 1; i > 0; i--)
    {
        // Move current root to end
        (array[0], array[i]) = (array[i], array[0]);
        
        // Heapify reduced heap: O(log n)
        Heapify(array, i, 0);
    }
}

private static void Heapify(int[] array, int n, int i)
{
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    
    if (left < n && array[left] > array[largest])
        largest = left;
    
    if (right < n && array[right] > array[largest])
        largest = right;
    
    if (largest != i)
    {
        (array[i], array[largest]) = (array[largest], array[i]);
        Heapify(array, n, largest);
    }
}
```

### Quadratic Time - O(n²)
**Characteristic:** Nested iteration over input

```csharp
// Bubble sort - compares each pair of elements
public static void BubbleSort(int[] array)
{
    int n = array.Length;
    for (int i = 0; i < n; i++)          // Outer loop: n iterations
    {
        bool swapped = false;
        for (int j = 0; j < n - 1 - i; j++)  // Inner loop: up to n iterations
        {
            if (array[j] > array[j + 1])
            {
                // Swap elements
                (array[j], array[j + 1]) = (array[j + 1], array[j]);
                swapped = true;
            }
        }
        if (!swapped) break;  // Optimization: stop if no swaps made
    }
}

// Selection sort - find minimum and place it at the beginning
public static void SelectionSort(int[] array)
{
    for (int i = 0; i < array.Length - 1; i++)
    {
        int minIndex = i;
        for (int j = i + 1; j < array.Length; j++)  // Check remaining elements
        {
            if (array[j] < array[minIndex])
                minIndex = j;
        }
        // Swap minimum with current position
        (array[i], array[minIndex]) = (array[minIndex], array[i]);
    }
}

// Find all duplicate pairs
public static List<(T, int, int)> FindDuplicatePairs<T>(T[] array) where T : IEquatable<T>
{
    var duplicates = new List<(T, int, int)>();
    
    for (int i = 0; i < array.Length; i++)       // Check each element
    {
        for (int j = i + 1; j < array.Length; j++) // Against every other element
        {
            if (array[i].Equals(array[j]))
            {
                duplicates.Add((array[i], i, j));
            }
        }
    }
    return duplicates;
}

// Matrix multiplication (naive approach)
public static int[,] MultiplyMatrices(int[,] matrix1, int[,] matrix2)
{
    int rows1 = matrix1.GetLength(0);
    int cols1 = matrix1.GetLength(1);
    int cols2 = matrix2.GetLength(1);
    
    int[,] result = new int[rows1, cols2];
    
    for (int i = 0; i < rows1; i++)          // For each row in result
    {
        for (int j = 0; j < cols2; j++)      // For each column in result
        {
            for (int k = 0; k < cols1; k++)  // For each element in dot product
            {
                result[i, j] += matrix1[i, k] * matrix2[k, j];
            }
        }
    }
    return result;
}

// Check if array contains duplicates (naive approach)
public static bool HasDuplicates<T>(T[] array) where T : IEquatable<T>
{
    for (int i = 0; i < array.Length; i++)
    {
        for (int j = i + 1; j < array.Length; j++)
        {
            if (array[i].Equals(array[j]))
                return true;
        }
    }
    return false;
}

// Better approach using HashSet - O(n)
public static bool HasDuplicatesEfficient<T>(T[] array)
{
    var seen = new HashSet<T>();
    foreach (T item in array)
    {
        if (!seen.Add(item))  // Add returns false if item already exists
            return true;
    }
    return false;
}
```

### Exponential Time - O(2ⁿ)
**Characteristic:** Each recursive call spawns multiple sub-problems

```csharp
// Naive recursive Fibonacci - recalculates same values repeatedly
public static long FibonacciNaive(int n)
{
    if (n <= 1) return n;
    
    // Each call creates two more calls - exponential growth
    return FibonacciNaive(n - 1) + FibonacciNaive(n - 2);
}

// Better approach using memoization - O(n)
public static long FibonacciMemoized(int n)
{
    var memo = new Dictionary<int, long>();
    return FibonacciHelper(n, memo);
}

private static long FibonacciHelper(int n, Dictionary<int, long> memo)
{
    if (n <= 1) return n;
    
    if (memo.ContainsKey(n))
        return memo[n];
    
    memo[n] = FibonacciHelper(n - 1, memo) + FibonacciHelper(n - 2, memo);
    return memo[n];
}

// Generate all subsets of a set (Power Set)
public static List<List<T>> GenerateSubsets<T>(List<T> set)
{
    if (set.Count == 0) 
        return new List<List<T>> { new List<T>() };
    
    T first = set[0];
    List<T> rest = set.Skip(1).ToList();
    
    // Get all subsets without the first element
    List<List<T>> subsetsWithoutFirst = GenerateSubsets(rest);
    
    // Create subsets with the first element
    List<List<T>> subsetsWithFirst = subsetsWithoutFirst
        .Select(subset => new List<T> { first }.Concat(subset).ToList())
        .ToList();
    
    // Combine both - doubles the number of subsets each recursion
    return subsetsWithoutFirst.Concat(subsetsWithFirst).ToList();
}

// Tower of Hanoi - classic exponential problem
public static void TowerOfHanoi(int n, char source, char destination, char auxiliary)
{
    if (n == 1)
    {
        Console.WriteLine($"Move disk 1 from {source} to {destination}");
        return;
    }
    
    // Move n-1 disks to auxiliary peg
    TowerOfHanoi(n - 1, source, auxiliary, destination);
    
    // Move the largest disk to destination
    Console.WriteLine($"Move disk {n} from {source} to {destination}");
    
    // Move n-1 disks from auxiliary to destination
    TowerOfHanoi(n - 1, auxiliary, destination, source);
}

// Solve N-Queens problem (backtracking)
public static List<int[]> SolveNQueens(int n)
{
    var solutions = new List<int[]>();
    var board = new int[n];
    SolveNQueensHelper(board, 0, n, solutions);
    return solutions;
}

private static void SolveNQueensHelper(int[] board, int row, int n, List<int[]> solutions)
{
    if (row == n)
    {
        solutions.Add((int[])board.Clone());
        return;
    }
    
    for (int col = 0; col < n; col++)
    {
        if (IsSafe(board, row, col))
        {
            board[row] = col;
            SolveNQueensHelper(board, row + 1, n, solutions);  // Exponential branching
        }
    }
}

private static bool IsSafe(int[] board, int row, int col)
{
    for (int i = 0; i < row; i++)
    {
        if (board[i] == col || 
            board[i] - i == col - row || 
            board[i] + i == col + row)
        {
            return false;
        }
    }
    return true;
}
```

### Factorial Time - O(n!)
**Characteristic:** Generates all permutations/arrangements

```csharp
// Generate all permutations of an array
public static List<List<T>> GeneratePermutations<T>(List<T> array)
{
    if (array.Count <= 1) 
        return new List<List<T>> { new List<T>(array) };
    
    var result = new List<List<T>>();
    
    for (int i = 0; i < array.Count; i++)
    {
        T current = array[i];
        // Create list without current element
        var remaining = array.Where((item, index) => index != i).ToList();
        
        // Get all permutations of remaining elements: (n-1)! permutations
        var perms = GeneratePermutations(remaining);
        
        // Add current element to front of each permutation
        foreach (var perm in perms)
        {
            var newPerm = new List<T> { current };
            newPerm.AddRange(perm);
            result.Add(newPerm);
        }
    }
    
    return result;  // Total: n × (n-1)! = n! permutations
}

// Traveling Salesman Problem (brute force approach)
public static (List<int> path, double distance) TravelingSalesman(double[,] distances)
{
    int n = distances.GetLength(0);
    var cities = Enumerable.Range(1, n - 1).ToList(); // Start from city 0
    
    var allPermutations = GeneratePermutations(cities);
    double minDistance = double.MaxValue;
    List<int> bestPath = null;
    
    foreach (var perm in allPermutations)  // Check all (n-1)! permutations
    {
        var path = new List<int> { 0 };  // Start at city 0
        path.AddRange(perm);
        path.Add(0);  // Return to start
        
        double totalDistance = 0;
        for (int i = 0; i < path.Count - 1; i++)
        {
            totalDistance += distances[path[i], path[i + 1]];
        }
        
        if (totalDistance < minDistance)
        {
            minDistance = totalDistance;
            bestPath = new List<int>(path);
        }
    }
    
    return (bestPath, minDistance);
}

// Generate all possible arrangements of a string
public static List<string> GenerateStringPermutations(string str)
{
    if (str.Length <= 1) 
        return new List<string> { str };
    
    var result = new List<string>();
    var chars = str.ToList();
    var permutations = GeneratePermutations(chars);
    
    foreach (var perm in permutations)
    {
        result.Add(new string(perm.ToArray()));
    }
    
    return result.Distinct().ToList();  // Remove duplicates if any
}

// Solve puzzle by trying all possible arrangements
public static bool SolvePuzzleByBruteForce<T>(T[] pieces, Func<T[], bool> isValidSolution)
{
    var allArrangements = GeneratePermutations(pieces.ToList());
    
    foreach (var arrangement in allArrangements)  // Try all n! arrangements
    {
        if (isValidSolution(arrangement.ToArray()))
        {
            return true;  // Found a solution
        }
    }
    
    return false;  // No solution found
}

// Example usage of the puzzle solver
public static void ExamplePuzzleUsage()
{
    int[] pieces = { 1, 2, 3, 4, 5 };
    
    // Example: find arrangement where each element is greater than previous
    bool result = SolvePuzzleByBruteForce(pieces, arr => 
    {
        for (int i = 1; i < arr.Length; i++)
        {
            if (arr[i] <= arr[i - 1]) return false;
        }
        return true;
    });
    
    Console.WriteLine($"Solution found: {result}");
}
```

---

## Space Complexity

Space complexity analyzes memory usage growth, following the same notation principles:

**Categories:**
- **Constant Space O(1):** Fixed memory usage regardless of input
- **Linear Space O(n):** Memory grows proportionally with input
- **Quadratic Space O(n²):** Memory grows with square of input

```csharp
// O(1) Space - only uses a few variables
public static T FindMax<T>(T[] array) where T : IComparable<T>
{
    if (array.Length == 0) throw new ArgumentException("Array cannot be empty");
    
    T max = array[0];      // Constant memory - just one variable
    for (int i = 1; i < array.Length; i++)
    {
        if (array[i].CompareTo(max) > 0) 
            max = array[i];
    }
    return max;
}

// O(n) Space - creates new array of same size
public static T[] ReverseArray<T>(T[] array)
{
    T[] reversed = new T[array.Length];     // Space grows with input size
    for (int i = 0; i < array.Length; i++)
    {
        reversed[i] = array[array.Length - 1 - i];
    }
    return reversed;
}

// O(n) Space - recursive call stack
public static long FactorialRecursive(int n)
{
    if (n <= 1) return 1;
    return n * FactorialRecursive(n - 1);  // Each call uses stack space
}

// O(1) Space - iterative version of same algorithm
public static long FactorialIterative(int n)
{
    long result = 1;  // Only uses constant extra space
    for (int i = 2; i <= n; i++)
    {
        result *= i;
    }
    return result;
}

// O(n²) Space - creates matrix
public static int[,] CreateMatrix(int n)
{
    int[,] matrix = new int[n, n];       // Space grows quadratically
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            matrix[i, j] = i * j;
        }
    }
    return matrix;
}

// O(n) Space - using List that grows dynamically
public static List<int> FilterPositive(int[] array)
{
    var positives = new List<int>();  // Worst case: all elements positive = O(n) space
    foreach (int num in array)
    {
        if (num > 0)
            positives.Add(num);
    }
    return positives;
}

// O(n) Space - using StringBuilder
public static string ConcatenateStrings(string[] strings)
{
    var builder = new StringBuilder();  // Space grows with total character count
    foreach (string str in strings)
    {
        builder.Append(str);
    }
    return builder.ToString();
}

// Space-efficient approach using yield (O(1) extra space)
public static IEnumerable<T> FilterLazy<T>(T[] array, Predicate<T> predicate)
{
    foreach (T item in array)  // Doesn't store results, yields one at a time
    {
        if (predicate(item))
            yield return item;
    }
}
```[i] > max) max = array[i];
    }
    return max;
};

// O(n) Space - creates new array of same size
const reverseArray = (array) => {
    const reversed = [];     // Space grows with input size
    for (let i = array.length - 1; i >= 0; i--) {
        reversed.push(array[i]);
    }
    return reversed;
};

// O(n²) Space - creates matrix
const createMatrix = (n) => {
    const matrix = [];       // Space grows quadratically
    for (let i = 0; i < n; i++) {
        matrix[i] = new Array(n).fill(0);
    }
    return matrix;
};
```

---

## Practical Analysis Tips

### 1. **Identify the Basic Operations**
Focus on operations that scale with input size:
- Comparisons in sorting algorithms
- Array accesses in search algorithms
- Recursive calls in divide-and-conquer

### 2. **Count Nested Loops**
- One loop: O(n)
- Two nested loops: O(n²)
- Three nested loops: O(n³)

### 3. **Analyze Recursive Algorithms**
**Simple approach:** Count how the problem breaks down

**Example:** Fibonacci fibonacci(5) calls fibonacci(4) + fibonacci(3)
```
fibonacci(5)
├── fibonacci(4)
│   ├── fibonacci(3)
│   └── fibonacci(2)
└── fibonacci(3)
    ├── fibonacci(2)  
    └── fibonacci(1)
```
**Pattern:** Each call makes 2 more calls → grows like 2ⁿ

**Use the Master Theorem** for divide-and-conquer (don't worry about the math):
```
T(n) = a × T(n/b) + f(n)
```
**Just ask yourself:**
- How many pieces do I break the problem into? (a)
- How much smaller is each piece? (divide by b)  
- How much work besides the recursive calls? (f(n))

### 4. **Drop Constants and Lower-Order Terms**
**Think "What matters when numbers get really big?"**

**Examples:**
- 3n + 5: When n = 1,000,000, the "+5" doesn't matter → O(n)
- n² + n + 1: When n = 1,000,000, the "n + 1" is tiny compared to n² → O(n²)
- 10n: The "10" is just a constant multiplier → O(n)

**Rule of thumb:** Keep the term that grows fastest, ignore everything else.

### 5. **Best, Average, Worst Cases**
Consider different scenarios:
- **Quicksort:** O(n log n) average, O(n²) worst
- **Binary Search:** O(log n) all cases
- **Linear Search:** O(1) best, O(n) worst

---

## Quick Reference

### **Complexity Hierarchy (Best → Worst)**
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)

### **Rule of Thumb for Input Sizes**
**"How big can my data be before this gets painfully slow?"**
- **O(1), O(log n):** Any size (these are your friends!)
- **O(n):** Up to 100 million elements (like processing every person in a country)
- **O(n log n):** Up to 1 million elements (good sorting algorithms)
- **O(n²):** Up to 10,000 elements (small datasets only)
- **O(n³):** Up to 1,000 elements (very small datasets)
- **O(2ⁿ):** Up to ~20 elements (tiny problems only)
- **O(n!):** Up to ~10 elements (almost never practical)

**Memory aid:** Each step down, you lose about 2-3 zeros from your maximum practical size.

### **Common Algorithm Complexities**
| Algorithm | Best Case | Average Case | Worst Case | Space |
|-----------|-----------|--------------|------------|-------|
| **Searching** |
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Hash Table Lookup | O(1) | O(1) | O(n) | O(n) |
| **Sorting** |
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| **Data Structures** |
| Array Access | O(1) | O(1) | O(1) | O(n) |
| Stack Push/Pop | O(1) | O(1) | O(1) | O(n) |
| Queue Enqueue/Dequeue | O(1) | O(1) | O(1) | O(n) |
| Linked List Access | O(n) | O(n) | O(n) | O(n) |
| Binary Tree Search | O(log n) | O(log n) | O(n) | O(n) |
| **Graph Algorithms** |
| DFS/BFS | O(V + E) | O(V + E) | O(V + E) | O(V) |

### **Memory Tips**
- **Big O:** "Oh no, this could be slow!" (Worst case)
- **Big Ω:** "At least this fast" (Best case)  
- **Big Θ:** "Exactly this growth rate" (Tight bound)
- **Drop constants:** Focus on growth rate, not exact count
- **Worst case matters:** Plan for Murphy's Law in critical systems