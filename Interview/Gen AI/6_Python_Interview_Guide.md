# 6. Python – Interview Guide

Skills covered: Python fundamentals, data structures, OOP, async, APIs, testing, best practices.

---

## Quick Reference

| Area | Key Points |
|------|------------|
| Types & data | int, float, str, bool, list, dict, set, tuple; type hints |
| Control flow | if/elif/else, for, while, comprehensions |
| Functions | def, *args, **kwargs, lambda, decorators, generators |
| OOP | class, __init__, inheritance, encapsulation, duck typing |
| Modules | import, __name__ == "__main__", venv, pip |
| Async | async/await, asyncio, I/O-bound concurrency |
| Best practices | PEP 8, venv, env vars, logging, testing |

---

## Core Concepts

### 1. Data Structures

- list: Ordered, mutable, [1, 2, 3]; indexing, slicing, append, extend.
- dict: Key-value, mutable, {"a": 1}; keys unique, O(1) lookup.
- set: Unordered, unique elements, mutable; no duplicates, fast membership.
- tuple: Ordered, immutable, (1, 2); hashable if elements hashable.
- str: Immutable sequence of characters; slicing, split, join, format.

### 2. Comprehensions

- List: [x**2 for x in range(10) if x % 2 == 0]
- Dict: {k: v for k, v in items}
- Set: {x for x in iterable}
- Generator: (x for x in iterable) – lazy, one-pass.

### 3. Functions

- Default args: def f(a, b=1); defaults evaluated once (avoid mutable defaults).
- *args, **kwargs: Variable positional and keyword args.
- Lambda: lambda x: x**2 – single expression.
- Decorators: Function that wraps another; @decorator above def.

### 4. OOP

- class, __init__(self), self; inheritance, super().
- Encapsulation: naming _private; __name mangling.
- Duck typing: "If it walks like a duck…" – use protocols/interfaces by behavior.
- Magic methods: __str__, __repr__, __len__, __getitem__, __enter__/__exit__ (context manager).

### 5. File & Environment

- open(), with open() as f, read/write; pathlib for paths.
- os.environ, .env files (python-dotenv); never hardcode secrets.
- __name__ == "__main__": run code only when script executed directly.

### 6. Async (Basics)

- async def, await; coroutines, event loop (asyncio.run).
- Use for I/O-bound concurrency (HTTP, DB); not for CPU-bound (use ProcessPoolExecutor).
- async with, async for for async context and iteration.

### 7. Testing & Quality

- unittest or pytest; assert, fixtures, parametrize.
- Mock/patch for external deps; coverage for line coverage.
- Type hints (typing module) for clarity and tooling; mypy for checking.

---

## Top 25 Interview Q&A – Python

Q1: What is the difference between list and tuple?
> "List is mutable; tuple is immutable. Tuple can be used as dict key or in set if elements are hashable. Use tuple for fixed sequences (e.g. return values, coordinates); list for dynamic collections."

Q2: When do you use dict vs list?
> "Dict when you need key-value lookup by identity (e.g. id → object); list when order and index matter. Dict is O(1) lookup by key; list is O(1) by index but O(n) search by value."

Q3: What is the difference between == and is?
> "== compares values; is compares object identity (same object in memory). Use is for None, True, False; == for values. For custom classes, override __eq__ for ==."

Q4: Explain *args and **kwargs.
> "*args collects extra positional args as tuple; **kwargs collects extra keyword args as dict. Used for flexible APIs and decorators. Naming is convention; only * and ** matter."

Q5: What is a decorator?
> "A function that takes another function and returns a wrapped function (e.g. adds logging, timing, auth). @decorator above def is syntactic sugar for func = decorator(func). Can take args with nested functions."

Q6: What is the GIL and how does it affect concurrency?
> "Global Interpreter Lock: only one thread runs Python bytecode at a time. Limits CPU-bound parallelism in threads; I/O-bound threads still help (release GIL during I/O). For CPU-bound, use multiprocessing or native extensions."

Q7: What is the difference between shallow and deep copy?
> "Shallow copy (copy.copy or list.copy()) copies top level; nested objects are references. Deep copy (copy.deepcopy()) recursively copies all levels. Use deep copy when you need independent nested structures."

Q8: How do you handle exceptions?
> "try/except/else/finally. Catch specific exceptions (e.g. ValueError), not bare except. Use else for code that runs when no exception; finally for cleanup. Raise or re-raise with raise."

Q9: What is a generator and why use it?
> "Function with yield; returns an iterator that produces values lazily (one at a time). Saves memory for large sequences; enables streaming. next(), for loop, or list(gen) to consume."

Q10: What is __init__ vs __new__?
> "__init__ initializes an instance (called after creation). __new__ is the constructor that creates and returns the instance; used for immutable types or singletons. Usually you only override __init__."

Q11: What is the difference between class method and static method?
> "@classmethod: first arg is class (cls); use for factory or alternate constructors. @staticmethod: no self/cls; use for utility functions that belong to the class namespace. Instance method gets self."

Q12: How do you make an object iterable?
> "Implement __iter__ (return self) and __next__ (return next value or raise StopIteration), or use yield in __iter__. Then for x in obj works."

Q13: What is a context manager and how do you create one?
> "Manages setup/teardown (e.g. open file, lock). Use with statement. Implement __enter__ and __exit__; or use @contextmanager and yield in a generator."

Q14: What is the difference between package and module?
> "Module is a single .py file. Package is a directory with __init__.py (and optionally subpackages). import package.module; from package import module."

Q15: How do you manage dependencies?
> "Use virtual env (venv, virtualenv) per project; pip install -r requirements.txt. Pin versions for reproducibility. Consider poetry or pipenv for lockfiles."

Q16: What are type hints and why use them?
> "Annotations like def f(x: int) -> str. No runtime enforcement by default; tools (mypy, IDEs) use them for checking and autocomplete. Improves readability and catches bugs early."

Q17: What is the difference between multiprocessing and threading?
> "Threading: shared memory, GIL limits CPU parallelism; good for I/O-bound. Multiprocessing: separate processes, no GIL; good for CPU-bound. asyncio: single-threaded concurrency for I/O-bound with async/await."

Q18: How do you read a large file without loading it all?
> "Open and iterate line by line: for line in open('file.txt'): or use read(size). For binary or structured data, use chunks. Generators and streaming keep memory low."

Q19: What is __name__ == "__main__"?
> "True when the file is run as script (python file.py); False when imported. Use it to run demo or CLI code only when executed directly, not when imported as module."

Q20: How do you reverse a list in place?
> "list.reverse() reverses in place and returns None. For a new list: reversed(list) or list[::-1]. reversed returns an iterator."

Q21: What is the difference between sort and sorted?
> "list.sort() sorts in place, returns None. sorted(iterable) returns a new list. Both take key= and reverse=. sorted works on any iterable."

Q22: What are * and ** in function calls?
> "Unpacking: * unpacks iterable into positional args, ** unpacks dict into keyword args. f(*[1,2], **{'c':3}) is f(1, 2, c=3)."

Q23: How do you remove duplicates from a list while preserving order?
> "dict.fromkeys(list) in Python 3.7+ preserves insertion order; list(dict.fromkeys(lst)). Or use a set + order tracking if elements are hashable."

Q24: What is the difference between encoding and decoding?
> "Encode: str → bytes (e.g. 'hi'.encode('utf-8')). Decode: bytes → str (e.g. b'hi'.decode('utf-8')). Specify encoding explicitly (utf-8) for portability."

Q25: How does Python support Gen AI / RAG development?
> "Rich ecosystem: requests/httpx for APIs, sentence-transformers for embeddings, LangChain/LangGraph for orchestration, pandas/NumPy for data. Async for concurrent API calls; type hints and tests for production pipelines."

---

## Key Talking Points

- Data structures: list vs tuple vs dict vs set; when to use each; complexity.
- Functions: defaults, *args/**kwargs, decorators, generators.
- OOP: classes, inheritance, duck typing, magic methods.
- Async: when to use; difference from threading/multiprocessing.
- Best practices: venv, type hints, testing, logging, env vars for config.

---

## See Also

- [4_Data_Analytics_Python_DS.md](4_Data_Analytics_Python_DS.md) – Pandas, NumPy, sklearn
- [3_Backend_DevOps_Cloud.md](3_Backend_DevOps_Cloud.md) – Flask, Docker
- [0_GEN_AI_MASTER_INDEX.md](0_GEN_AI_MASTER_INDEX.md) – Master index
