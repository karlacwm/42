/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/31 09:10:30 by wcheung           #+#    #+#             */
/*   Updated: 2025/11/06 12:35:38 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"
#include <stdio.h> // for comparison

int	main(void)
{
	int				my_count;
	int				printf_count;
	unsigned int	unsigned_num;

	unsigned num = -999;
	my_count = ft_printf("%\n");
	printf("\n");
	printf_count = printf("%\n");
	printf("\n\n\n");
	printf("returnvalue ft_printf: %d | printf: %d\n\n", my_count, printf_count);

	return (0);
}

