/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 08:30:26 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/03 18:37:00 by wcheung        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	main(int argc, char **argv)
{
	t_arg		args;
	t_coder		*coders;
	t_dongle	*dongles;

	if (parse_argv(argc, argv, &args) == 1)
		return (1);
	if (init_data(&args, &coders, &dongles) == 1)
		return (1);
	printf("success :)\n");
	free(coders);
	free(dongles);
	return (0);
}

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
