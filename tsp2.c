/********************************************************************
 * Program: tsp2.cpp
 * Author: Ben Swinford
 * Date: 3/15/21
 * Description: An AI system that finds the optimal solution for the 
 * 				 travelling salesman problem.
********************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>

#define infinity 9999
#define MAXCHAR 1000

int adjacencyMatrix1[MAXCHAR][MAXCHAR],mst[MAXCHAR][MAXCHAR];
int DFSvisited1[MAXCHAR];
int adjacencyMatrix0[MAXCHAR][MAXCHAR];
int DFSvisited0[MAXCHAR];

int total = 0;


int DFS(int count, int itemNum, int tracker, FILE *file, int print) {

	if(print == 1) {
	DFSvisited1[count] = 1;
	int index = count;
	int min = 999999;
	for(int i=0; i<itemNum; i++) {
		if(!DFSvisited1[i] && adjacencyMatrix1[count][i] != 0) {
			for(int j=0; j<itemNum; j++) {
				if(adjacencyMatrix1[count][i] < min && adjacencyMatrix1[count][i] != 0) {
					index = i;
					min = adjacencyMatrix1[count][i];
				}
			}
		}
	}


	tracker++;
	if(tracker<itemNum) {
		if(print == 1) {
			fprintf(file, "%d\n", index);
		}
		total += min;
		DFS(index, itemNum, tracker, file, print);
	}
	else {
		total += adjacencyMatrix1[index][0];
	}
	}


	if(print == 0) {
	DFSvisited0[count] = 1;
	int index = count;
	int min = 999999;
	for(int i=0; i<itemNum; i++) {
		if(!DFSvisited0[i] && adjacencyMatrix0[count][i] != 0) {
			for(int j=0; j<itemNum; j++) {
				if(adjacencyMatrix0[count][i] < min && adjacencyMatrix0[count][i] != 0) {
					index = i;
					min = adjacencyMatrix0[count][i];
				}
			}
		}
	}


	tracker++;
	if(tracker<itemNum) {
		total += min;
		DFS(index, itemNum, tracker, file, print);
	}
	else {
		total += adjacencyMatrix0[index][0];
	}
	}
}


int tsp(int* xAxis, int* yAxis, int itemNum, FILE *file) {
	for(int x=0; x<itemNum; x++) {
	 // store current vertex x and y
    int currX = xAxis[x];
    int currY = yAxis[x];
	 // for each other vertex (to get edges)
    for(int y=0; y<itemNum; y++) {
		// store the comparing vertex x and y
      int newX = xAxis[y];
      int newY = yAxis[y];
		// calculate the weight of the edge
      int xVal = (currX - newX) * (currX - newX);
      int yVal = (currY - newY) * (currY - newY);
      double squareRoot = sqrt(xVal+yVal);
      int weight = round(squareRoot);
			adjacencyMatrix1[x][y] = weight;
			adjacencyMatrix1[y][x] = weight;
			adjacencyMatrix0[x][y] = weight;
			adjacencyMatrix0[y][x] = weight;
    }
  }
	for(int k = 0; k<itemNum; k++) {
		for(int z=0; z<itemNum; z++) {
			if(k==1 && z==65) {
			}
		}
	}

	int cost[MAXCHAR][MAXCHAR];
	int u,v,min_distance,distance[MAXCHAR],from[MAXCHAR];
	int visited[MAXCHAR],no_of_edges,i,min_cost,j;

	//create cost[][] matrix,spanning[][]
	for(i=0;i<itemNum;i++)
		for(j=0;j<itemNum;j++)
		{
			if(adjacencyMatrix1[i][j]==0)
				cost[i][j]=infinity;
			else
				cost[i][j]=adjacencyMatrix1[i][j];
				mst[i][j]=0;
		}

	//initialise visited[],distance[] and from[]
	distance[0]=0;
	visited[0]=1;

	for(i=1;i<itemNum;i++)
	{
		distance[i]=cost[0][i];
		from[i]=0;
		visited[i]=0;
	}

	min_cost=0;		//cost of spanning tree
	no_of_edges=itemNum-1;		//no. of edges to be added

	while(no_of_edges>0)
	{
		//find the vertex at minimum distance from the tree
		min_distance=infinity;
		for(i=1;i<itemNum;i++)
			if(visited[i]==0&&distance[i]<min_distance)
			{
				v=i;
				min_distance=distance[i];
			}

		u=from[v];

		//insert the edge in spanning tree
		mst[u][v]=distance[v];
		mst[v][u]=distance[v];
		no_of_edges--;
		visited[v]=1;

		//updated the distance[] array
		for(i=1;i<itemNum;i++)
			if(visited[i]==0&&cost[i][v]<distance[i])
			{
				distance[i]=cost[i][v];
				from[i]=v;
			}

		min_cost=min_cost+cost[u][v];
	}

	for(int idk=0; idk<itemNum; idk++) {
		DFSvisited1[idk] = 0;
		DFSvisited0[idk] = 0;
	}
	DFS(0, itemNum, 0, file, 0);
	fprintf(file, "%d\n%d\n", total, 0);
	DFS(0, itemNum, 0, file, 1);
	return min_cost;

}


// Reading in the file and allocating the data to specified locations
void processFile(char *filePath) {
  char str[MAXCHAR]; // str[] will hold the user input
  FILE *itemFile = fopen(filePath, "r");

  // series of vars to signal what type of number is being considered in the line
  // i.e. case number or vertex location numbers
  int second = 1;
  int third = 0;
  int zeroth = 0;
  // counter to track how many vertices have been checked
  int thirdTracker = 0;
  // vertices x and y locations
  int xAxis[1000];
  int yAxis[1000];
  // case number
  int theCase = 0;
  // int to track the number of vertices to be entered
  int itemNum;
  char *saveptr;

  char newFile[32];
  sprintf(newFile, "%s.txt.tour", filePath);
  FILE *file;
  file = fopen(newFile, "a");

  // obtain each character of the input
  while(fgets(str, MAXCHAR, itemFile) != NULL) {

	// get the first string / number of the line
   char* token = strtok_r(str, " ", &saveptr);
 	char str2[16];
 	strcpy(str2, token);
 	int currStr = atoi(str2);

	// enter the x and y of the vertices, trigger the mstWeight
	// function once each vertex has been entered
   if(third == 1) {
     token = strtok_r(NULL, " ", &saveptr);
     int currStr2 = atoi(token);
		 token = strtok_r(NULL, " ", &saveptr);
     int currStr3 = atoi(token);
     xAxis[thirdTracker] = currStr2;
     yAxis[thirdTracker] = currStr3;
     thirdTracker = thirdTracker + 1;
     if(thirdTracker == itemNum) {
       third = 0;
       zeroth = 1;
       int total_cost = tsp(xAxis, yAxis, itemNum, file);
     }
   }

	// Print the test case number, record the number of vertices to be entered
   if(second == 1) {
     theCase += 1;
     itemNum = currStr;
     second = 0;
     third = 1;
   }

	// After the first case this will be triggered to not record the next
	// number as the number of test cases
   if(zeroth == 1) {
     zeroth = 0;
     second = 1;
   }
  }
  fclose(itemFile);
}


int main(int argc, char *argv[]) {
	processFile(argv[1]);
	return 0;
}


