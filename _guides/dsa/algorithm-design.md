---
title: "Algorithm Design Paradigms"
category: Data Structures & Algorithms
---

## Dynamic Programming

### Why Dynamic Programming Exists
Solves optimization problems by breaking them into simpler subproblems and storing results to avoid redundant computation. Transforms exponential time complexity into polynomial time for problems with overlapping subproblems and optimal substructure.

### When to Use Dynamic Programming

**Use when:**
- Problem has overlapping subproblems (same subproblem solved multiple times)
- Problem exhibits optimal substructure (optimal solution contains optimal solutions to subproblems)
- Need to find optimal solution (minimum, maximum, count of ways)
- Recursive solution has exponential time complexity

**Don't use when:**
- Subproblems don't overlap
- Greedy approach gives optimal solution
- Simple iterative solution exists

### Time Complexity
- **Memoization (Top-down):** O(number of unique subproblems × time per subproblem)
- **Tabulation (Bottom-up):** O(number of states × time per transition)
- **Space:** O(number of states stored)

### Memoization vs Tabulation

**Memoization (Top-down):**
- Start with original problem, recurse down to base cases
- Store results as you compute them
- More intuitive for recursive problems

**Tabulation (Bottom-up):**
- Start with base cases, build up to final answer
- Fill table in predetermined order
- Often more space-efficient

### Classic DP Problems

#### 1. Longest Common Subsequence (LCS)
```csharp
public static class LCS
{
    public static int LongestCommonSubsequence(string text1, string text2)
    {
        int m = text1.Length, n = text2.Length;
        var dp = new int[m + 1, n + 1];

        for (int i = 1; i <= m; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                if (text1[i - 1] == text2[j - 1])
                {
                    dp[i, j] = dp[i - 1, j - 1] + 1;
                }
                else
                {
                    dp[i, j] = Math.Max(dp[i - 1, j], dp[i, j - 1]);
                }
            }
        }

        return dp[m, n];
    }

    // Example usage
    public static void DemonstrateLCS()
    {
        Console.WriteLine(LongestCommonSubsequence("abcde", "ace")); // 3 ("ace")
        Console.WriteLine(LongestCommonSubsequence("abc", "abc"));   // 3 ("abc")
        Console.WriteLine(LongestCommonSubsequence("abc", "def"));   // 0 (no common)
    }
}
```

#### 2. 0/1 Knapsack Problem
```csharp
public static class Knapsack
{
    public static int Knapsack01(int[] weights, int[] values, int capacity)
    {
        int n = weights.Length;
        var dp = new int[n + 1, capacity + 1];

        for (int i = 1; i <= n; i++)
        {
            for (int w = 1; w <= capacity; w++)
            {
                // Don't include current item
                dp[i, w] = dp[i - 1, w];

                // Include current item if it fits
                if (weights[i - 1] <= w)
                {
                    int includeValue = values[i - 1] + dp[i - 1, w - weights[i - 1]];
                    dp[i, w] = Math.Max(dp[i, w], includeValue);
                }
            }
        }

        return dp[n, capacity];
    }

    // Space-optimized version
    public static int KnapsackOptimized(int[] weights, int[] values, int capacity)
    {
        var dp = new int[capacity + 1];

        for (int i = 0; i < weights.Length; i++)
        {
            for (int w = capacity; w >= weights[i]; w--)
            {
                dp[w] = Math.Max(dp[w], values[i] + dp[w - weights[i]]);
            }
        }

        return dp[capacity];
    }
}
```

#### 3. Edit Distance (Levenshtein Distance)
```csharp
public static class EditDistance
{
    public static int MinDistance(string word1, string word2)
    {
        int m = word1.Length, n = word2.Length;
        var dp = new int[m + 1, n + 1];

        // Initialize base cases
        for (int i = 0; i <= m; i++) dp[i, 0] = i;  // Delete all
        for (int j = 0; j <= n; j++) dp[0, j] = j;  // Insert all

        for (int i = 1; i <= m; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                if (word1[i - 1] == word2[j - 1])
                {
                    dp[i, j] = dp[i - 1, j - 1];  // No operation needed
                }
                else
                {
                    dp[i, j] = 1 + Math.Min(
                        Math.Min(dp[i - 1, j],     // Delete
                                dp[i, j - 1]),     // Insert
                        dp[i - 1, j - 1]          // Replace
                    );
                }
            }
        }

        return dp[m, n];
    }

    // Example usage
    public static void DemonstrateEditDistance()
    {
        Console.WriteLine(MinDistance("horse", "ros"));    // 3 (h->r, r->o, se->s)
        Console.WriteLine(MinDistance("intention", "execution")); // 5
    }
}
```

---

## Greedy Algorithms

### Why Greedy Algorithms Exist
Make locally optimal choices at each step, hoping to find a global optimum. Work when local optimal choices lead to globally optimal solutions, providing simple and efficient algorithms for optimization problems.

### When to Use Greedy

**Use when:**
- Problem has greedy choice property (local optimum leads to global optimum)
- Problem has optimal substructure
- Need efficient algorithm for optimization problem
- Can prove greedy approach gives optimal solution

**Don't use when:**
- Local optimum doesn't guarantee global optimum
- Need to consider future consequences of current choices
- Problem requires backtracking or exploring multiple paths

### Classic Greedy Problems

#### 1. Activity Selection Problem
```csharp
public static class ActivitySelection
{
    public class Activity
    {
        public int Start { get; set; }
        public int End { get; set; }
        public string Name { get; set; }

        public Activity(int start, int end, string name)
        {
            Start = start;
            End = end;
            Name = name;
        }
    }

    public static List<Activity> SelectActivities(List<Activity> activities)
    {
        // Sort by ending time (greedy choice)
        activities.Sort((a, b) => a.End.CompareTo(b.End));

        var selected = new List<Activity>();
        if (activities.Count == 0) return selected;

        selected.Add(activities[0]);
        int lastEndTime = activities[0].End;

        for (int i = 1; i < activities.Count; i++)
        {
            if (activities[i].Start >= lastEndTime)
            {
                selected.Add(activities[i]);
                lastEndTime = activities[i].End;
            }
        }

        return selected;
    }
}
```

#### 2. Fractional Knapsack
```csharp
public static class FractionalKnapsack
{
    public class Item
    {
        public int Weight { get; set; }
        public int Value { get; set; }
        public double ValuePerWeight => (double)Value / Weight;

        public Item(int weight, int value)
        {
            Weight = weight;
            Value = value;
        }
    }

    public static double MaxValue(List<Item> items, int capacity)
    {
        // Sort by value per weight ratio (greedy choice)
        items.Sort((a, b) => b.ValuePerWeight.CompareTo(a.ValuePerWeight));

        double totalValue = 0;
        int remainingCapacity = capacity;

        foreach (var item in items)
        {
            if (remainingCapacity >= item.Weight)
            {
                // Take whole item
                totalValue += item.Value;
                remainingCapacity -= item.Weight;
            }
            else
            {
                // Take fraction of item
                double fraction = (double)remainingCapacity / item.Weight;
                totalValue += fraction * item.Value;
                break;
            }
        }

        return totalValue;
    }
}
```

---

## Divide & Conquer

### Why Divide & Conquer Exists
Break complex problems into smaller, manageable subproblems, solve them independently, then combine results. Leverages recursion and often achieves better time complexity than naive approaches through clever problem decomposition.

### When to Use Divide & Conquer

**Use when:**
- Problem can be broken into independent subproblems
- Subproblems have same structure as original problem
- Can efficiently combine subproblem solutions
- Want to achieve better than O(n²) complexity

**Don't use when:**
- Subproblems overlap significantly (use DP instead)
- Problem doesn't decompose naturally
- Overhead of recursion outweighs benefits

### Classic Divide & Conquer Problems

#### 1. Merge Sort Implementation
```csharp
public static class DivideConquerSort
{
    public static void MergeSort(int[] arr, int left, int right)
    {
        if (left < right)
        {
            int mid = left + (right - left) / 2;

            // Divide
            MergeSort(arr, left, mid);
            MergeSort(arr, mid + 1, right);

            // Conquer
            Merge(arr, left, mid, right);
        }
    }

    private static void Merge(int[] arr, int left, int mid, int right)
    {
        int leftSize = mid - left + 1;
        int rightSize = right - mid;

        int[] leftArray = new int[leftSize];
        int[] rightArray = new int[rightSize];

        Array.Copy(arr, left, leftArray, 0, leftSize);
        Array.Copy(arr, mid + 1, rightArray, 0, rightSize);

        int i = 0, j = 0, k = left;

        while (i < leftSize && j < rightSize)
        {
            if (leftArray[i] <= rightArray[j])
            {
                arr[k] = leftArray[i];
                i++;
            }
            else
            {
                arr[k] = rightArray[j];
                j++;
            }
            k++;
        }

        while (i < leftSize)
        {
            arr[k] = leftArray[i];
            i++;
            k++;
        }

        while (j < rightSize)
        {
            arr[k] = rightArray[j];
            j++;
            k++;
        }
    }
}
```

#### 2. Quick Select (Find Kth Largest)
```csharp
public static class QuickSelect
{
    public static int FindKthLargest(int[] nums, int k)
    {
        return QuickSelectHelper(nums, 0, nums.Length - 1, nums.Length - k);
    }

    private static int QuickSelectHelper(int[] nums, int left, int right, int k)
    {
        int pivotIndex = Partition(nums, left, right);

        if (pivotIndex == k)
        {
            return nums[pivotIndex];
        }
        else if (pivotIndex < k)
        {
            return QuickSelectHelper(nums, pivotIndex + 1, right, k);
        }
        else
        {
            return QuickSelectHelper(nums, left, pivotIndex - 1, k);
        }
    }

    private static int Partition(int[] nums, int left, int right)
    {
        int pivot = nums[right];
        int i = left;

        for (int j = left; j < right; j++)
        {
            if (nums[j] < pivot)
            {
                (nums[i], nums[j]) = (nums[j], nums[i]);
                i++;
            }
        }

        (nums[i], nums[right]) = (nums[right], nums[i]);
        return i;
    }
}
```

---

## Backtracking

### Why Backtracking Exists
Systematically explores all possible solutions by building candidates incrementally and abandoning candidates that cannot lead to valid solutions. Essential for constraint satisfaction problems and finding all solutions to combinatorial problems.

### When to Use Backtracking

**Use when:**
- Need to find all solutions to a problem
- Constraint satisfaction problems
- Combinatorial optimization
- Need to explore decision trees systematically

**Don't use when:**
- Only need one solution and greedy/DP works
- Problem has too many possibilities without good pruning
- Can solve with simpler approach

### Classic Backtracking Problems

#### 1. N-Queens Problem
```csharp
public static class NQueens
{
    public static List<List<string>> SolveNQueens(int n)
    {
        var result = new List<List<string>>();
        var board = new char[n][];

        for (int i = 0; i < n; i++)
        {
            board[i] = new char[n];
            Array.Fill(board[i], '.');
        }

        BacktrackQueens(board, 0, result);
        return result;
    }

    private static void BacktrackQueens(char[][] board, int row, List<List<string>> result)
    {
        if (row == board.Length)
        {
            result.Add(BoardToStringList(board));
            return;
        }

        for (int col = 0; col < board.Length; col++)
        {
            if (IsValidQueenPlacement(board, row, col))
            {
                board[row][col] = 'Q';  // Place queen
                BacktrackQueens(board, row + 1, result);  // Recurse
                board[row][col] = '.';  // Backtrack
            }
        }
    }

    private static bool IsValidQueenPlacement(char[][] board, int row, int col)
    {
        int n = board.Length;

        // Check column
        for (int i = 0; i < row; i++)
        {
            if (board[i][col] == 'Q') return false;
        }

        // Check diagonal (top-left to bottom-right)
        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--)
        {
            if (board[i][j] == 'Q') return false;
        }

        // Check diagonal (top-right to bottom-left)
        for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++)
        {
            if (board[i][j] == 'Q') return false;
        }

        return true;
    }

    private static List<string> BoardToStringList(char[][] board)
    {
        var result = new List<string>();
        foreach (var row in board)
        {
            result.Add(new string(row));
        }
        return result;
    }
}
```

#### 2. Generate All Subsets
```csharp
public static class SubsetGeneration
{
    public static List<List<int>> GenerateSubsets(int[] nums)
    {
        var result = new List<List<int>>();
        var currentSubset = new List<int>();

        BacktrackSubsets(nums, 0, currentSubset, result);
        return result;
    }

    private static void BacktrackSubsets(int[] nums, int start, List<int> currentSubset, List<List<int>> result)
    {
        // Add current subset to result
        result.Add(new List<int>(currentSubset));

        // Try adding each remaining element
        for (int i = start; i < nums.Length; i++)
        {
            currentSubset.Add(nums[i]);          // Include element
            BacktrackSubsets(nums, i + 1, currentSubset, result);  // Recurse
            currentSubset.RemoveAt(currentSubset.Count - 1);      // Backtrack
        }
    }

    // Alternative: Generate subsets with specific sum
    public static List<List<int>> SubsetsWithSum(int[] nums, int targetSum)
    {
        var result = new List<List<int>>();
        var currentSubset = new List<int>();

        BacktrackWithSum(nums, 0, currentSubset, 0, targetSum, result);
        return result;
    }

    private static void BacktrackWithSum(int[] nums, int start, List<int> currentSubset,
                                       int currentSum, int targetSum, List<List<int>> result)
    {
        if (currentSum == targetSum)
        {
            result.Add(new List<int>(currentSubset));
            return;
        }

        if (currentSum > targetSum) return;  // Pruning

        for (int i = start; i < nums.Length; i++)
        {
            currentSubset.Add(nums[i]);
            BacktrackWithSum(nums, i + 1, currentSubset, currentSum + nums[i], targetSum, result);
            currentSubset.RemoveAt(currentSubset.Count - 1);
        }
    }
}
```

---

## Modern Usage & Best Practices

### When to Use Each Paradigm

**Dynamic Programming:**
- Optimization problems with overlapping subproblems
- Finding optimal solutions (min/max cost, ways to do something)
- Examples: Route optimization, resource allocation, sequence alignment

**Greedy Algorithms:**
- Optimization problems where local optimum leads to global optimum
- Activity scheduling, minimal spanning trees, compression algorithms
- Examples: Task scheduling, network routing, data compression

**Divide & Conquer:**
- Problems that decompose naturally into independent subproblems
- Sorting, searching, computational geometry
- Examples: Image processing, fast mathematical operations, parallel computing

**Backtracking:**
- Constraint satisfaction and exhaustive search problems
- Puzzle solving, configuration problems, AI game playing
- Examples: Sudoku solvers, pathfinding with constraints, resource assignment

### C# Implementation Tips

**Use built-in collections:** `Dictionary<K,V>` for memoization, `List<T>` for dynamic arrays
**Prefer iterative DP:** Often more efficient than recursive memoization
**Consider space optimization:** Many DP problems can use O(1) or O(k) space instead of O(n²)
**Profile your code:** These algorithms can be memory-intensive with large inputs

### Key Takeaways

- **Pattern recognition** is more important than memorizing specific algorithms
- **Start simple** - brute force first, then optimize using appropriate paradigm
- **Consider constraints** - time limits, memory limits, and problem-specific requirements
- **Practice implementation** - these paradigms appear frequently in interviews and real-world problems