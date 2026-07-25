/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   mutex_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/21 23:38:14 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/25 02:44:25 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_dongles(t_arg *args, t_dongle *dongles)
{
	int	i;

	i = 0;
	while (i < args->nb_coders)
	{
		dongles[i].id = i;
		dongles[i].available_when = 0;
		if (pthread_mutex_init(&dongles[i].mutex, NULL) != 0)
			return (1);
		i++;
	}
	return (0);
}

static void	init_coders(t_arg *args, t_coder *coders, t_dongle *dongles)
{
	int	i;

	i = 0;
	while (i < args->nb_coders)
	{
		coders[i].id = i + 1;
		coders[i].nb_compiles = 0;
		coders[i].last_compile_time = 0;
		coders[i].args = args;
		coders[i].left_dongle = &dongles[i];
		coders[i].right_dongle = &dongles[(i + 1) % args->nb_coders];
		i++;
	}
}

int	init_data(t_arg *args, t_coder **coders, t_dongle **dongles)
{
	*dongles = malloc(sizeof(t_dongle) * args->nb_coders);
	if (!*dongles)
		return (1);
	*coders = malloc(sizeof(t_coder) * args->nb_coders);
	if (!*coders)
	{
		free(*dongles);
		return (1);
	}
	if (init_dongles(args, *dongles))
	{
		free(*coders);
		free(*dongles);
		return (1);
	}
	init_coders(args, *coders, *dongles);
	return (0);
}

static int	mutex_handle(t_arg *args)
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
	args->ready_coders = 0;
	args->start_ready = 0;
	args->queue.requests = malloc(sizeof(t_request) * args->nb_coders);
	if (!args->queue.requests)
		return (1);
	if (mutex_handle(args))
		return (free(args->queue.requests), 1);
	return (0);
}
