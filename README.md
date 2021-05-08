# Wadsworth | IT Assistant


Wadsworth is a multi-modular application designed to streamline repetitive processes into a single discord command interface.

Each module is a seperate application with discord running as the user interface. 

## Authors

* **[Johnny Whitworth (@Poseidon-dev)](https://github.com/poseidon-dev)** 

## Support

If you need some help for something, please reach out to me directly or submit an issue and I'll get to it as soon as I can

## How to use

An up-to-date list of modules and their current commands

| Injection <img width=200/>  | What it is <img width=500/>                                                 |
| ----------------------------| ----------------------------------------------------------------------------|
| key -a [KEY]                | Adds the key to the office keys db. Must be 29 characters long              |
| key -d                      | Deletes a key from the office keys db based on table ID. Irreversible       |
| key -m                      | Prompts for computer and email and delivers an avilable key                 |
| key -r                      | Lists all available keys                                                    |
| key -c                      | Count available keys                                                        |
| ticket [TICKETID]           | Retrieves a ticket based on ticket ID                                       |
| tickets                     | Retrieves all active tickets                                                |
| url [URL] [COUNT]           | Retrieves a ticket based on URL, delivers comments based on count           |
| pass                        | Generates a random password based on a list of 4000 words                   |
| whois id [ID]               | Retrieves employee record with ID (Inactive or active)                      |
| whois f [First]             | Retrieves employe with fname like [First] (active)                          |
| whois l [Last]              | Retrieves employe with lname like [Last] (active)                           |
| whois fl [First] [Last]     | Retrieves employe with fname and lname like [First] [Last] (active)         |

## Current Modules

| Module <img width=200/>     | Description <img width=500/>                                                |
| ----------------------------| ----------------------------------------------------------------------------|
| JitBit API                  | Creates a request integration into discord to allow for quicker viewing     |
| Office                      | Stores and logs MS Office keys                                              |
| Password                    | Password generator                                                          |
| Employee                    | ERP Connection                                                              |
| Censor                      | Very remidial vulgarity censor                                              |
| Info                        | General information about Wadsworth                                         |
## Potential future modules

- [x] Password Generator
- [x] ERP employee integration
- [ ] Task Scheduler/Calendar
- [ ] Email Scrubber
- [ ] Employee Status change tracker
- [ ] Employee asset managmenet
- [ ] Google admin API integration
- [ ] Verizon API
- [ ] Github API 
