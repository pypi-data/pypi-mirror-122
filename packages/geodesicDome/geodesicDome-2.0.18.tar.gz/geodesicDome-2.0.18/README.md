## CP38 - Development of Python Library for the Geodesic Dome
This project aims to complete a python library implementing 3 key features
related to the Geodesic Dome:

- Create a Geodesic Dome with the ability to continuously tessellate each face
  according to a specified frequency
- Tessellate a subset of faces
- Implement a neighbour search algorithm to find all points within a specified
  distance, where each neighbour can be found in O(1) time

We aim to implement these three features correctly while also trying to make the
code performant both in terms of time and memory.

Note:  
Seems like the set version crashes at freq 10, it seems like its because it uses up
too much memory for the edge creation. Will have to test adj list + edges for
current implementation.

List version just doesn't finish, no clue why and I can't be bothered trying to
figure out why.