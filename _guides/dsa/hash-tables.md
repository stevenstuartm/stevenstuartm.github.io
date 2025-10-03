---
title: "Hash Tables"
category: Data Structures & Algorithms
---

## Why Hash Tables Exist
Provides average O(1) lookups by trading space for time using mathematical hashing. This is the fundamental trade-off that powers most modern software.

## When to Use Hash Tables

**✅ Use when:**
- Need fast lookups by key
- Counting frequencies of items
- Caching computed results
- Implementing sets (unique values)
- Building lookup tables or indexes

**❌ Don't use when:**
- Need to maintain ordering of elements
- Memory is extremely constrained
- Keys don't hash well (cause many collisions)
- Need to iterate in sorted order

**🏢 Modern reality:** Your go-to data structure. Use `Dictionary<K,V>` in C#. Hash tables power most modern software - databases, caches, compilers, etc.

## Time Complexity
- **Average case:** O(1) for all operations (lookup, insert, delete)
- **Worst case:** O(n) when many collisions occur
- **Space:** O(n) for storing key-value pairs

## How Hash Tables Work

1. **Hash Function:** Converts key to array index
2. **Compression:** Map hash code to array size using modulo
3. **Collision Handling:** Deal with multiple keys mapping to same index

## Collision Resolution Strategies

### Open Addressing (Linear Probing)
- When collision occurs, check next available slot
- Simple but can cause clustering

### Separate Chaining  
- Each array slot holds a list of key-value pairs
- More complex but handles collisions gracefully


## C# Implementation

```csharp
public class HashMap<TKey, TValue>
{
    private int arraySize;
    private (TKey key, TValue value)?[] array;
    
    public HashMap(int arraySize)
    {
        this.arraySize = arraySize;
        array = new (TKey key, TValue value)?[arraySize];
    }
    
    private int Hash(TKey key, int countCollisions = 0)
    {
        int hashCode = key.GetHashCode();
        return Math.Abs(hashCode + countCollisions);
    }
    
    private int Compressor(int hashCode)
    {
        return hashCode % arraySize;
    }
    
    public void Assign(TKey key, TValue value)
    {
        int arrayIndex = Compressor(Hash(key));
        var currentArrayValue = array[arrayIndex];
        
        // Empty slot - insert directly
        if (!currentArrayValue.HasValue)
        {
            array[arrayIndex] = (key, value);
            return;
        }
        
        // Key already exists - update value
        if (EqualityComparer<TKey>.Default.Equals(currentArrayValue.Value.key, key))
        {
            array[arrayIndex] = (key, value);
            return;
        }
        
        // Collision - use linear probing
        int numberCollisions = 1;
        while (!EqualityComparer<TKey>.Default.Equals(currentArrayValue.Value.key, key))
        {
            int newHashCode = Hash(key, numberCollisions);
            int newArrayIndex = Compressor(newHashCode);
            currentArrayValue = array[newArrayIndex];
            
            if (!currentArrayValue.HasValue)
            {
                array[newArrayIndex] = (key, value);
                return;
            }
            
            if (EqualityComparer<TKey>.Default.Equals(currentArrayValue.Value.key, key))
            {
                array[newArrayIndex] = (key, value);
                return;
            }
            
            numberCollisions++;
            
            // Prevent infinite loop if table is full
            if (numberCollisions >= arraySize)
            {
                throw new InvalidOperationException("HashMap is full");
            }
        }
    }
    
    public TValue Retrieve(TKey key)
    {
        int arrayIndex = Compressor(Hash(key));
        var possibleReturnValue = array[arrayIndex];
        
        if (!possibleReturnValue.HasValue)
        {
            return default(TValue);
        }
        
        if (EqualityComparer<TKey>.Default.Equals(possibleReturnValue.Value.key, key))
        {
            return possibleReturnValue.Value.value;
        }
        
        // Handle collision case
        int retrievalCollisions = 1;
        while (possibleReturnValue.HasValue && 
               !EqualityComparer<TKey>.Default.Equals(possibleReturnValue.Value.key, key))
        {
            int newHashCode = Hash(key, retrievalCollisions);
            int retrievingArrayIndex = Compressor(newHashCode);
            possibleReturnValue = array[retrievingArrayIndex];
            
            if (!possibleReturnValue.HasValue)
            {
                return default(TValue);
            }
            
            if (EqualityComparer<TKey>.Default.Equals(possibleReturnValue.Value.key, key))
            {
                return possibleReturnValue.Value.value;
            }
            
            retrievalCollisions++;
            
            // Prevent infinite loop
            if (retrievalCollisions >= arraySize)
            {
                break;
            }
        }
        
        return default(TValue);
    }
}

// Example usage
var hashMap = new HashMap<string, string>(16);
hashMap.Assign("name", "Alice");
hashMap.Assign("age", "25");
hashMap.Assign("city", "NYC");

Console.WriteLine(hashMap.Retrieve("name"));    // "Alice"
Console.WriteLine(hashMap.Retrieve("age"));     // "25"  
Console.WriteLine(hashMap.Retrieve("missing")); // null or default
```

## Common Hash Table Applications

### Frequency Counting

### Caching/Memoization

### Two-Sum Problem (Interview Classic)

## Performance Considerations

**Load Factor:** Ratio of filled slots to total slots
- Keep load factor < 0.7 for good performance
- Resize table when load factor gets too high

**Hash Function Quality:**
- Good distribution reduces collisions
- C# has optimized hash functions for built-in types via `GetHashCode()`

**Collision Strategy Impact:**
- Linear probing: Good cache performance but clustering issues
- Separate chaining: More memory overhead but handles high load factors better

## Interview Tips

**Common Questions:**
1. Implement basic hash table operations
2. Handle collisions gracefully  
3. Explain time complexity trade-offs
4. Solve problems using hash tables (two-sum, anagrams, etc.)

**Key Points to Mention:**
- Average O(1) operations vs O(n) worst case
- Trade memory for time
- Critical for many algorithms (counting, lookups, caching)
- Foundation of modern databases and caches

## Modern Usage

**C#:** Use `Dictionary<K,V>` - generic, fast, well-tested with excellent performance
**Collections:** Also consider `ConcurrentDictionary<K,V>` for thread-safe scenarios
**When to implement custom:** Almost never in production, but common interview topic

The implementations above are educational - they show the core concepts but lack optimizations like dynamic resizing, better hash functions, and robust error handling found in production hash tables.