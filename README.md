# Walmart Interview Challenge: Movie Theater Seating Arrangement

## By Nicholas Passantino

### Running the Program
All you need to run this program is python. Simply run: `python main.py "test1.txt"` to generate output. The answers to the challenge are saved in `out.txt` while a visualization of where the customers are in the theater is printed to the console. There are a few test files that all work.

### Simple Explanation of my Methodology
The easiest way to understand what I did is to look at `theater_visualization.jpg` which I made to describe the order of regions where my program delegates customers first before filling in whatever blanks there might be.


### Customer Satisfaction (in order of priority)
1. Customers prefer to sit next to their reservation group members
    - I place groups together unless they do not fit in any row, then I recursively divide the groups until they fit into remaining seats
2. Customers prefer to sit in the center of the room, away from the screen, and as far from strangers as possible
    - I initially place the first 5 reservations in alternating center rows, with reservations after that being placed to the left and right aisles, maximizing distance between groups
    - Both of these steps are done from highest row letter to lowest since distance from screen is preferred
3. Customers prefer to see the movie rather than not
    - My algorithm at this point, after the above steps, just places groups wherever they fit, so long as the capacity of the theater is not reached.

### Customer Safety
1. I implemented my solution using the 3-seat buffer between groups. I chose not to break up groups to maintain the buffer, as customers probably value sitting with their companions more than they would appreciate being separated to uphold safety standards they are not aware of.
2. The first 15 groups are maximally spaced out (assuming no oversized groups, then step 3 of above is used) which also should maximize safety due to crowd size


### Assumptions
1.  A reservation is cancelled if it would cause the capacity (200) to be exceeded
2.  After a customer is placed, those customer's seats cannot be moved (earliest reservations should keep their priority seating)
3.  Center seats are more enjoyable for the consumer than those to the sides
4.  Farther / higher seats are more enjoyable for the consumer than those closer to the screen


