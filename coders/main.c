/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 08:30:26 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/20 00:31:58 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_runtime_sync(t_arg *args)
{
	args->queue.size = 0;
	args->queue.capacity = args->nb_coders;
	args->queue.scheduler = args->scheduler;
	args->queue.requests = malloc(sizeof(t_request) * args->nb_coders);
	if (!args->queue.requests)
		return (1);
	if (pthread_mutex_init(&args->coding_mutex, NULL) != 0)
		return (free(args->queue.requests), 1);
	if (pthread_mutex_init(&args->message_mutex, NULL) != 0)
	{
		pthread_mutex_destroy(&args->coding_mutex);
		return (free(args->queue.requests), 1);
	}
	if (pthread_mutex_init(&args->queue_mutex, NULL) != 0)
	{
		pthread_mutex_destroy(&args->coding_mutex);
		pthread_mutex_destroy(&args->message_mutex);
		return (free(args->queue.requests), 1);
	}
	if (pthread_cond_init(&args->queue_cond, NULL) != 0)
	{
		pthread_mutex_destroy(&args->coding_mutex);
		pthread_mutex_destroy(&args->message_mutex);
		pthread_mutex_destroy(&args->queue_mutex);
		return (free(args->queue.requests), 1);
	}
	return (0);
}

int	main(int argc, char **argv)
{
	t_arg		args;
	t_coder		*coders;
	t_dongle	*dongles;
	int			i;

	if (parse_argv(argc, argv, &args) == 1)
		return (1);
	if (init_data(&args, &coders, &dongles) == 1)
		return (1);
	if (init_runtime_sync(&args) == 1)
	{
		printf("Error: Failed to initialize runtime synchronization.\n");
		free(coders);
		free(dongles);
		return (1);
	}
	args.burnout_yet = 1;
	args.start_time = get_time_in_ms();
	i = 0;
	while (i < args.nb_coders)
	{
		coders[i].last_compile_time = args.start_time;
		dongles[i].available_when = args.start_time;
		if (pthread_create(&coders[i].thread, NULL, cycle, &coders[i]) != 0)
			break ;
		i++;
	}
	if (i != args.nb_coders)
	{
		pthread_mutex_lock(&args.coding_mutex);
		args.burnout_yet = 0;
		pthread_mutex_unlock(&args.coding_mutex);
		pthread_cond_broadcast(&args.queue_cond);
		while (i-- > 0)
			pthread_join(coders[i].thread, NULL);
		cleanup_simulation(&args, coders, dongles);
		printf("Error: Failed to create all coder threads.\n");
		return (1);
	}
	monitor_check(coders);
	i = 0;
	while (i < args.nb_coders)
	{
		if (pthread_join(coders[i].thread, NULL) != 0)
			return (cleanup_simulation(&args, coders, dongles), 1);
		i++;
	}
	cleanup_simulation(&args, coders, dongles);
	return (0);
}

//

// --------learning about threads----------
// void	*routine(void)
// {
// 	printf("start\n");
// 	sleep(2);
// 	printf("end\n");
// 	return (NULL);
// }

// int	main(int argc, char **argv)
// {
// 	pthread_t	t1;
// 	pthread_t	t2;

// 	pthread_create(&t1, NULL, (void *)&routine, NULL);
// 	pthread_create(&t2, NULL, (void *)&routine, NULL);
// 	pthread_join(t1, NULL);
// 	pthread_join(t2, NULL);
// 	return (0);
// }
