What we want to have is a sequence of nodes like this:

![Nodes connected. Their incoming degree might be of 1 or more. No self loops.](images/graph.png)

We can see different paths: N1 - N2, N1 - N4 - N2, N1 - N4 - N5 - N3 - N6, N1 - N3 - N6.
Each path is made of different Nodes (that's why we have N[n] for the nodes in the graph).

**Each path has:**

- a description
- an owner (from the User class)
- a playcount
- a rating

**Each node has:**

- a description
- an owner (from the User class)
- a playcount
- a rating
- connections to other nodes, in the NodeLink class.

**Each user has:**

- a bio
- an username
- a password (hashed)
- an email
- follows
- friends

**How we are creating this:**

- Nodes: we store nodes in a db table, and their links (many to many) in another one.
- Paths: we have paths with their info in a table, and a many to many table with the sequence of nodes in each path
- Users: we store them in a DB table, their friends in a many to many table and their followers similarly

**How the client will interact with all of this:**

We are building the API for any client to do get and post requests to it.
