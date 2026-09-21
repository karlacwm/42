/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/14 16:29:49 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/18 19:35:02 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_bzero(void *str, size_t n)
{
	unsigned char	*temp;

	temp = str;
	while (n > 0)
	{
		*temp = '\0';
		temp++;
		n--;
	}
}
// to modify the memory block, no need to return anything
