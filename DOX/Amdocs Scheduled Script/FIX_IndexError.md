# Fix: IndexError - tuple index out of range

## Issue

Error when executing SQL query:
```
IndexError: tuple index out of range
at cursor.execute(query, (part_id_start, part_id_end, spec_ver_id))
```

## Root Cause

The positional parameter syntax (`%s`) in psycopg2 can sometimes cause issues depending on the version or query complexity. The error occurred when passing a tuple of parameters to `cursor.execute()`.

## Solution

**Changed from positional parameters to named parameters**

### Before (Positional):
```python
query = """
    WHERE 
        oai.part_id BETWEEN %s AND %s
        AND oai.spec_ver_id = %s
        AND spoi.name NOT LIKE '%MM_PROD_TEST%'
"""

cursor.execute(query, (part_id_start, part_id_end, spec_ver_id))
```

### After (Named):
```python
query = """
    WHERE 
        oai.part_id BETWEEN %(part_id_start)s AND %(part_id_end)s
        AND oai.spec_ver_id = %(spec_ver_id)s
        AND spoi.name NOT LIKE %(test_pattern)s
"""

params = {
    'part_id_start': int(part_id_start),
    'part_id_end': int(part_id_end),
    'spec_ver_id': str(spec_ver_id),
    'test_pattern': '%MM_PROD_TEST%'
}

cursor.execute(query, params)
```

## Benefits of Named Parameters

✅ **More Reliable** - Avoids tuple indexing issues  
✅ **Clearer Code** - Easy to see what each parameter is  
✅ **Better Debugging** - Parameter names in error messages  
✅ **Type Safe** - Explicit type casting  
✅ **Less Error-Prone** - No dependency on parameter order  

## Changes Made

### 1. Query Updated
- Changed `%s` to `%(parameter_name)s` format
- Moved `'%MM_PROD_TEST%'` pattern to parameter

### 2. Parameter Passing
- Changed from tuple `(a, b, c)` to dictionary `{'a': a, 'b': b, 'c': c}`
- Added explicit type casting: `int()` for integers, `str()` for strings

### 3. Enhanced Error Logging
- Added parameter value logging on error
- Added parameter type logging for debugging
- Added line number tracking in errors

## Testing

After this fix, the query should:
1. Execute without IndexError
2. Fetch data successfully
3. Log parameters clearly if errors occur

## Deployment

Just replace the file `checkUserPendingTask_converted.py` with the updated version.

No other changes needed:
- Database configuration unchanged
- Email configuration unchanged
- Dependencies unchanged
- Execution flow unchanged

---

**Fixed**: October 20, 2024  
**Status**: ✅ Ready for deployment















