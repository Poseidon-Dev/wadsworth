# Wadsworth | IT Assistant


Wadsworth is a multi-modular application designed to streamline repetitive processes into a single discord command interface.

Each module is a seperate application with discord running as the user interface. 

## Authors

* **[Johnny Whitworth (@Poseidon-dev)](https://github.com/poseidon-dev)** 

## Support

If you need some help for something, please reach out to me directly or submit an issue and I'll get to it as soon as I can

## Current Modules

| Module <img width=170/>     | Description <img width=450/>                                                |
| ----------------------------| ----------------------------------------------------------------------------|
| JitBit API                  | Creates a request integration into discord to allow for quicker viewing     |
| Office                      | Stores and logs MS Office keys                                              |
| Password                    | Password generator                                                          |
| Employee                    | ERP Connection                                                              |
| Censor                      | Very remidial vulgarity censor                                              |
| Support                     | Outputs ticket on the helpdesk                                              |
| Info                        | General information about Wadsworth                                         |

## How to use

An up-to-date list of modules and their current commands



| Office <img width=170/>  | What it is <img width=450/>                                                 |
| ----------------------------| ----------------------------------------------------------------------------|
| key -a [KEY]                | Adds the key to the office keys db. Must be 29 characters long              |
| key -d                      | Deletes a key from the office keys db based on table ID. Irreversible       |
| key -m                      | Prompts for computer and email and delivers an avilable key                 |
| key -r                      | Lists all available keys                                                    |
| key -c                      | Count available keys                                                        |

  
| Password <img width=170/>  | What it is <img width=450/>                                                 |
| ----------------------------| ----------------------------------------------------------------------------|
| pass                        | Generates a random password based on a list of 4000 words                   |

  
| ERP <img width=170/>  | What it is <img width=450/>                                                 |
| ----------------------------| ----------------------------------------------------------------------------|
| whois id [ID]               | Retrieves employee record with ID (Inactive or active)                      |
| whois f [First]             | Retrieves employe with fname like [First] (active)                          |
| whois l [Last]              | Retrieves employe with lname like [Last] (active)                           |
| whois fl [First] [Last]     | Retrieves employe with fname and lname like [First] [Last] (active)         |
| (AFTER LOOKUP) Property Reactions  | Retreived active company property based on user reactions after lookup|

  
| Support Desk <img width=170/>  | What it is <img width=450/>                                                 |
| ----------------------------| ----------------------------------------------------------------------------|
| URL EVENT LISTENER          | Retreives ticket information as an event listener on all messages           |

## Potential future modules

- [x] Password Generator
- [x] ERP employee integration
- [ ] Task Scheduler/Calendar
- [ ] Email Scrubber
- [x] Employee Status change tracker
- [ ] Employee asset managmenet
- [ ] Google admin API integration
- [ ] Verizon API
- [ ] Github API 
