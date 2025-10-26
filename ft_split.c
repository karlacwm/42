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

int	ft_locate_word(char const *str, char c, int *word_start, int *word_end)
{
	while (str[*word_end] && str[*word_end] == c)
		(*word_end)++;
	*word_start = *word_end;
	while (str[*word_end] && str[*word_end] != c)
		(*word_end)++;
	return (*word_end > *word_start);
}

char	*ft_copy_word(char const *str, size_t word_start, size_t word_end)
{
	char	*word;
	size_t	letter;

	word = (char *)malloc(sizeof(char) * (word_end - word_start + 1));
	if (!word)
		return (NULL);
	letter = 0;
	while (word_start + letter < word_end)
	{
		word[letter] = str[word_start + letter];
		letter++;
	}
	word[letter] = '\0';
	return (word);	
}

void	ft_free_all(char **split_str, size_t i)
{
	while (i > 0)
		free(split_str[--i]);
	free(split_str);
}

char	**ft_split(char const *str, char c)
{
	char	**split_str;
	int		word_start;
	int		word_end;
	int		i;

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
		if (ft_locate_word(str, c, &word_start, &word_end))
		{
			split_str[i] = ft_copy_word(str, word_start, word_end);
			if (!split_str[i])
			{
				ft_free_all(split_str, i);
				return (NULL);
			}
			i++;
		}
	}
	split_str[i] = NULL;
	return (split_str);
}

#include <stdio.h>

// // check word count
// int	main(void)
// {
// 	char	a[] = "a)a";
// 	char	c;

// 	c = 'a';
// 	printf("%d", ft_word_count(a, c));
// }

// // check split
int	main(void)
{
	char	a[] = "      split       this for   me  !       ";
	char	c = 32;
	char	**result;
	int		i = 0;

	result = ft_split(a, c);
	while (result[i])
	{
		printf("%s\n", result[i++]);
	}
}
