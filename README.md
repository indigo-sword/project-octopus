<div style="text-align: center;" align="center">
  <h1>Branches Of Fate</h1>
  <h3>A branch-based history game</h3>
  <image style="display: block; margin-left: auto; margin-right: auto; width: 40%; border-radius: 10%;" src="images/branches_of_fate.png"/>
  <h5>Team Indigo Sword</h5>
  <h6>2024</h6>

  <a href="https://discord.gg/dMyUErVjV9x">
    <img src="https://img.shields.io/discord/1209242387440730163?label=Discord&logo=discord" alt="Discord"> </a>
</div>

#### What is Branches of Fate?

- Branches of Fate (called Project Octopus in initial stages) is a **branch-based** game, where each piece is a level in a **branch** (or storyline) you are playing. Designed to be a **single-player** game with online features, it allows users to create their own nodes and paths and share them with others - either via popularity or by befriending other users. If you want to know more, please check [Project Octopus](projectoctopus.org)

#### What is the game like?

- Team Indigo Sword is developing Branches Of Fate to be a top-down 2D soulslike game, set in a medieval cyberpunk environment. You will play as a fallen corporate knight, who quit their job after realizing the company's true intentions. You will have to fight your way through the company's defenses, and uncover the truth behind the company's actions.

- In the game, you will be able to swing you sword to fight through enemies, as well as dodge, parry and heal. You will need to be careful, though, as the game will be unforgiving and you will have to learn from your mistakes. You will also need to keep your stamina bar in mind.

#### How is this implemented?

- This repository contains TentacleWeb, the server-side code for the game. It is implemented in Python, using the Flask - SQLAlchemy framework. Check it in tentacle-web/code. It is made basically of API, class codes and unit tests.
- The 3 basic pillars of TentacleWeb are the Node, Path and User classes, which are used to store the game's data.
- Node is a class that represents a level in the game. It contains the level's data, such as its name, description, and the path it belongs to. You can perform a series of actions on it, which will be interfaced through the client.
- Futurely, we want to **expand the architecture of the Path class** to allow for more complex paths by storing them in a JSON representation of a dictionary graph. (TBD)

##### Check out our architecture

- This also contains our tech stack.
<div style="text-align: center;" align="center">
  <image style="display: block; margin-left: auto; margin-right: auto; width: 80%; border-radius: 10%;" src="images/arch.png"/>
</div>

#### Contributing to the project

- Check our [Current TODOs](#current-todos)
- Currently, the only thing this repo would need is new endpoints for the API. They would be great "first-issue" type of tasks. We will list some endpoints we need here.
  - [ ] Get a user's nodes
  - [ ] Get a user's paths
  - [ ] Change a user's password
  - [ ] Change a user's email
  - [x] Change a user's username
  - [ ] Get most followed users
  - [ ] Unlink two nodes, but *only if a user owns both nodes*
  - [ ] (A *very* advanced one) help us change the Path class to store paths into a JSON representation of a dictionary graph

- Please feel free to fork the repository and submit a pull request. We will be happy to review it and merge it if it fills the following requirements:
  - Follows a consistent style guide (i.e. PEP8)
  - Has unit tests that cover the new code
  - Other unit tests are not broken
  - Code is documented properly

#### Installation

- Clone the repository
- Install the requirements on tentacle-web/code/requirements.txt
``` bash
git clone https://github.com/indigo-sword/project-octopus.git
cd project-octopus/tentacle-web/code
pip install -r requirements.txt
```

##### Run the server

- If you want not only to run, but also **code** the server, check its documentation on the tentacle-web folder

- If you want to run the server, follow these steps:
```bash
git clone https://github.com/indigo-sword/project-octopus.git
cd project-octopus/tentacle-web/code
pip install -r requirements.txt
python3
  >>> python3: 
  >>> from db_manager import init_db
  >>> init_db()
python3 api.py
```

- Run the test scripts if you want to check everything is working. First, run the server and then in another terminal run:

```bash
python3 [program]_test.py
```

- If you only want to **use** the database, we left over here a database file with some data. You can use it to do whatever you need. Just run the server and the database will be used accordingly. 

- We also left some sample levels in tentacle-web/levels. You can use them to test the server. Just run the server and the levels will be used accordingly.

#### Where to get help

- If you need help, please feel free to open an issue in the repository. We will be happy to help you.
- If you want to contact us, please enter [our discord server](https://discord.gg/ZgnjVCcAax)

#### Documentation links

- Flask: [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- SQLAlchemy: [SQLAlchemy](https://www.sqlalchemy.org/)
- Python: [Python](https://www.python.org/)
- Branches Of Fate: [Branches Of Fate](projectoctopus.org)

#### Current TODOs
- Check our project's board for more detailed information on what we are working on: [Project Octopus Board](https://github.com/orgs/indigo-sword/projects/1)

- [x] Server code
- [x] Client code
- [x] Backend documentation
- [ ] Game code (WIP)
- [ ] Level editor (WIP)
- [ ] Game Design Document (WIP)

#### Contributors

- **Daniel Carvalho**: Huge shoutout to Daniel "Desenhos" Carvalho for the amazing art he has been doing for the game. He created a lot of assets you will be seeing in the game, as well as the game's logo. Thanks, Daniel!
- **Anna Kelley**: Thanks for Anna "ack" Kelley for contributing with API endpoints about allowing a user to change his / her username.
- **Alexandre Tagava**: Thanks for Alexandre "Alex" Tagava for contributing with music for the game.

#### License

**Defend free software!**

- This project uses GNU GPL v3.0. Check the license file of this repository for more information: [License](https://github.com/indigo-sword/project-octopus/blob/main/LICENSE).
