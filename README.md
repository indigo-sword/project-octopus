<div style="text-align: center;" align="center">
  <h1>Project Octopus</h1>
  <h3>A node-based history game</h3>
  <image style="display: block; margin-left: auto; margin-right: auto; width: 10%; border-radius: 10%;" src="images/octopus.png"/>
  <h5>Team Indigo Sword</h5>
  <h6>2024</h6>

  <a href="https://discord.gg/dMyUErVjV9x">
    <img src="https://img.shields.io/discord/1209242387440730163?label=Discord&logo=discord" alt="Discord"> </a>
</div>

#### What is Project Octopus?

- Project Octopus is a **node-based** game, where each node is a level in a **path** (or storyline) you are playing. Designed to be a **single-player** game with online features, it allows users to create their own nodes and paths and share them with others - either via popularity or by befriending other users. If you want to know more, please check [Project Octopus](projectoctopus.org)

#### What is the game like?

- Team Indigo Sword is developing Project Octopus to be a top-down 2D soulslike game, set in a medieval cyberpunk environment. You will play as a fallen corporate knight, who quit their job after realizing the company's true intentions. You will have to fight your way through the company's defenses, and uncover the truth behind the company's actions.

- In the game, you will be able to swing you sword to fight through enemies, as well as dodge, parry and heal. You will need to be careful, though, as the game will be unforgiving and you will have to learn from your mistakes. You will also need to keep your stamina bar in mind.

#### How is this implemented?

- This repository contains TentacleWeb, the server-side code for the game. It is implemented in Python, using the Flask - SQLAlchemy framework. Check it in tentacle-web/code. It is made basically of API, class codes and unit tests.
- The 3 basic pillars of TentacleWeb are the Node, Path and User classes, which are used to store the game's data.
- Node is a class that represents a level in the game. It contains the level's data, such as its name, description, and the path it belongs to. You can perform a series of actions on it, which will be interfaced through the client.

##### Check out our architecture

- This also contains our tech stack.
<div style="text-align: center;" align="center">
  <image style="display: block; margin-left: auto; margin-right: auto; width: 80%; border-radius: 10%;" src="images/arch.png"/>
</div>

#### Contributing to the project

- Check our [Current TODOs](#current-todos)
- If you want to contribute to any of them, please feel free to fork the repository and submit a pull request. We will be happy to review it and merge it if it is good. We will comment as soon as possible. Just be sure to use python's PEP8 style guide and to write unit tests for your code. Also make sure to document your code properly and that other unit tests are not broken.

#### Installation

- Clone the repository
- Install the requirements

##### Run the server

```bash
git clone
cd tentacle-web
export FLASK_APP=api
python3 api.py
```

- Run the test scripts if you want

```bash
python3 [program]_test.py
```

#### Where to get help

- If you need help, please feel free to open an issue in the repository. We will be happy to help you.
- If you want to contact us, please enter [our discord server](https://discord.gg/ZgnjVCcAax)

#### Documentation links

- Flask: [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- SQLAlchemy: [SQLAlchemy](https://www.sqlalchemy.org/)
- Python: [Python](https://www.python.org/)
- Project Octopus: [Project Octopus](projectoctopus.org)

#### Current TODOs

- [x] Server code
- [ ] Client code
- [ ] Backend documentation
- [ ] Game code
- [ ] Level editor
- [ ] Game Documentation

#### Contributors

**Be the first to contribute!**

- We would love to have someone contribute to our project. If you want to be the first, please feel free to fork the repository and submit a pull request. Check out the [Contributing to the project](#contributing-to-the-project) section for more information.

#### License

**Defend free software!**

- This project uses GNU GPL v3.0. Check the license file of this repository for more information: [License](https://github.com/indigo-sword/project-octopus/blob/main/LICENSE).
