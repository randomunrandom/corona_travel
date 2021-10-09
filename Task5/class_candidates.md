Based on description and user story in [Task3](https://github.com/randomunrandom/corona_travel/blob/c0231f534defd03539edac0142a58a1222940785/Task%203.%20Product%20definition.pptx)

| Candidate   | Criteria  | Stored information                                              | Operations                           |
|:------------|-----------|:----------------------------------------------------------------|:-------------------------------------|
| User        | SIOAT     | name, hash of a password, quiz results, visited places          | take a quiz, view places             |
| App         | SIOAUT    | version, device, user info                                      | login, RU map, CRUD place, CRUD quiz |
| Location    | duplicate | of                                                              | Place                                |
| Destination | duplicate | of                                                              | Place                                |
| 3-D media   | SOT       | name, author, metadata                                          | CRUD                                 |
| Fact        | SOT       | place, 3D-media(?), qestion4quiz, answers4quiz                  | CRUD                                 |
| Client      | duplicate | of                                                              | App                                  |
| Place       | SIOAUT    | location, list of facts, list of quizes, name, 3d-media, sounds | add, add fact, add media, add quiz   |
| Sound       | SOT       | name, duration, author                                          | CRUD                                 |

Included not from description or story, but as a logical counterpart to above

| Candidate   | Criteria  | Stored information                                 | Operations                                                       |
|:------------|-----------|:---------------------------------------------------|:-----------------------------------------------------------------|
| Server      | SIOAUT    | version, map, places, quizes                       | login, RU map, CRUD place, CRUD quiz, CRUD sound, CRUD 3d-media  |
| Map         | SIT       | list of places, lsit of journeys                   | add place, remove place, move to                                 |
| Journey     | SIOAU     | name, date started, list of places, list of quizes | create, add place, remove place, add quiz, remove quiz, postpone |
| Quiz        | SIOAUT    | list of facts, name, author                        | solve, create, add fact                                          |

