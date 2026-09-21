/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   k_sort.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/18 15:04:20 by wcheung           #+#    #+#             */
/*   Updated: 2026/01/20 12:50:12 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	chunk_size(int size)
{
	if (size <= 100)
		return (15);
	else if (size <= 500)
		return (33);
	return (size / 15);
}

static void	k_sort_chunks(t_node **a, t_node **b, int size)
{
	int	chunk;
	int	i;
	int	range;

	chunk = chunk_size(size);
	i = 0;
	while (*a)
	{
		range = i + chunk;
		if ((*a)->index <= i)
		{
			pb(a, b);
			rb(b);
			i++;
		}
		else if ((*a)->index <= range)
		{
			pb(a, b);
			i++;
		}
		else
			ra(a);
	}
}

static int	find_max_index(t_node **b, int b_size)
{
	t_node	*current;
	int		max_index;

	current = *b;
	max_index = 0;
	while (current && current->index != (b_size - 1))
	{
		max_index++;
		current = current->next;
	}
	return (max_index);
}

static void	refine_chunks(t_node **a, t_node **b)
{
	int		b_size;
	int		max_index;

	while (*b)
	{
		b_size = stack_size(*b);
		max_index = find_max_index(b, b_size);
		if (max_index <= b_size / 2)
		{
			while ((*b)->index != (b_size - 1))
				rb(b);
		}
		else
		{
			while ((*b)->index != (b_size - 1))
				rrb(b);
		}
		pa(a, b);
	}
}

void	k_sort(t_node **a, t_node **b, int size)
{
	k_sort_chunks(a, b, size);
	refine_chunks(a, b);
}

// push int from a to b in roughly sorted chunks
// +/- k is the range of the correct position = k_sort
// need chunk size
// rotate stack a when int is too big for current chunk
// in many algorithms, most efficient way: divide a set by its square root
// for push swap, sqaure root x 1.5: lowest move count
// ra when int is too big
// pb when int is in the bigger half
// pb rb when int is in the smaller half in chunk

// stack a:
// [3] 4
// [6] 7
// [0] 1
// [5] 6
// [8] 9
// [2] 3
// [1] 2
// [4] 5
// [7] 8

// chunk = 3
// i = 3
// range = i + chunk

// stack a:	b:
// [7] 8
// [8] 9
// 			[5] 6
// 			[3] 4
// 			[0] 1
// 			[2] 3
// 			[1] 2
// 			[4] 5
// 			[6] 7

// i=0 range = 3 [3] 4 pb
// i=1 range = 4 [6] 7 ra
// i=2 range = 5 [0] 1 pb rb
// i=3 range = 6 [5] 6 pb
// i=4 range = 7 [8] 9 ra
// pb rb
// pb rb
// pb rb
// pb

// max index = size -1 = 8
