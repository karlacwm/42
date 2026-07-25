NAME = codexion
CC = cc
CFLAG = -Wall -Wextra -Werror -pthread
RM = rm -f

SRC = main.c utils.c cycle.c queue.c dongles.c monitor.c \
	mutex_utils.c parser1_parse.c parser2_store.c

OBJ = ${SRC:%.c=%.o}

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAG) -o $(NAME) $(OBJ)

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
