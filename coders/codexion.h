/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 08:31:13 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/21 23:42:36 by wcheung          ###   ########.fr       */
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

typedef struct s_request
{
	int		coder_id;
	long	arrival_time; // Used to sort if scheduler == 0 (FIFO
	long	deadline; // Used to sort if scheduler == 1 (EDF)
}		t_request;

typedef struct s_heap
{
	t_request	*requests;
	int			size;
	int			capacity;
	int			scheduler; // 0 for FIFO, 1 for EDF
}		t_heap;

typedef struct s_arg
{
	int				nb_coders;
	int				time_to_burnout;
	int				time_to_compile;
	int				time_to_debug;
	int				time_to_refactor;
	int				nb_compiles_required;
	int				dongle_cooldown;
	int				scheduler; // 0 for fifo, 1 for edf
	long			start_time;
	int				burnout_yet; // 0 for burnout, 1 for coding
	pthread_mutex_t	coding_mutex;
	pthread_mutex_t	message_mutex;
	t_heap			queue;
	pthread_mutex_t	queue_mutex;
	pthread_cond_t	queue_cond;
}		t_arg;

typedef struct s_dongle
{
	int				id;
	long			available_when;
	pthread_mutex_t	mutex;
}		t_dongle;

typedef struct s_coder
{
	int			id;
	int			nb_compiles;
	long		last_compile_time;
	pthread_t	thread;
	t_arg		*args;
	t_dongle	*left_dongle;
	t_dongle	*right_dongle;
}		t_coder;

int			parse_argv(int argc, char **argv, t_arg *args);
int			init_data(t_arg *args, t_coder **coders, t_dongle **dongles);
void		*cycle(void *arg);
long		get_time_in_ms(void);
void		usleep_in_ms(long time_to_sleep_in_ms);
void		log_message(t_coder *coder, char *status);
void		join_heap_q(t_heap *heap, t_request new_req);
t_request	take_out_top_and_replace(t_heap *heap);
int			request_dongles(t_coder *coder);
void		release_dongles(t_coder *coder);
int			check_burnout_or_coding(t_arg *args);
void		monitor_check(t_coder *coders);
void		cleanup_simulation(t_arg *args, t_coder *coders, t_dongle *dongles);
int			mutex_handle(t_arg *args);
int			mutex_init(t_arg *args);

#endif
