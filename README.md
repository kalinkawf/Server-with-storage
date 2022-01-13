# Server with storage
 Simple server to save data of processes of PC

Server understands only put and get commands, any other raises exception or returns wrongvalue.
User can save data of process, value of memory as float and timestamp as int in seconds.
get * returns every data, that exists in storage atm .
Server can process more, than 1 person at one time thanks to asyncio
