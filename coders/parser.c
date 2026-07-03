#include "codexion.h"

int check_argv(int argc, char ** argv)
{
    if (argc != 9)
	{
		printf("Parsing error - invalid number of arguments.\n");
		return (1);
	}
    
}




// "Try again with: ./codexion <no_of_coders> <time_to_burnout> "
// 			"<time_to_compile> <time_to_debug> <time_to_refactor> "
// 			"<no_of_compiles_required> <dongle_cooldown> <scheduler>\n"