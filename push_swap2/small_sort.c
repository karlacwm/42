/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   small_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/11 11:07:34 by wcheung           #+#    #+#             */
/*   Updated: 2026/01/20 13:02:32 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_two(t_node **a)
{
	int	first;
	int	second;

	first = (*a)->value;
	second = (*a)->next->value;
	if (first > second)
		sa(a);
}

void	sort_three(t_node **a)
{
	int	first;
	int	second;
	int	third;

	first = (*a)->index;
	second = (*a)->next->index;
	third = (*a)->next->next->index;
	if (first > second && first > third)
		ra(a);
	else if (second > first && second > third)
		rra(a);
	sort_two(a);
}

void	sort_four(t_node **a, t_node **b)
{
	while ((*a)->index != 0)
		ra(a);
	pb(a, b);
	sort_three(a);
	pa(a, b);
}

void	sort_five(t_node **a, t_node **b)
{
	if (find_last_node(*a)->index == 0)
		rra(a);
	while ((*a)->index != 0)
		ra(a);
	pb(a, b);
	if (find_last_node(*a)->index == 1)
		rra(a);
	while ((*a)->index != 1)
		ra(a);
	pb(a, b);
	sort_three(a);
	pa(a, b);
	pa(a, b);
}

// 3	3	2	2	1	1
// 2	1	3	1	3	2
// 1	2	1	3	2	3
// TEST: 3 5 4 2 1
