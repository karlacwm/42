/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 15:48:32 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/23 18:17:59 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	dst_len;
	size_t	src_len;
	size_t	i;

	dst_len = 0;
	while (dst[dst_len] && dst_len < size)
		dst_len++;
	i = 0;
	src_len = ft_strlen(src);
	if (size == 0)
		return (src_len);
	if (size <= dst_len)
		return (size + src_len);
	while (i < size - dst_len - 1 && src[i])
	{
		dst[dst_len + i] = src[i];
		i++;
	}
	dst[dst_len + i] = '\0';
	return (dst_len + src_len);
}
// size refers to the total size of the dst buffer
// check if size == 0 before running ft_strlen on dest
// #include <stdio.h>

// int	main(void)
// {
// 	char	a[13] = "banana banana";
// 	char	b[] = "nanana";
// 	unsigned int	x = 13;
// 	printf("ft_strlcat = %zu\n", ft_strlcat(a, b, x));
// 	printf("result = %s", a);
// 	return (0);
// }
