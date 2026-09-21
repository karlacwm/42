/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/14 17:04:47 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/26 13:16:28 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dst, const void *src, size_t n)
{
	unsigned char		*temp_dst;
	unsigned const char	*temp_src;

	if (!dst && !src)
		return (NULL);
	temp_dst = (unsigned char *)dst;
	temp_src = (unsigned const char *)src;
	while (n > 0)
	{
		*temp_dst++ = *temp_src++;
		n--;
	}
	return (dst);
}
// int	main(void)
// {
// 	char	a[] = "000000";
// 	char	b[] = "123456";
// 	char	c[] = "abcdef";
// 	ft_memcpy(b, a, 3);
// 	printf("ft_memcpy: %s\n", b);
// 	memcpy(c, a, 3);
// 	printf("memcpy: %s\n", c);
// }
