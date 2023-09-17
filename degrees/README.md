# Degree
The program performs a __Breadth-First Search Algorithm__ and determines how many “degrees of separation” apart two actors are.

![image](https://github.com/Thesadsatan/projects/assets/99989899/ba3ba39c-85c1-4830-93cf-556acb000c1c)


## Background about the degree of separation

According to the Six Degrees of Kevin Bacon game, anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in.

The program will find the __shortest path__ between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

##  Overview of program

several data structures are defined to store information from the CSV files. The names dictionary is a way to look up a person by their name: it maps names to a set of corresponding ids (because it’s possible that multiple actors have the same name). The people dictionary maps each person’s id to another dictionary with values for the person’s name, birth year, and the set of all the movies they have starred in. And the movies dictionary maps each movie’s id to another dictionary with values for that movie’s title, release year, and the set of all the movie’s stars. The load_data function loads data from the CSV files into these data structures.

The main function in this program first loads data into memory (the directory from which the data is loaded can be specified by a command-line argument). Then, the function prompts the user to type in two names. The person_id_for_name function retrieves the id for any person (and handles prompting the user to clarify, in the event that multiple people have the same name). The function then calls the shortest_path function to compute the shortest path between the two people, and prints out the path.

## Explanation of the approach and the Search Algorithm 

The shortest_path performs a __Breadth-First Search (BFS) Algorithm__ first in first (FIFO) and it returns the shortest path from the person with id source to the person with the id target. The algorithm is implemented using a Class that initializes a frontier that stores the Nodes, and checks whether a particular Node already exists in the frontier, and checks whether a frontier is empty. Each Node stores a person_id, movie_id, and parent ( which is the person_id of the actor who led to this person ). The parent would ultimately be used to track the way and find the path from the target to the source. In the util.py file, there are 2 Classes StackFrontier and QueueFrontier which inherit from the StackFrontier and only change the remove method to delete the Node from the beginning of the list. The reason for writing both classes and not only the QueueFrontier is to show my familiarity with __Object Oriented Programming, inheritance and my deep understanding of both __BFS and DFS algorithms__. Since the program could use StackFrontie instead, and it would perform a __Depth-First Search (BFS)__ which would be efficient to solve this problem. 

## Explanation of the shortest_path function

1. Assuming there is a path from the source to the target, the function should return a list, where each list item is the next (movie_id, person_id) pair in the path from the source to the target. Each pair is a tuple of two strings.
   For example: if the return value of shortest_path were [(1, 2), (3, 4)], that would mean that the source starred in movie 1 with person 2, person 2 starred in      movie 3 with person 4, and person 4 is the target.

2. If there are multiple paths of minimum length from the source to the target, the function can return any of them.

3. If there is no possible path between two actors, the function should return None.


