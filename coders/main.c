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
	t_arg *args;

	args = parse_argv(argc, argv);
	if (args == NULL)
		return (1);
	free(args);
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
