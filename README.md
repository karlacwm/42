*This project has been created as part of the 42 curriculum by wcheung.*

## Description

Coders can compile, debug, or refactor. The project codexion is about a group of coders working together in a shared environment.
There are as many coders as dongles, and a coder needs two dongles to compile.
Their work cycle is compile, debug and refactor, until they reach their compile target.
The challenge lies in the simulation, when each coder tries to get the same resource, or some have waited for too long and burned out, or deadlock situation when every coder stopped and wait for each other.

The simulation is controlled by a monitor to check if someone has burnout or everyone has reached the target. And to avoid data race, each coder has to go through the scheduler* first before they can get a dongle.

*scheduler: (1)edf - earliest deadline first, (2)fifo - first in first out

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
Youtube videos
[[1]](https://www.youtube.com/watch?v=d9s_d28yJq0&list=PLfqABt5AS4FmuQf70psXrsMLEDQXNkLq2&index=1)
[[2]](https://www.youtube.com/watch?v=mvZKu0DfFLQ)
[[3]](https://www.youtube.com/watch?v=zOpzGHwJ3MU)
[[4]](https://www.youtube.com/watch?v=ldJ8WGZVXZk)

Threads
[[1]](https://man7.org/linux/man-pages/man7/pthreads.7.html)
[[2]](https://pubs.opengroup.org/onlinepubs/7908799/xsh/pthread.h.html)
[[3]](https://www.geeksforgeeks.org/c/thread-functions-in-c-c/)
[[4]](https://blog.gtwang.org/programming/pthread-multithreading-programming-in-c-tutorial/)
[[5]](https://tigercosmos.xyz/en/post/2020/07/simple-pthread-usage/)
[[6]](https://www.codequoi.com/en/threads-mutexes-and-concurrent-programming-in-c/)

Guide
[[1]](https://medium.com/@ruinadd/philosophers-42-guide-the-dining-philosophers-problem-893a24bc0fe2)
[[2]](https://medium.com/@jalal92/the-dining-philosophers-7157cc05315)
[[3]](https://suspectedoceano.notion.site/Philosophers-b1bf3c57eee6420cafa7d0900b3d3216)

Heap
[[1]](https://www.geeksforgeeks.org/c/heap-in-c/)

## AI Usage
AI is used in this project:
- build my foundation knowledge for threads and mutexes concepts
- confirm and correct my understanding to the new concepts
- explain when i don't understand something
- guide me through step by step
- debug and check for error handling
