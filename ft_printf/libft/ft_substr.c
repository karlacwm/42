/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/23 14:08:02 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/27 10:07:13 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(char const *str, unsigned int start, size_t len)
{
	size_t	str_len;
	size_t	end;
	char	*sub;

	if (!str)
		return (NULL);
	str_len = ft_strlen(str);
	end = len;
	if (start >= str_len)
		return ((char *)ft_calloc(1, 1));
	else if (len > str_len - start)
		end = str_len - start;
	sub = (char *)malloc(sizeof(char) * (end + 1));
	if (!sub)
		return (NULL);
	ft_strlcpy(sub, str + start, end + 1);
	return (sub);
}
// #include <stdio.h>

// int	main(void)
// {
// 	char a[] = "aaaBBBaaa";
// 	printf("ft_substr: %s", ft_substr(a, 3, 9));
// }
