# Bot platform goals

Bot platform main goal is providing basic set of features required for writing bot for Tox messenger. 
In bot platform all possible features required for writing different kind of bots are implemented.
Developers can reuse and easily extend this set of functions for their own bots.

# Features provided by bot platform

1) Support of basic commands like command for changing name and status.
2) Basic file transfers and avatars support.
3) Simplified settings and profile management. Bot platform allows you to load and save custom settings and profile without writing any lines of code.
4) Easy deployment via Docker and pip.
5) Both NGC and OGC support (required for writing group bots).
6) Easy bootstrap scheme (bot platform will use latest nodes for you).
7) Simple and extendable solution architecture.

# How to use bot platform

As longer bot platform provides basic set of features you should extend it with all required features you need.
For extending default implementation you should do following:

1) Create ToxBotApplication and pass profile path to it. ToxBotApplication is instance of your bot application.
2) Create ToxBotAppParameters instance. This class contains various settings required for writing bot:
