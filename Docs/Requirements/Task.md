# Chat Task

You will make a chat-like app that can run in command-line.

## Requirements

All input / output will be made by command-line.  
You may use `input()` function for getting input,  
and use `output()` for showing output.

As input, next commands will be used.

- `add_user <id(string)>`
- `talk <from_id> <to_id> <content(string)>`
- `show_log <id_1> <id_2>`

### `add_user`

Register a new user into a system.

If there is an id dupplication with an old (already registered) user, output `ERROR: ID already used!`

If successfully registered, show `<ID> registered!`

ex1)

```
input: add_user adam
OUTPUT: adam registered!
input: add_user adam
OUTPUT: ERROR: ID already used!
```

### `talk`

Memorize the talk conversation in the system.

If there are none of the given user ID registered, show `Error: no user ID`  
Else, don't output anything.

ex2) Only `adam`, `eve` registered

```
input: talk adam eve hi
input: talk eve adam I hate you
input: talk adam gogami nyugaku
OUTPUT: Error: no user ID
```

### `show_log`

Show conversation between 2 users.

If there are none of the given user ID registered, show `Error: no user ID`

Else, output with this format.

```
<from_ID> -> <to_ID>: <content>
```

ex3) after ex2

```
input: show_log adam eve
OUTPUT: adam -> eve: hi
eve -> adam: I hate you
input: show_log adam gogami
OUTPUT: ERROR: no user ID
```
