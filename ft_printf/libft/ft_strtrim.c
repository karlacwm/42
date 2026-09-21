/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/23 19:23:26 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/29 15:15:23 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strtrim(char const *s1, char const *set)
{
	char	*trimmed;
	size_t	trimmed_len;
	size_t	start;
	size_t	end;

	if (!s1 || !set)
		return (NULL);
	start = 0;
	end = ft_strlen(s1);
	while (s1[start] && ft_strchr(set, s1[start]))
		start++;
	while (end > start && ft_strchr(set, s1[end - 1]))
		end--;
	trimmed_len = end - start;
	trimmed = (char *)malloc(sizeof(char) * (trimmed_len +1));
	if (!trimmed)
		return (NULL);
	ft_memcpy(trimmed, s1 + start, trimmed_len);
	trimmed[trimmed_len] = '\0';
	return (trimmed);
}
// #include <stdio.h>

// int	main(void)
// {
// 	char a[] = "abaBBBaaa";
// 	char b[] = "aba";
// 	printf("ft_strtrim: %s", ft_strtrim(a, b));
// }
