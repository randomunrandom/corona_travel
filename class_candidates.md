| Candidate   | Criteria  | Stored information                                              | Operations                                                       |
|:------------|-----------|:---------------------------------------------------------------:|:----------------------------------------------------------------:|
| User        | SIOAT     | name, hash of a password, quiz results, visited places          | take a quiz, view places                                         |
| App         | SIOAUT    | version, device, user info                                      | login, RU map, CRUD place, CRUD quiz                             |
| Location    | duplicate | of                                                              | Place                                                            |
| Destination | duplicate | of                                                              | Place                                                            |
| 3-D media   | SOT       | name, author, metadata                                          | CRUD                                                             |
| Fact        | SOT       | place, 3D-media(?), qestion4quiz, answers4quiz                  | CRUD                                                             |
| Client      | duplicate | of                                                              | App                                                              |
| Place       | SIOAUT    | location, list of facts, list of quizes, name, 3d-media, sounds | add, add fact, add media, add quiz                               |
| Sound       | SOT       | name, duration, author                                          | CRUD                                                             |

Included not from description or story, but as a logical counterpart to above

| Candidate   | Criteria  | Stored information                                              | Operations                                                       |
|:------------|-----------|:---------------------------------------------------------------:|:----------------------------------------------------------------:|
| Server      | SIOAUT    | version, map, places, quizes, results                           | login, CUD map, CRUD place                                       |
| Map         | SIT       | list of places, lsit of journeys                                | add place, remove place, move to                                 |
| Journey     | SIOAU     | name, date started, list of places, add place, remove place,    | create, add place, remove place, add quiz, remove quiz, postpone |
| Quiz        | SIOAUT    | list of facts, name, author                                     | solve, create, add fact                                          |

