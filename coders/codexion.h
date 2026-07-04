/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 08:31:13 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/03 18:37:20 by wcheung        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <stdio.h>
# include <unistd.h>
# include <pthread.h>
# include <string.h>
# include <stdlib.h>

typedef struct s_arg
{
	int nb_coders;
	int time_to_burnout;
	int time_to_compile;
	int time_to_debug;
	int time_to_refactor;
	int nb_compiles_required;
	int dongle_cooldown;
	int scheduler;              // 0 for fifo, 1 for edf
}           t_arg;

t_arg    *parse_argv(int argc, char ** argv);

#endif

