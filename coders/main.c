/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 08:30:26 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/18 04:46:37 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

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
	if (pthread_mutex_init(&args.message_mutex, NULL) != 0)
	{
		printf("Error: Failed to initialize message mutex.\n");
		free(coders);
		free(dongles);
		return (1);
	}
	args.start_time = get_time_in_ms();
	i = 0;
	while (i < args.nb_coders)
	{
		if (pthread_create(&coders[i].thread, NULL, cycle, &coders[i]) != 0)
		{
			printf("Error: Failed to create thread %d.\n", coders[i].id);
			return (1);
		}
		i++;
	}
	run_monitor(coders);
	i = 0;
	while (i < args.nb_coders)
	{
		if (pthread_join(coders[i].thread, NULL) != 0)
		{
			printf("Error: Failed to join thread %d.\n", coders[i].id);
			return (1);
		}
		i++;
	}
	printf("%ld\n", args.start_time);
	printf("success :)\n");
	pthread_mutex_destroy(&args.message_mutex);
	free(coders);
	free(dongles);
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
