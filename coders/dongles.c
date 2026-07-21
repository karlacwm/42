/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongles.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/17 02:20:16 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/21 15:42:33 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	request_dongles(t_coder *coder)
{
	t_request	polite_request;
	t_dongle	*first_dongle;
	t_dongle	*second_dongle;
	long		last_compile_time;
	int			same_dongle;
	int			first_lock_ok;
	int			second_lock_ok;
	int			am_i_first;

	polite_request.coder_id = coder->id;
	polite_request.arrival_time = get_time_in_ms();
	pthread_mutex_lock(&coder->args->coding_mutex);
	last_compile_time = coder->last_compile_time;
	pthread_mutex_unlock(&coder->args->coding_mutex);
	polite_request.deadline = last_compile_time + coder->args->time_to_burnout;
	same_dongle = (coder->left_dongle == coder->right_dongle);
	first_dongle = coder->left_dongle;
	second_dongle = coder->right_dongle;
	if (!same_dongle && first_dongle->id > second_dongle->id)
	{
		first_dongle = coder->right_dongle;
		second_dongle = coder->left_dongle;
	}
	pthread_mutex_lock(&coder->args->queue_mutex);
	join_heap_q(&coder->args->queue, polite_request);
	while (1)
	{
		if (check_burnout_or_coding(coder->args) == 0)
			return (pthread_mutex_unlock(&coder->args->queue_mutex), 0);
		am_i_first = (coder->args->queue.requests[0].coder_id == coder->id);
		pthread_mutex_unlock(&coder->args->queue_mutex);
		if (am_i_first)
		{
			first_lock_ok = (pthread_mutex_trylock(&first_dongle->mutex) == 0);
			second_lock_ok = 1;
			if (!same_dongle)
				second_lock_ok = (pthread_mutex_trylock(&second_dongle->mutex)
						== 0);
			if (first_lock_ok && second_lock_ok)
			{
				if (get_time_in_ms() >= coder->left_dongle->available_when
					&& get_time_in_ms() >= coder->right_dongle->available_when)
				{
					pthread_mutex_lock(&coder->args->queue_mutex);
					take_out_top_and_replace(&coder->args->queue);
					pthread_mutex_unlock(&coder->args->queue_mutex);
					break ;
				}
				if (!same_dongle)
					pthread_mutex_unlock(&second_dongle->mutex);
				pthread_mutex_unlock(&first_dongle->mutex);
			}
			else
			{
				if (second_lock_ok && !same_dongle)
					pthread_mutex_unlock(&second_dongle->mutex);
				if (first_lock_ok)
					pthread_mutex_unlock(&first_dongle->mutex);
			}
		}
		usleep(500);
		pthread_mutex_lock(&coder->args->queue_mutex);
	}
	return (1);
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
	coder->left_dongle->available_when = current_time + coder->args->dongle_cooldown;
	coder->right_dongle->available_when = current_time + coder->args->dongle_cooldown;
	if (!same_dongle)
		pthread_mutex_unlock(&second_dongle->mutex);
	pthread_mutex_unlock(&first_dongle->mutex);
	pthread_cond_broadcast(&coder->args->queue_cond);
	pthread_mutex_unlock(&coder->args->queue_mutex);
}
