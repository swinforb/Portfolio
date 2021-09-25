/*******************************************
* Program: smallsh.c
* Assignment: #3
* Author: Ben Swinford
* Date: 2/8/21
*******************************************/


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <errno.h>
#include <signal.h>

static volatile sig_atomic_t sig = 0;


// Parses the command and executes special cases with < > and &
int parseCommand(char *userCommand, char **parameters, int comment) {
	char str1[512]; // string of characters before a redirection
	char str2[512]; // string of characters after a > redirection
	char str3[512]; // string of characters after a < redirection
	int option = 0; // indicates if there is a redirection and what type
	int moreThanOne = 0; // indicates more than one word before a redirection
	int moreThanTwo = 0; // indicates more than one word after a redirection
	int bg = 0; // indicates if the process will be run in the background
	int bothL = 0;
	int bothR = 0;
	char *pHolder; // holds userCommand characters to check before being entered to parameters

	// Loop to parse each word provided from the user input (can take up to 512 words)
	for(int i=0; i < 512; i++) {

		// pHolder is used so that the program may check for background processes without inserting & into parameters[]
		pHolder = strsep(&userCommand, " ");

		// Once the last word has been parsed, parse a null character to signify the end of the command.
		// Breaks the loop because the command has been fully parsed.
		if(pHolder == NULL) {
			parameters[i] = pHolder;
			break;
		}

		if(strcmp(pHolder, "&") != 0) { // Condition to avoid parsing the background signifier.
			parameters[i] = pHolder; // Parse the current word into the parameters array.

			// Redirect out conditional, notifies program to run the redirection fork.
			if(strcmp(parameters[i], ">") == 0) {
				option = 1;
				bothL = 1;
			}
			// Redirect in  conditional, notifies program to run the redirection fork.
			if(strcmp(parameters[i], "<") == 0) {
				option = 2;
				bothR = 1;
			}

			// This next section focuses on seperating strings for redirection.
			// str1 is everything left of a "<" or ">"  // str2 is everything after ">"
			// str3 is everything after "<" and before ">"
			//
			// If there has not been a redirection in the command add to the str1
			if(strcmp(parameters[i], ">") != 0 && strcmp(parameters[i], "<") != 0) {
				if(option == 0) {
	
					if(moreThanOne == 1) {
						sprintf(str1, " ");
					}
					sprintf(str1, "%s", parameters[i]);
					moreThanOne = 1;
				}
	
				// If there has been a > redirection add to the str2
				else if(option == 1) {
					if(moreThanTwo == 1) {
						sprintf(str2, " ");
					}
					sprintf(str2, "%s", parameters[i]);
					moreThanTwo = 1;
				}
	
				// If there has been a < redirection add to the str3
				else if(option == 2){
					sprintf(str3, "%s", parameters[i]);
				}
			}
		}

		// If the current parameter is &, add a null character to signify the end of the command and break the loop
		else {
			if(strcmp(parameters[0], "status") != 0) {
				bg = 1; // indicate that the exec will need to be run in the background (reference line 119)
				parameters[i] = NULL;
				break;
			}
		}

		// used to print the inputs of p3testscript
		printf("%s ", parameters[i]);
	}

	// From the params, comments should not do anything
	if(comment == 1) {
		return 0;
	}

	// indicates to main() that the background process should be run
	if(bg == 1) {
		return 2;
	}

	// initializations for the redirection forks
  	int childExitMethod;
  	char *err;
  	int sourceFD, targetFD, result;
  	int currpid = getpid();
  	char pid[21];

	if(bothL == 1 && bothR == 1) {
		option = 3;
	}

	// if a redirection has been triggered fork the program
	if(option == 1 || option == 2 || option == 3) {
			pid_t forkPID = fork();
			switch (forkPID) {
				// If the fork creation fails print an error
				case -1:
					err = strerror(errno);
					printf("Redirect Fork Error: %s", err);
					exit(1);
					break;
				// CHILD PROCESS, redirection
				case 0:
					// If redirection ">" is triggered
					if(option == 1) {
						// open the location for the output // create the location if it does not exist
						targetFD = open(str2, O_WRONLY | O_CREAT | O_TRUNC, 0640);
						if(targetFD == -1) { perror("target open()"); exit(1); } // open() failure msg
						// redirect the output into str2
						result = dup2(targetFD, 1);
						if(result == -1) { perror("target dup2()"); exit(2); } // dup2() failure msg
					}
					// If redirection "<" is triggered
					else if(option == 2) {
						// open the input location for read only
						targetFD = open(str3, O_RDONLY);
						if(targetFD == -1) { perror("target open()"); exit(1); } // open() failure msg
						// redirect the input of str3 to str1
						result = dup2(targetFD, 0);
						if(result == -1) { perror("target dup2()"); exit(2); } // dup2() failure msg
					}
					// If there are two redirections
					else if(option == 3) {
						// open the location for the output // create the location if it does not exist  ">"
						targetFD = open(str2, O_WRONLY | O_CREAT | O_TRUNC, 0644); // ">"
						if(targetFD == -1) { perror("target open()"); exit(1); } // open() failure msg

						// open the input location for read only  "<"
						sourceFD = open(str3, O_RDONLY);
						if(sourceFD == -1) { perror("target open()"); exit(1); } // open() failure msg

						// redirect the input of str3 to str1
						result = dup2(sourceFD, 0); // "<"
						if(result == -1) { perror("target dup2()"); exit(2); } // dup2() failure msg

						// redirect the output into str2
						result = dup2(targetFD, 1);
						if(result == -1) { perror("target dup2()"); exit(2); } // dup2() failure msg
						
					}
					result = execlp(str1, str1, NULL); // exec call, runs commands based off of the bash shell
					if(result == -1) {
						perror("exec result error\n"); // execlp() failure msg
					}
					// if exec failed exit and break
					exit(1);
					break;
				// PARENT PROCESS, waiting
				default:
					waitpid(forkPID, &childExitMethod, 0); // wait for child process to terminate
					break;
			}
			fflush(stdout);
			return 1; // signify to main() that a redirection has occured
	}
	return 0; // signify to main() that a foreground process should be run
}


// Foreground only mode triggers
// Using global variable sig, 0 signifies the program was most recently in foreground and background mode
// 1 signifies foreground only mode.
void handle_SIGTSTP(int signo) {
	if(sig == 0) {
		char* message = "Entering Foreground Only Mode\n ";
		write(STDOUT_FILENO, message, 29);
		sig = 1;
	}
	else if(sig == 1) {
		char* message = "Exiting Foreground Only Mode\n ";
		write(STDOUT_FILENO, message, 28);
		sig = 0;
	}

}


// A function to check if a background process has finished, returning the pid and status if it has
void checkBackground() {
	pid_t pid;
	int status;
	while((pid = waitpid(-1, &status, WNOHANG)) > 0) { // catch if a bg process has finished
		printf("background pid %d is done ", pid);
		// print exit status
		if(WIFEXITED(status) != 0) {
			printf("Exit value %d\n", WEXITSTATUS(status));
		}
		// Print termination signal if one was used
		else if(WIFSIGNALED(status) != 0) {	
			printf("Terminated by Signal : %d\n", WTERMSIG(status));
		}
		fflush(stdout);
	}
}


// Forking function for foreground and background processes
void otherCommand(char **parameters, int bgOrFg, int *exitStatus, int *termType) {
  	int childExitMethod;
	char* err;
	// return default SIGINT function inside the foreground child
	struct sigaction SIGINT_default = {0};
	SIGINT_default.sa_handler = SIG_DFL;
	sigfillset(&SIGINT_default.sa_mask);
	SIGINT_default.sa_flags = 0;

	// trigger and untrigger foreground only mode with SIGTSTP
	struct sigaction SIGTSTP_default = {0};
	SIGTSTP_default.sa_handler = handle_SIGTSTP;
	sigfillset(&SIGTSTP_default.sa_mask);
	SIGTSTP_default.sa_flags = 0;

	sigaction(SIGTSTP, &SIGTSTP_default, NULL);

	pid_t forkPID = fork();

	switch (forkPID) {
		// fork failure msg
		case -1:
			err = strerror(errno);
			printf("Fork Error: %s", err);
			exit(1);
			break;
		// CHILD PROCESS (bgOrFg = 0 is foreground, bgOrFg is background)
		case 0:
			// foreground exec using bash shell
	      if(bgOrFg == 0 || sig == 1) {
				//printf("The parameters are %s, %s, %s, %s\n", parameters[0], parameters[1], parameters[2], parameters[3]);
				sigaction(SIGINT, &SIGINT_default, NULL);
		   	execvp(parameters[0], parameters);
    	   }
			// background exec using bash shell
        	else if(bgOrFg == 1) {
          //	raise(SIGTSTP); // step into the background
          	execvp(parameters[0], parameters);
        	}
			// exec failure msg, exit and break if exec failed
			perror("Exec Error\n");
			fflush(stdout);
			exit(1);
			break;
		// PARENT PROCESS
		default:
			// foreground waitpid
			if(bgOrFg == 0 || sig == 1) {
		  		 waitpid(forkPID, &childExitMethod, 0);
				if(WIFSIGNALED(childExitMethod) != 0) {
					printf("terminated by signal %d\n", WTERMSIG(childExitMethod));
					fflush(stdout);
					*termType = 0;
				}
				else if(WIFEXITED(childExitMethod)) {
					*exitStatus = WEXITSTATUS(childExitMethod);
				}
			}

	// background waitpid
        	else if(bgOrFg == 1) {
			//	 waitpid(forkPID, &childExitMethod, WNOHANG);
	        	 waitpid(forkPID, &childExitMethod, WNOHANG);
         	 printf("\nBackground pid is : %d\n", forkPID);
				 fflush(stdout);
			}          	
      } // end of switch case

} 


// SIGINT handler function
int handle_SIGINT(int signo) {
	sleep(10);
  return 0;
}


int main() {

	char userCommand[2048]; // input command
	char* parameters[512]; // parts of the command
//	pid_t pidArr; // hold the pid of background processes
	int exit = 0; // smallsh will continue running until exit = 1
	int isOther; // triggers otherCommand() if 1
	int status; // exit status retainer
	int termType;

	// SIGINT signal handling (ignore all instances)
	struct sigaction SIGINT_action = {0};
	SIGINT_action.sa_handler = SIG_IGN;
	sigfillset(&SIGINT_action.sa_mask);
	SIGINT_action.sa_flags = 0;

	sigaction(SIGINT, &SIGINT_action, NULL);

	// SIGSTP signal handling (ignore all instances)
	struct sigaction SIGTSTP_action = {0};
	SIGTSTP_action.sa_handler = SIG_IGN;
	sigfillset(&SIGTSTP_action.sa_mask);
	SIGTSTP_action.sa_flags = 0;

	sigaction(SIGTSTP, &SIGTSTP_action, NULL);

	// loop that keeps smallsh running until user enters exit
	while(exit == 0) {

		checkBackground();
		isOther = 1; // otherCommand() will run unless a built in command or redirection occurs
		printf("\n: "); // colon prompt

		// get the input from the terminal, if the input does not exist return an error
		if(fgets(userCommand, sizeof(userCommand), stdin) == NULL) {
			printf("\nAn error has occured\n");
			exit = 1;
		}

		// if a command ends with the newline character replace it with a null character
		if(userCommand[strlen(userCommand)-1] == '\n') {
			userCommand[strlen(userCommand)-1] = '\0';
		}

		// if the first character of the command is # do nothing, it is a comment
   	char hash = userCommand[0];
   	char hash2 = '#';
		if(hash == hash2) {
			parseCommand(userCommand, parameters, 1);
		}
		else if(userCommand[0] == NULL) {
			// do nothing
		}
		else if(hash != hash2) { // if the line is not null or a comment, run as intended

			// initializations to convert $$ to pid
			char newArr[2048] = {0};
			int k = 0; // userCommand counter
			int x = 0; // newArr counter
			int cmd;
			int pid = getpid();
			char thePid[21];

			// Create an char array of the pid and check if the command contains $$.
			// If it does, loop through each character in the command to locate the position of it.
			// Each loop iteration a character will be entered into newArr, from userCommand if the $$
			// has not been located yet, and if $$ has been located these will be skipped in place of thePid.
			sprintf(thePid, "%d", pid);
			if(strstr(userCommand, "$$") != NULL) {
				while(userCommand[k] != NULL) {
					// if $$ is located
					if(userCommand[k] == '$' && userCommand[k+1] == '$') {
						int j = 0; // thePid counter
						while(thePid[j] != NULL) {
							newArr[x] = thePid[j];
							j++;
							x++;
						}
						k = k + 2; // thePid is fully entered, skip the next userCommand (which will be the second $)
					}
					// if $$ is not located
					else {
						newArr[x] = userCommand[k];
						k = k + 1;
						x = x + 1;
					}
				}
				// If the command contains $$ use the newArr
				cmd = parseCommand(newArr, parameters, 0);
			}
			else {
				// If the command does not contain $$ use the userCommand
				cmd = parseCommand(userCommand, parameters, 0);
			}

			// Foreground commands
			if(cmd == 0) {

				// CHANGE DIRECTORY
				if(strcmp(parameters[0], "cd") == 0) {
					// if a directory is entered, switch to it
					if(parameters[1] != NULL)  {
						chdir(parameters[1]);
					}
					// if no directory is entered, go to home directory
					else {
						chdir(getenv("HOME"));
					}
					// no need for exec
					isOther = 0;
				}

				// STATUS
				if(strcmp(parameters[0], "status") == 0) {
					if(termType = 1) {
						printf("\nExit Status : %d\n", status);
					}
					else {
						printf("Exit Signal : %d\n", status);
					}
					isOther = 0; // no need for exec
				}

				// EXIT
				if(strcmp(userCommand, "exit") == 0) {
					// exit loop (closes smallsh)
					exit = 1;
					isOther = 0; // no need for exec
				}

				// BASH COMMAND
				if(isOther == 1) {
					// run foreground bash command, retain exit status
					otherCommand(parameters, 0, &status, &termType);
				}
			}

			// If the command should be run in the background
			if(cmd == 2) {
				// run background bash command, retain exit status
				otherCommand(parameters, 1, &status, &termType);
			}
		}
			fflush(stdout);
	}
	return 0;
}
