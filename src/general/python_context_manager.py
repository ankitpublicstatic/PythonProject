"""
Python context manager: Context managers in Python are a way to manage resources efficiently and safely,
Ensuring that setup and cleanup actions are performed automatically. They are most common used with the "with"
statement, which guarantees that resources are properly acquired and released, even if exceptions occur during execution.
This is particularly useful for handling files, database connections, lock or any scenario where you need to
"enter" a context (Setup) and "exit" it (Cleanup).

context manager helps prevent resources leaks and make src more readable by
encapsulating the try-finally pattern. There were introduced in Python 2.5 via PEP 343
and have a core feature since.

Basic usage: The with statement is the primary way to use context managers. For example opening file
"""
import tempfile
from logging import Manager

from click import Context

with open('file.txt', 'r') as f:
    content = f.read()
    # Do something with content
# File is automatically closed here, even if an exception occurs inside the block

"""
Here, open() returns a context manager that handles opening the file (__enter__) and closing it (__exit__).

if an exception happens inside the with block the __exit__ method is still called, allowing for proper cleanup. 

How Context manager work: 
A context manager is any object that implements two special methods. 

__enter__(self): Called when entering the with block. It can return a value that's bound to the as variable (e.g. the file objects above)

__exit__(self, exc_type, exc_value, traceback): Called when exiting the with block, whether normally or due to an exception. It receives exception details if one occurred.

If it return True, the exception is suppressed (swallowed); otherwise, it's re-raised.

If no exception, exc_type, exc_value and traceback are None.
Creating a context manager Using a class

You can define your own by implementing __enter__ and __exit__ methods.

Example: A simple timer context manager.
"""

import time
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self # Return self, so 'as t' can access the instance

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time()
        print(f"Execution time: {self.end - self.start} seconds")
        if exc_type is not None:
            print(f"Exception occurred: {exc_type}")
            return False # Re-raise the exception.

with Timer() as t:
    time.sleep(2)
    # Optionally raise an error: raise ValueError("Oops")
"""
In this example: 

__enter__ starts the timer and returns the instance.
__exit__ calculates the time, handles any exception info, and can decide to suppress the exception by returning Ture

Creating a Context Manager Using the @contextmanager Decorator
For Simpler cases, use the contextlib modules @contextmanager decorator. 
This turns a generator function into a context manager, where yield separates setup from cleanup. 

Example: Same timer using decorator
"""

from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.time()
    try:
        yield # This is where the with block executes
    finally:
        end = time.time()
        print(f"Execution time: {end - start} seconds")

with timer():
    time.sleep(2)

"""
Here:
Code before yield is like __enter__
Code after yield (in finally) is like __exit__

If an exception occurs in the with block, it's re-raised after the finally block runs.

To suppress exceptions, use try except around the yield and handle it.

This is more concise for generators and avoids full class definitions.
"""

# Nested Context Managers: You can nest with statements or use multiple in on with
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    outfile.write(infile.read())
# Both files auto-closed

# Nested
with open('file.txt', 'r') as inputfile:
    with open('Output.txt', 'w') as outputfile:
        outputfile.write(inputfile.read())

# Exception Handling in Context Managers: In __exit__, you can inspect and handle exceptions.
# Example: Suppress a specific exception.

class SuppressFileNotFound:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is FileNotFoundError:
            print("File not found, but suppressing")
            return True # Suppress
        return False

with SuppressFileNotFound():
    with open('nonexitentfile.txt', 'r') as nonexitentfile:
        pass
# No error raised, prints "File not found, but suppressing"

"""
Advance Topics:
Contextlib Utillties: contextlib.suppress(*exceptions): Suppress specified exceptions
"""

from  contextlib import suppress
with suppress(FileNotFoundError, PermissionError):
    open("missing.txt").read()

# No error if file missing

# redirect_stdout(io.StringIO()): Redirect output

from contextlib import redirect_stdout
import io

f = io.StringIO()
with redirect_stdout(f):
    print("Captured output")
print(f.getvalue()) # Captured output\n

# contextlib.redirect_stdout(new_targe): Redirects print output.
# contextlib.ExitStack(): Manages a stack of context managers dynamically, useful for variable numbers.

from contextlib import ExitStack

files = ['file.txt', 'file2.txt']
with ExitStack() as stack:
    opened_files = [stack.enter_context(open(fname)) for fname in files]
    # Process opened_files
# All auto-closed

# 2. Async Context Managers (Python 3.7+)
# For async src, use __aenter__ and __aexit__ (Note the 'a' for async). or @asynccontextmanager from contextlib.

from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def async_timer():
    start = asyncio.get_event_loop().time()
    try:
        yield
    finally:
        end = asyncio.get_event_loop().time()
        print(f"Async Execution time: {end - start} seconds")

async def main():
    async  with async_timer():
        await asyncio.sleep(2)

asyncio.run(main())

# 3. Third-Party and standard Library Examples:
# threading.Lock(): Use with "with" for thread safety.

import threading
lock = threading.Lock()
with lock:
    # Critical section

#tempfile.TemporaryFile(): # Auto deletes file on exit()

# DAtabase: Many ORMs like SQLAlchemy use context managers for sessions.

"""
3. Customizing for classes:

Inherit from contextlib.AbstractContextManager (Python 3.9+) for type hints

Handle __init__ for state.

Common Use Cases:

Files/Sockets: open(), socket.socket().makefile().

Locks: threading.Look(), asyncio.Lock()

DB Sessions: SQLAlchemy's sessionmaker()

Temporary Resources: tempfile.NamedTemporaryFile()

Testing: Mocking contexts in unittest.mock.

Pitfalls and Best Practice

Order Matters: Entry left-to-right, exit right-to-left-mind dependencies.

No Re-entrancy: Most aren't thread-safe; use locks if multi-threaded

Exception in Setup/Teardown: __enter__ exceptions skip the block but run __exit__ with None's. Teardown exceptions override the original if both occur. 

Performance: Negligible overhead; use freely

Testing: Mock the manager or use asserRaises around with

Avoid manual calls: Don't call __enter__ / __exit__ directly-use with.

Context managers embody Python's "batteries included" philosophy, making resource handling elegant. 

"""
"""
4. Best Practices and Pitfalls:

Always use "with" for resources to avoid leaks. 
__exit__ should not raise exceptions unless necessary, as it can mask original errors. 
For reusable managers, prefer classes; for one-offs, use decorators.
Context managers are not thread-safe. by default, use locks if needed.
Performance: Minimal overhead, but avoid in hot loops if unnecessary. 

Context managers promote clean, exception-safe src. 
"""

from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def async_db_connection(db_name):
    print(f"Setup: Async connection to {db_name}....")
    connection = f"Async connection to {db_name}"
    # Simulate async setup: await some_connect()
    await asyncio.sleep(.5) # mimic network delay

    try:
        await yield connection # Yield for block; await to pause
    except Exception as e:
        print(f"Teardown: Async rollback due to {e}")
        raise
    finally:
        print(f"Teardown: Async closing {db_name}")
        await asyncio.sleep(.5) # Mimic async disconnect

async def main():
    async with async_db_connection('postgres') as connection:
        print(f"Using connection: {connection}")
        await asyncio.sleep(0.5)
        # raise RuntimeError("Query failed async")

asyncio.run(main())

# This is generator-style: more Pythonic for linear flows, less boilerplate than classes.

# Using a Async Code: With Built-in Async Resources: asyncio provides many e.g., asyncio.Lock()

import asyncio

async def critical_section(lock, shared_resource):
    async with lock:
        shared_resource += 1
        await asyncio.sleep(0.1)
        return shared_resource

async def worker(lock, resource, id):
    for _ in range(3):
        val = await critical_section(lock, resource)
        print(f"Worker {id}: {val}")

async def main():
    lock = asyncio.Lock()
    resource = 0
    await asyncio.gather(
        worker(lock, resource, 1),
        worker(lock, resource, 2),
    )

asyncio.run(main())

# Async File I/O: Use aiofiles (third-party, but assume available or note it.)

# pip install aiofile
import aiofiles

async def read_file_async(filename):
    async with aiofiles.open(filename, 'r') as f:
        content = await f.read()
        return content

# Multiple Async Contexts: Comma-seprate or nest:

async with lock1, lock2: # Multiple
    # Both acquired
    pass

async with outer():
    async with inner(): # Nested
        pass

# Entry: left-to-right; exit: right-to-left

# Suppressing Exceptions in Async: like sync, return True from __aexit__ or handle in decorator.
# Example: Suppress asyncio.TimeoutError

class AsyncSuppressor:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is asyncio.TimeoutError:
            print("Timeout suppressed async")
            return True
        return False

async def main():
    async with AsyncSuppressor():
        try:
            await asyncio.wait_for(asyncio.sleep(1), timeout=0.5)
        except asyncio.TimeoutError:
            pass # But suppressed anyway

"""
Advance Topics: 

1. Cancellation handling: 

asyncio.CancelledError (from task cancellation) is treated like any exception __aexit__ runs. 
Use try-except asyncio.CancelledError in __aexit__ for cleanup. 

2. Contextlib Utilities for Async:

@asynccontextmanager
AsyncExitStack: Dynamic staking (Like ExitStack but async)

"""

from contextlib import AsyncExitStack
import asyncio
async def make_connections(names):
    async with AsyncExitStack() as stack:
        conns = [await stack.enter_async_context(async_db_connection(name)) for name in names]
        # Use conns
        yield conns # If in a generator
# Usage in async func

"""
3. Custom Async Locks or semaphores:
Extend asyncio.Lock or implement from scratch for rate-limiting.

4. Integration with Frameworks:
FastAPI/Starlette: Use for DB Sessions (e.g., async SQLAlchemy).
aiohttp: Sessions as async contexts.

Differences from Synchronous Context Managers;

Methods: __enter__, __exit__ (sync) > __aenter__, __aexit__ (async)

Syntax: with > async with (in async def)

Invocation: Direct call > Awaited implicitly

Use Case: CPU-bound, simple resources > I/O-bound, concurrent(e.g., networks)

Decorator: @contextmanager (generator) > @asynccontextmanager (async generator)

Exception flow: Sync raises > Propagates via event looop

Best Practices and Pitfalls:

Always Await: Forget await in __aenter__ , __aexit__ ? It blocks-use async ops inside.

Event Loop: RUn with asyncio.run() or in existing loop; no nesting asyncio.run()

Cancellation: Handle CancelledError explicitly for graceful shutdowns.

Testing: Use pytest-asyncio for async with in tests.
Performance: Minimal overhead, but avoid in tight loops.

Pitfalls:
    Not interchangeable: Can't use sync in async with and vice versa.
    __aexit__ must be async even if no awaits-It's a coroutine. 
    In nested tasks, ensure proper propagation.
    
When to Use Class vs Decorator: Class for complex state/multiple methods, decorator for linear setup/teardown..

Async context managers unlock non-blocking resource handling, making asyncio src robust. Experiment in an IPython kernel with %run for 
quick tests For more, see Python docs on asyncio and contextlib. 
    
"""