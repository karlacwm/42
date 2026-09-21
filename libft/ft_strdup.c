/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 23:48:35 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/25 16:14:03 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *str)
{
	char	*copy;
	size_t	copy_len;

	copy_len = ft_strlen(str);
	copy = (char *)malloc(sizeof(char) * (copy_len + 1));
	if (!copy)
		return (NULL);
	ft_memcpy(copy, str, (sizeof(char) * (copy_len + 1)));
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
