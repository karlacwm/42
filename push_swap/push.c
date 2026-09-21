/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/09 19:57:28 by wcheung           #+#    #+#             */
/*   Updated: 2026/01/20 12:54:19 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// pa (push a): Take the first element at the top of b, put it at the top of a.
// Do nothing if b is empty.
// pb (push b): Take the first element at the top of a, put it at the top of b.
// Do nothing if a is empty.

#include "push_swap.h"

// static void	push(t_node **from_stack, t_node **to_stack)
// {
// 	t_node	*to_be_pushed;

// 	if (!from_stack || !to_stack)
// 		return ;
// 	to_be_pushed = *from_stack;
// 	(*from_stack)->prev = NULL;
// 	*from_stack = (*from_stack)->next;
// 	to_be_pushed->next = *to_stack;
// 	to_be_pushed->prev = NULL;
// 	*to_stack = to_be_pushed;
// }

static void	push(t_node **from_stack, t_node **to_stack)
{
	t_node	*to_be_pushed;

	if (!from_stack || !to_stack)
		return ;
	to_be_pushed = *from_stack;
	*from_stack = to_be_pushed->next;
	if (*from_stack)
		(*from_stack)->prev = NULL;
	to_be_pushed->next = *to_stack;
	if (*to_stack)
		(*to_stack)->prev = to_be_pushed;
	*to_stack = to_be_pushed;
	to_be_pushed->prev = NULL;
}

void	pa(t_node **a, t_node **b)
{
	push(b, a);
	write(1, "pa\n", 3);
}

void	pb(t_node **a, t_node **b)
{
	push(a, b);
	write(1, "pb\n", 3);
}
