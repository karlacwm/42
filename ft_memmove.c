/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 11:44:54 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/26 13:17:33 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dst, const void *src, size_t n)
{
	unsigned char		*temp_dst;
	unsigned const char	*temp_src;

	if (!dst && !src)
		return (NULL);
	temp_dst = (unsigned char *)dst;
	temp_src = (unsigned const char *)src;
	if (temp_dst < temp_src)
	{
		while (n--)
			*temp_dst++ = *temp_src++;
	}
	else
	{
		temp_dst = temp_dst + n;
		temp_src = temp_src + n;
		while (n--)
			*(--temp_dst) = *(--temp_src);
	}
	return (dst);
}

// int main (void)
// {
//    char a[] = "123456789";
//    printf("ft_memmove\nbefore = %s\n", a);
//    ft_memmove(a + 2, a, 5);
//    printf("after = %s\n", a);
//    char b[] = "123456789";
//    printf("memmove\nbefore = %s\n", b);
//    memmove(b + 2, b, 5);
//    printf("after = %s", b);
//    return(0);
// }
// check pointer address
// copy from the end before data being overwritten
// memmove end to start 123456 -> 112345
// memcpy start to end 123456 -> 11111
