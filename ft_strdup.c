/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 23:48:35 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/23 12:32:07 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *str)
{
	char	*copy;

	copy = (char *)malloc((ft_strlen(str) + 1));
	if (!copy)
		return (NULL);
	ft_memcpy(copy, str, (ft_strlen(str) + 1));
	return (copy);
}

	// size_t	i;

	// i = 0;
	// while (str[i])
	// {
	// 	copy[i] = str[i];
	// 	i++;
	// }
	// copy[i] = 0;
