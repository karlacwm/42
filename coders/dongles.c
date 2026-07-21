/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongles.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/17 02:20:16 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/22 00:35:12 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	init_before_request(t_coder *coder, t_request *req,
		t_dongle **first, t_dongle **second)
{
	long	last_compile_time;

	req->coder_id = coder->id;
	req->arrival_time = get_time_in_ms();
	pthread_mutex_lock(&coder->args->coding_mutex);
	last_compile_time = coder->last_compile_time;
	pthread_mutex_unlock(&coder->args->coding_mutex);
	req->deadline = last_compile_time + coder->args->time_to_burnout;
	*first = coder->left_dongle;
	*second = coder->right_dongle;
	if (*first != *second && (*first)->id > (*second)->id)
	{
		*first = coder->right_dongle;
		*second = coder->left_dongle;
	}
}

static int	try_take_dongles(t_coder *coder, t_dongle *first,
		t_dongle *second)
{
	int	same;
	int	ok1;
	int	ok2;

	same = (first == second);
	ok1 = (pthread_mutex_trylock(&first->mutex) == 0);
	ok2 = same || (pthread_mutex_trylock(&second->mutex) == 0);
	if (ok1 && ok2
		&& get_time_in_ms() >= coder->left_dongle->available_when
		&& get_time_in_ms() >= coder->right_dongle->available_when)
		return (1);
	if (ok2 && !same)
		pthread_mutex_unlock(&second->mutex);
	if (ok1)
		pthread_mutex_unlock(&first->mutex);
	return (0);
}

static int	wait_for_turn(t_coder *coder, t_dongle *first,
		t_dongle *second)
{
	while (1)
	{
		if (check_burnout_or_coding(coder->args) == 0)
			return (pthread_mutex_unlock(&coder->args->queue_mutex), 0);
		if (coder->args->queue.requests[0].coder_id == coder->id)
		{
			pthread_mutex_unlock(&coder->args->queue_mutex);
			if (try_take_dongles(coder, first, second))
			{
				pthread_mutex_lock(&coder->args->queue_mutex);
				take_out_top_and_replace(&coder->args->queue);
				pthread_mutex_unlock(&coder->args->queue_mutex);
				return (1);
			}
		}
		else
			pthread_mutex_unlock(&coder->args->queue_mutex);
		usleep(500);
		pthread_mutex_lock(&coder->args->queue_mutex);
	}
}

int	request_dongles(t_coder *coder)
{
	t_request	polite_request;
	t_dongle	*first;
	t_dongle	*second;

	init_before_request(coder, &polite_request, &first, &second);
	pthread_mutex_lock(&coder->args->queue_mutex);
	join_heap_q(&coder->args->queue, polite_request);
	return (wait_for_turn(coder, first, second));
}

void	release_dongles(t_coder *coder)
{
	long		current_time;
	t_dongle	*first_dongle;
	t_dongle	*second_dongle;
	int			same_dongle;

	same_dongle = (coder->left_dongle == coder->right_dongle);
	first_dongle = coder->left_dongle;
	second_dongle = coder->right_dongle;
	if (!same_dongle && first_dongle->id > second_dongle->id)
	{
		first_dongle = coder->right_dongle;
		second_dongle = coder->left_dongle;
	}
	pthread_mutex_lock(&coder->args->queue_mutex);
	current_time = get_time_in_ms();
	coder->left_dongle->available_when = current_time
		+ coder->args->dongle_cooldown;
	coder->right_dongle->available_when = current_time
		+ coder->args->dongle_cooldown;
	if (!same_dongle)
		pthread_mutex_unlock(&second_dongle->mutex);
	pthread_mutex_unlock(&first_dongle->mutex);
	pthread_cond_broadcast(&coder->args->queue_cond);
	pthread_mutex_unlock(&coder->args->queue_mutex);
}
