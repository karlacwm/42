*This project has been created as part of the 42 curriculum by wcheung.*

# project plan
Phase 1: Architecture & Parsing (📍 We are almost done here)Done: Parse and validate all command-line arguments.  Next: Define the data structures for the Coders and the Dongles, and allocate memory for them.

Phase 2: Data Structures for SchedulersImplement a Priority Queue (a min-heap) in C. This is required to handle the fifo and edf scheduling policies fairly when multiple coders want the same dongles.

Phase 3: Thread Initialization & Core LoopSpin up one thread per coder using pthread_create.  Write the infinite loop where coders attempt to: grab dongles -> compile -> debug -> refactor.

Phase 4: Synchronization & ArbitrationThe hardest part: using pthread_mutex_t and condition variables to safely lock the dongles.  Implement the dongle_cooldown timer.  Serialize the logging so text doesn't overlap in the terminal.

Phase 5: The Monitor Thread & CleanupCreate a dedicated "Monitor" thread that constantly checks if any coder has exceeded time_to_burnout or if everyone hit number_of_compiles_required.  Cleanly shut down all threads, destroy all mutexes, and free all the memory we allocated.

========
Phase 1: Parsing & Validation (Complete)
Phase 2: Data Structures & Memory Allocation (Complete)
Phase 3: Utility Functions (Time & Logging) (Complete)
Phase 4: The Coder Lifecycle & Thread Launching (We are here)
Phase 5: Synchronization & Scheduling (The hardest part: locking the dongles using FIFO/EDF).
Phase 6: The Monitor Thread & Cleanup (Checking for burnouts and freeing memory)

## Description

Coders can compile, debug, or refactor. The project codexion is about

## Instruction

To build:
```
cd coders && make
```

Test the program with the exact number of arguments:

(Values should be positive integers. Time value will be parsed in milliseconds and there should be at least one coder.)
```
./codexion <no_of_coders> <time_to_burnout> <time_to_compile> <time_to_debug> <time_to_refactor> <no_of_compiles_required> <dongle_cooldown> <edf/fifo>
```

For example:
```
./codexion 5 500 50 50 50 3 50 fifo
```

To test with valgrind and helgrind:
```
valgrind ./codexion 5 500 50 50 50 3 50 fifo
valgrind --tool=helgrind ./codexion 5 500 50 50 50 3 50 fifo
```

Example test to show difference in edf and fifo

```
./codexion 4 600 200 100 100 5 10 fifo
./codexion 4 600 200 100 100 5 10 edf
```

## Blocking cases handled


## Thread synchronization mechanisms


## Resources
https://www.youtube.com/watch?v=d9s_d28yJq0&list=PLfqABt5AS4FmuQf70psXrsMLEDQXNkLq2&index=1
https://www.youtube.com/watch?v=mvZKu0DfFLQ
https://www.youtube.com/watch?v=zOpzGHwJ3MU
https://www.youtube.com/watch?v=ldJ8WGZVXZk
https://man7.org/linux/man-pages/man7/pthreads.7.html
https://pubs.opengroup.org/onlinepubs/7908799/xsh/pthread.h.html
https://www.geeksforgeeks.org/c/thread-functions-in-c-c/
https://blog.gtwang.org/programming/pthread-multithreading-programming-in-c-tutorial/
https://medium.com/@ruinadd/philosophers-42-guide-the-dining-philosophers-problem-893a24bc0fe2
https://tigercosmos.xyz/en/post/2020/07/simple-pthread-usage/
https://medium.com/@jalal92/the-dining-philosophers-7157cc05315
https://suspectedoceano.notion.site/Philosophers-b1bf3c57eee6420cafa7d0900b3d3216
https://www.codequoi.com/en/threads-mutexes-and-concurrent-programming-in-c/
https://www.geeksforgeeks.org/c/heap-in-c/

For this project, the README.md must also include:
• A “Blocking cases handled” section describing all the concurrency issues addressed in your solution (e.g., deadlock prevention and Coffman’s conditions, starvation prevention, cooldown handling, precise burnout detection, and log serialization).
• A “Thread synchronization mechanisms” section explaining the specific threading primitives used in your implementation (pthread_mutex_t, pthread_cond_t, custom event implementation) and how they coordinate access to shared resources (dongles, logging, monitor state). Include examples of how race conditions are prevented and how thread-safe communication is achieved between coders and the monitor
