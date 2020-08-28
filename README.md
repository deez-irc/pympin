# pympin

IRC bot skeleton using pydle

* Modular - can hot-reload modules
* Can evaluate lines of python code, usefull for debugging (admin only)
* Will try to rejoin a channel if kicked
* Will regain it's nick when it becomes available

Modules
* ibip - Complies with the big meme, [IRC Bot Identification Protocol](https://github.com/inexist3nce/IBIP)
* log - Logs messages to a SQLite3 database (will be re-written)
