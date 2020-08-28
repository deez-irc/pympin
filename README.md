# pympin

IRC bot skeleton using pydle

* Modular - can hot-reload modules
* Command rate-limiting [depends on the **log** module]
* Can evaluate lines of python code, useful for debugging (admin only)
* Checks if admins/owner is identified, auto ops them
* Will try to rejoin a channel if kicked
* Will regain its nick when it becomes available

Modules
* ibip - Complies with the big meme, [IRC Bot Identification Protocol](https://github.com/inexist3nce/IBIP)
* log - Logs messages to a SQLite3 database (will be re-written)
