/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/25 12:25:32 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/25 19:28:24 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_word_count(char const *str, char c)
{
	int	word_count;

	word_count = 0;
	while (*str)
	{
		while (*str == c)
			str++;
		if (*str != '\0')
		{
			word_count++;
			while (*str && *str != c)
				str++;
		}
	}
	return (word_count);
}

char	**ft_split(char const *str, char c)
{
	char	**split_str;
	int		word_start;
	int		word_end;
	int		i;
	int		letter;

	if (!str)
		return (NULL);
	split_str = (char **)malloc(sizeof(char *) * (ft_word_count(str, c) + 1));
	if (!split_str)
		return (NULL);
	split_str[ft_word_count(str, c)] = (void *)'\0';
	word_start = 0;
	word_end = 0;
	i = 0;
	while (str[word_end])
	{
		while (str[word_end] && str[word_end] == c)
			word_end++;
		word_start = word_end;
		while (str[word_end] && str[word_end] != c)
			word_end++;
		if (word_end > word_start)
		{
			split_str[i] = (char *)malloc(sizeof(char) * (word_end - word_start
						+ 1));
			if (!split_str[i])
			{
				while (i > 0)
					free(split_str[--i]);
				free(split_str);
				return (NULL);
			}
			letter = 0;
			while (word_start + letter < word_end)
			{
				split_str[i][letter] = str[word_start + letter];
				letter++;
			}
			split_str[i][letter] = '\0';
			i++;
		}
	}
	return (split_str);
}

// #include <stdio.h>

// // check word count
// int	main(void)
// {
// 	char	a[] = "a)a";
// 	char	c;

// 	c = 'a';
// 	printf("%d", ft_word_count(a, c));
// }

// // check split
// int	main(void)
// {
// 	char	a[] = "      split       this for   me  !       ";
// 	char	c;
// 	char	**result;
// 	int		i;

// 	c = 32;
// 	i = 0;
// 	result = ft_split(a, c);
// 	while (result[i])
// 	{
// 		printf("%s\n", result[i++]);
// 	}
// }
