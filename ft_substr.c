/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/23 14:08:02 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/24 11:48:02 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	s_len;
	size_t	end;
	char	*sub;

	if (!s)
		return (NULL);
	s_len = ft_strlen(s);
	end = len;
	if (start >= s_len)
		return ((char *)ft_calloc(1, 1));
	else if (len > s_len - start)
		end = s_len - start;
	sub = (char *)malloc(sizeof(char) * (end + 1));
	if (!sub)
		return (NULL);
	ft_strlcpy(sub, s + start, end + 1);
	return (sub);
}
