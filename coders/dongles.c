/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongles.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/17 02:20:16 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/20 00:31:57 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	request_dongles(t_coder *coder)
{
	t_request	polite_request;
	int			same_dongle;
	int			left_lock_ok;
	int			right_lock_ok;

	polite_request.coder_id = coder->id;
	polite_request.arrival_time = get_time_in_ms();
	polite_request.deadline = coder->last_compile_time
		+ coder->args->time_to_burnout;
	same_dongle = (coder->left_dongle == coder->right_dongle);
	pthread_mutex_lock(&coder->args->queue_mutex);
	join_heap_q(&coder->args->queue, polite_request);
	while (1)
	{
		if (check_burnout_or_coding(coder->args) == 0)
			return (pthread_mutex_unlock(&coder->args->queue_mutex), 0);

		if (coder->args->queue.requests[0].coder_id == coder->id)
		{
			if (get_time_in_ms() >= coder->left_dongle->available_when
				&& get_time_in_ms() >= coder->right_dongle->available_when)
			{
				left_lock_ok = (pthread_mutex_trylock(&coder->left_dongle->mutex) == 0);
				right_lock_ok = 1;
				if (!same_dongle)
					right_lock_ok = (pthread_mutex_trylock(&coder->right_dongle->mutex)
							== 0);
				if (left_lock_ok && right_lock_ok)
				{
					take_out_top_and_replace(&coder->args->queue);
					break ;
				}
				if (left_lock_ok)
					pthread_mutex_unlock(&coder->left_dongle->mutex);
				if (right_lock_ok && !same_dongle)
					pthread_mutex_unlock(&coder->right_dongle->mutex);
			}
		}
		pthread_mutex_unlock(&coder->args->queue_mutex);
		usleep(500);
		pthread_mutex_lock(&coder->args->queue_mutex);
	}
	pthread_mutex_unlock(&coder->args->queue_mutex);
	return (1);
}

void	release_dongles(t_coder *coder)
{
	long	current_time;
	int		same_dongle;

	same_dongle = (coder->left_dongle == coder->right_dongle);
	pthread_mutex_lock(&coder->args->queue_mutex);
	current_time = get_time_in_ms();
	coder->left_dongle->available_when = current_time + coder->args->dongle_cooldown;
	coder->right_dongle->available_when = current_time + coder->args->dongle_cooldown;
	pthread_mutex_unlock(&coder->left_dongle->mutex);
	if (!same_dongle)
		pthread_mutex_unlock(&coder->right_dongle->mutex);
	pthread_cond_broadcast(&coder->args->queue_cond);
	pthread_mutex_unlock(&coder->args->queue_mutex);
}
