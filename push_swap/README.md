*This project has been created as part of the 42 curriculum by wcheung.*

# push_swap

# Description
Push swap is about sorting data with two stacks within limited operations with minimal move counts. The operation moves are restricted, only push, swap, rotate and reverse rotate are allowed. One challenge is to choose an algortithm for the solution. My choice is to sort with K-sort with the help of indexing.

Before sorting, the input is checked if it is in valid format. Invalid format includes non-integers, duplicates and values outside the int range. Next, numbers will be indexed by their rank, which are ranked by a bubble sort. The index of the numbers are helpful, as I can efficiently compare it and roughly sort the numbers to stack b. And lastly, to find the largest one in stack B and push it back to stack a. For under 5 numbers, the sorting is hard-coded for lowest possible moves. The logic of sort_four and sort_five are based on sort_three.

# Instructions
Compile:
make
cc -Wall -Werror -Wextra push_swap.c push_swap.a -o push_swap
./push_swap 4 2 1 5 3
./push_swap "1 5 2 3 4"
(any invalid format in input will print Error\n)

Tester:
download tester from 42 intra
chmod +x checker_linux
ARG=""
./push_swap $ARG | ~/checker_linux $ARG
(tester shows either OK or KO)

# Resources
AI was used for debugging, explaining the algorithm and explaining confusing concepts about linked lists.

Youtube playlist for linked lists:
https://youtube.com/playlist?list=PLfqABt5AS4FmXeWuuNDS3XGENJO1VYGxl&

push swap tester on GitHub:
https://github.com/gemartin99/Push-Swap-Tester/tree/master

push swap visualizer:
https://push-swap42-visualizer.vercel.app/
