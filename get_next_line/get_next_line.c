/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/10 11:27:02 by wcheung           #+#    #+#             */
/*   Updated: 2025/11/18 09:40:42 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static char	*extract_line(char *remaining)
{
	int		i;
	char	*line;

	i = 0;
	if (!remaining || !remaining[i])
		return (NULL);
	while (remaining[i] && remaining[i] != '\n')
		i++;
	if (remaining[i] == '\n')
		i++;
	line = (char *)malloc(sizeof(char) * (i + 1));
	if (!line)
		return (NULL);
	ft_memcpy(line, remaining, i);
	line[i] = '\0';
	return (line);
}

static char	*update_remaining(char *remaining)
{
	int		i;
	char	*updated;

	if (!remaining)
		return (NULL);
	i = 0;
	while (remaining[i] && remaining[i] != '\n')
		i++;
	if (!remaining[i] || !remaining[i + 1])
	{
		free(remaining);
		return (NULL);
	}
	updated = ft_strdup(&remaining[i + 1]);
	free(remaining);
	return (updated);
}

static char	*read_n_join(int fd, char *remaining, char	*read_buffer)
{
	int	bytes_read;

	bytes_read = 1;
	while (bytes_read > 0 && (!ft_strchr(remaining, '\n')))
	{
		bytes_read = read(fd, read_buffer, BUFFER_SIZE);
		if (bytes_read < 0)
		{
			free(remaining);
			return (NULL);
		}
		read_buffer[bytes_read] = '\0';
		remaining = ft_strjoin(remaining, read_buffer);
		if (!remaining)
			return (NULL);
	}
	return (remaining);
}

static char	*get_remaining(int fd, char *remaining)
{
	char	*read_buffer;

	read_buffer = (char *)malloc(BUFFER_SIZE + 1);
	if (!read_buffer)
	{
		free(remaining);
		remaining = NULL;
		return (NULL);
	}
	remaining = read_n_join(fd, remaining, read_buffer);
	free(read_buffer);
	return (remaining);
}

char	*get_next_line(int fd)
{
	static char	*remaining;
	char		*return_line;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	remaining = get_remaining(fd, remaining);
	if (!remaining)
		return (NULL);
	if (remaining[0] == '\0')
	{
		free(remaining);
		remaining = NULL;
		return (NULL);
	}
	return_line = (extract_line(remaining));
	if (!return_line)
	{
		free(remaining);
		remaining = NULL;
		return (NULL);
	}
	remaining = update_remaining(remaining);
	return (return_line);
}

// char	*get_next_line(int fd)
// {
// 	static char	*remaining = NULL;
// 	char		*return_line;
// 	char		*read_buffer;
// 	int			bytes_read;

// 	if (fd < 0 || BUFFER_SIZE <= 0)
// 		return (NULL);
// 	read_buffer = (char *)malloc(BUFFER_SIZE + 1);
// 	if (!read_buffer)
// 	{
// 		free(remaining);
// 		remaining = NULL;
// 		return (NULL);
// 	}
// 	bytes_read = 1;
// 	while ((!ft_strchr(remaining, '\n')) && bytes_read > 0)
// 	{
// 		bytes_read = read(fd, read_buffer, BUFFER_SIZE);
// 		if (bytes_read < 0)
// 		{
// 			free(read_buffer);
// 			free(remaining);
// 			remaining = NULL;
// 			return (NULL);
// 		}
// 		read_buffer[bytes_read] = '\0';
// 		remaining = ft_strjoin(remaining, read_buffer);
// 		if (!remaining)
// 		{
// 			free(read_buffer);
// 			return (NULL);
// 		}
// 	}
// 	free(read_buffer);
// 	if (!remaining)
// 		return (NULL);
// 	if (remaining[0] == '\0')
// 	{
// 		free(remaining);
// 		remaining = NULL;
// 		return (NULL);
// 	}
// 	return_line = (extract_line(remaining));
// 	if (!return_line)
// 	{
// 		free(remaining);
// 		remaining = NULL;
// 		return (NULL);
// 	}
// 	remaining = update_remaining(remaining);
// 	return (return_line);
// }
