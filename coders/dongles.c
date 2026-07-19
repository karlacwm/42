/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongles.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/17 02:20:16 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/19 23:27:25 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	request_dongles(t_coder *coder)
{
	t_request	polite_request;

	polite_request.coder_id = coder->id;
	polite_request.arrival_time = get_time_in_ms();
	polite_request.deadline = coder->last_compile_time
		+ coder->args->time_to_burnout;
	pthread_mutex_lock(&coder->args->queue_mutex);
	join_heap_q(&coder->args->queue, polite_request);
	while (1)
	{
		if (check_burnout_or_coding(coder->args) == 0)
        {
            pthread_mutex_unlock(&coder->args->queue_mutex);
            return (0); // Return 0 to tell the cycle to abort!
        }

		if (coder->args->queue.requests[0].coder_id == coder->id)
		{
			if (get_time_in_ms() >= coder->left_dongle->available_when
				&& get_time_in_ms() >= coder->right_dongle->available_when)
			{
				pthread_mutex_lock(&coder->left_dongle->mutex);
				pthread_mutex_lock(&coder->right_dongle->mutex);
				take_out_top_and_replace(&coder->args->queue);
				break ;
			}
		}
		pthread_cond_wait(&coder->args->queue_cond, &coder->args->queue_mutex);
	}
	pthread_mutex_unlock(&coder->args->queue_mutex);
	return (1);
}

void	release_dongles(t_coder *coder)
{
	long	current_time;

	pthread_mutex_lock(&coder->args->queue_mutex);
	current_time = get_time_in_ms();
	coder->left_dongle->available_when = current_time + coder->args->dongle_cooldown;
	coder->right_dongle->available_when = current_time + coder->args->dongle_cooldown;
	pthread_mutex_unlock(&coder->left_dongle->mutex);
	pthread_mutex_unlock(&coder->right_dongle->mutex);
	pthread_cond_broadcast(&coder->args->queue_cond);
	pthread_mutex_unlock(&coder->args->queue_mutex);
}
