/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/17 01:05:53 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/21 20:15:44 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	decide_who_first(t_request a, t_request b, int scheduler)
{
	if (scheduler == 0)
		return (a.arrival_time < b.arrival_time);
	return (a.deadline < b.deadline);
}

void	join_heap_q(t_heap *heap, t_request new_req)
{
	int			current;
	int			parent;
	t_request	temp;

	current = heap->size;
	heap->requests[current] = new_req;
	heap->size++;
	while (current > 0)
	{
		parent = (current - 1) / 2;
		if (decide_who_first(heap->requests[current],
				heap->requests[parent], heap->scheduler))
		{
			temp = heap->requests[current];
			heap->requests[current] = heap->requests[parent];
			heap->requests[parent] = temp;
			current = parent;
		}
		else
		{
			break ;
		}
	}
}

static int	actual_work(t_heap *heap, int current)
{
	t_request	temp;
	int			left;
	int			right;
	int			most_urgent;

	while (1)
	{
		most_urgent = current;
		left = (2 * current) + 1;
		right = (2 * current) + 2;
		if (left < heap->size && decide_who_first(heap->requests[left],
				heap->requests[most_urgent], heap->scheduler))
			most_urgent = left;
		if (right < heap->size && decide_who_first(heap->requests[right],
				heap->requests[most_urgent], heap->scheduler))
			most_urgent = right;
		if (most_urgent == current)
			return (-1);
		temp = heap->requests[current];
		heap->requests[current] = heap->requests[most_urgent];
		heap->requests[most_urgent] = temp;
		current = most_urgent;
	}
	return (current);
}

t_request	take_out_top_and_replace(t_heap *heap)
{
	t_request	top;
	int			current;

	current = 0;
	top = heap->requests[0];
	heap->size--;
	if (heap->size == 0)
		return (top);
	heap->requests[0] = heap->requests[heap->size];
	current = 0;
	while (current != -1)
	{
		current = actual_work(heap, current);
	}
	return (top);
}

// heap is a specialized array,
// where most important item always bubbles up to index 0
// heap is presented with binary tree
// Left Child: L(i) = 2i + 1
// Right Child: R(i) = 2i + 2
// Parent: P(i) = (i-1)/2
//
// when coder wants to compile, goes to queue
// new coder always put to end of queue
// compare with parent, depends on fifo/edf, swap = push
// compare and swap (bubble sort) until parent is more urgent = sorted
// put index 0 coder to end of queue = pop
