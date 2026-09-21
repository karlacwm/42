/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 08:30:26 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/25 02:09:17 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	start_threads(t_arg *args, t_coder *coders)
{
	int	i;

	i = 0;
	while (i < args->nb_coders)
	{
		if (pthread_create(&coders[i].thread, NULL, cycle, &coders[i]) != 0)
			break ;
		i++;
	}
	return (i);
}

static int	join_threads(t_arg *args, t_coder *coders, t_dongle *dongles)
{
	int	i;

	i = 0;
	while (i < args->nb_coders)
	{
		if (pthread_join(coders[i].thread, NULL) != 0)
			return (cleanup_simulation(args, coders, dongles), 1);
		i++;
	}
	return (0);
}

static void	init_simulation(t_arg *args, t_coder *coders,
		t_dongle *dongles)
{
	int	i;

	args->burnout_yet = 1;
	args->start_time = get_time_in_ms();
	i = 0;
	while (i < args->nb_coders)
	{
		coders[i].last_compile_time = args->start_time;
		dongles[i].available_when = args->start_time;
		i++;
	}
}

static int	handle_thread_error(t_arg *args, t_coder *coders,
		t_dongle *dongles, int created)
{
	pthread_mutex_lock(&args->queue_mutex);
	pthread_mutex_lock(&args->coding_mutex);
	args->burnout_yet = 0;
	pthread_mutex_unlock(&args->coding_mutex);
	pthread_cond_broadcast(&args->queue_cond);
	pthread_mutex_unlock(&args->queue_mutex);
	while (created-- > 0)
		pthread_join(coders[created].thread, NULL);
	cleanup_simulation(args, coders, dongles);
	return (1);
}

int	main(int argc, char **argv)
{
	t_arg		args;
	t_coder		*coders;
	t_dongle	*dongles;
	int			created;

	if (parse_argv(argc, argv, &args))
		return (1);
	if (init_data(&args, &coders, &dongles))
		return (1);
	if (mutex_init(&args))
		return (free(coders), free(dongles), 1);
	init_simulation(&args, coders, dongles);
	created = start_threads(&args, coders);
	if (created != args.nb_coders)
		return (handle_thread_error(&args, coders, dongles, created));
	monitor_check(coders);
	if (join_threads(&args, coders, dongles))
		return (1);
	cleanup_simulation(&args, coders, dongles);
	return (0);
}
