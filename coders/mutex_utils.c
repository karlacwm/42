/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mutex_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/21 23:38:14 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/21 23:38:29 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	mutex_handle(t_arg *args)
{
	if (pthread_mutex_init(&args->coding_mutex, NULL) != 0)
		return (1);
	if (pthread_mutex_init(&args->message_mutex, NULL) != 0)
		return (pthread_mutex_destroy(&args->coding_mutex), 1);
	if (pthread_mutex_init(&args->queue_mutex, NULL) != 0)
	{
		pthread_mutex_destroy(&args->coding_mutex);
		pthread_mutex_destroy(&args->message_mutex);
		return (1);
	}
	if (pthread_cond_init(&args->queue_cond, NULL) != 0)
	{
		pthread_mutex_destroy(&args->coding_mutex);
		pthread_mutex_destroy(&args->message_mutex);
		pthread_mutex_destroy(&args->queue_mutex);
		return (1);
	}
	return (0);
}

int	mutex_init(t_arg *args)
{
	args->queue.size = 0;
	args->queue.capacity = args->nb_coders;
	args->queue.scheduler = args->scheduler;
	args->queue.requests = malloc(sizeof(t_request) * args->nb_coders);
	if (!args->queue.requests)
		return (1);
	if (mutex_handle(args))
		return (free(args->queue.requests), 1);
	return (0);
}
