
*This project has been created as part of the 42 curriculum by **``` lde-krui ```**.*

# Push Swap

## 📌 Description

**Push Swap** is an algorithmic sorting project whose goal is to sort a stack of integers using a very limited set of operations, while producing the **smallest number of moves possible**.

You are given two stacks:
- **Stack A** (initially filled with random integers, without duplicates)
- **Stack B** (initially empty)

The challenge is to use a restricted set of instructions to sort **Stack A in ascending order**, using **Stack B as auxiliary storage**, and to do so as efficiently as possible.

This project is designed to deepen understanding of:
- Sorting algorithms
- Optimization strategies
- Stack data structures
- Time and space complexity

### Allowed operations:

| Operation	| Description 							|
|----------	|---------------------------------------|
| `sa` 		| swap the first 2 elements of stack A	|
| `sb` 		| swap the first 2 elements of stack B	|
| `ss` 		| `sa` and `sb` at the same time		|
| `pa` 		| push the top of B to A				|
| `pb` 		| push the top of A to B				|
| `ra` 		| rotate A up by one					|
| `rb` 		| rotate B up by one					|
| `rr` 		| `ra` and `rb` at the same time		|
| `rra` 	| reverse rotate A						|
| `rrb` 	| reverse rotate B						|
| `rrr` 	| `rra` and `rrb` at the same time		|

---

## Instructions

Reading the Markdown file (if in VSCODE)
- click somewhere in the Markdown file
- use the command: ``` CTL + SHIFT + V ```

After cloning
1. make
2. make clean
3. go to the PushSwap visualizer : [here](https://push.eliotlucas.ch/)
4. change the number of numbers to be generated
5. hit load
6. hit copy (under comman to execute similar to : ./push_swap 30 etc.)
7. run the command
8. retrieve the results from the generated log.txt file,
9. paste it back in the visualizer under "Operations (one per line)"
10. hit start

If you want to check inside the code you can use the following function:
```c
void	print_stack(t_stack *stack)
{
	while (stack != NULL)
	{
		ft_printf("%d, lis_size %d, in_lis %d, c %p n %p, p %p\n", stack->value, stack->lis_size, stack->in_lis, stack, stack->next, stack->prev);
		stack = stack->next;
	}
}
```

Bonus : test your PushSwap checker with the linux PushSwap-checker
1. download the linux checker from the 42 project page
2. ``` ./push_swap 5 2 1 4 3 | ./checker 5 2 1 4 3 ```
3. If the operation is sucessful the terminal will display ``` OK ``` else ``` KO ``` , or nothing if no input is given

• For maximum project validation (100%) and eligibility for bonuses, you must:

	◦ Sort 100 random numbers in fewer than 700 operations.
	◦ Sort 500 random numbers in no more than 5500 operations.

---

## ▶️ Resources - What I used to complete the project

- AI was used to create the description part of the README.md file
- Video from Thuggonaut [here](https://www.google.com/search?q=push+swap+K+strategy&oq=push+swap+K+strategy&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQIRigAdIBCTg5MzZqMGoxNagCCLACAfEFtdGDFZmhXyU&sourceid=chrome&ie=UTF-8#fpstate=ive&vld=cid:fb33a2cb,vid:wRvipSG4Mmk,st:0)
- Video from Oceano [here](https://www.youtube.com/watch?v=OaG81sDEpVk)
- The strategy used is K-distribution sort from Sylvain Maitre 's guide [here](https://medium.com/@brakebein42/k-distribution-sort-applied-to-the-push-swap-problem-ae2d96d68376)
- The visualizer from Eliot Lucas : [here](https://push.eliotlucas.ch/)
- Special thank you to the students I was able to evaluate or ask for help at 42 Heilbronn for the different strategies
- AI helped me filtering the different strategies
- AI was used to understand k-sort and turc sort at a deeper level
- good reminder for linked list is the CodeVault series [here](https://www.youtube.com/watch?v=29OANTQ826Y)

Here are a few strategies to consider for this project (only k-sort & turc-sort was used here):
- k-sort
- turn-sort
- lis
- greed
- turk-sort

! some implemented 2 strategies, e.g.
* Turk-sort strategy for 100 random numbers
* K-sort strategy for 500 random numbers
