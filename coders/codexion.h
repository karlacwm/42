/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 08:31:13 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/14 21:53:47 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <stdio.h>
# include <unistd.h>
# include <pthread.h>
# include <string.h>
# include <stdlib.h>
# include <sys/time.h>

typedef struct s_arg
{
	int		nb_coders;
	int		time_to_burnout;
	int		time_to_compile;
	int		time_to_debug;
	int		time_to_refactor;
	int		nb_compiles_required;
	int		dongle_cooldown;
	int		scheduler; // 0 for fifo, 1 for edf
	long	start_time;
}		t_arg;

typedef struct s_dongle
{
	int				id;
	// int occupied;
	long			cooldown_until; // handles dongle_cooldown
	pthread_mutex_t	mutex; // protects this dongle from race conditions
}		t_dongle;

typedef struct s_coder
{
	int			id;
	int			nb_compiles;
	long		last_compile_time; // used to calculate burnout
	pthread_t	thread; // thread for this coder
	t_arg		*args; // pointer to the arguments struct
	t_dongle	*left_dongle;
	t_dongle	*right_dongle;
}		t_coder;

int		parse_argv(int argc, char **argv, t_arg *args);
int		init_data(t_arg *args, t_coder **coders, t_dongle **dongles);
void	*cycle(void *arg);
long	get_time_in_ms(void);

#endif
