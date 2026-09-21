/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 12:55:51 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/25 16:17:13 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcpy(char *dst, const char *src, size_t size)
{
	size_t	src_len;
	size_t	i;

	src_len = ft_strlen(src);
	i = 0;
	if (size > 0)
	{
		while (src[i] != '\0' && i < size - 1)
		{
			dst[i] = src[i];
			i++;
		}
		dst[i] = '\0';
	}
	return (src_len);
}

	// check?
	// if (!dst || !src)
	// 	return (0);

// #include <stdio.h>
// size_t	ft_strlen(const char *s)
// {
// 	size_t	i;

// 	i = 0;
// 	while (s[i])
// 		i++;
// 	return (i);
// }
// int	main(void)
// {
// 	char	dst[5] ;
// 	char	src [] = "appleeeee";
// 	unsigned int	x = 7;

// 	ft_strlcpy(dst, src, x);
// 	printf("new dst = %s\n", dest);
// 	printf("new dst length = %zu\n\n", strlen(dest));
// 	return (0);
// }
