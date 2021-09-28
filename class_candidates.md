| Candidate | Criteria | Stored information                                              | Operations                                                       |
|-----------|----------|-----------------------------------------------------------------|------------------------------------------------------------------|
| User      | SIOAT    | name, hash of a password, quiz results, visited places          | take a quiz, view places                                         |
| Map       | SIT      | list of places, lsit of journeys                                | add place, remove place, move to                                 |
| Journey   | SIOAU    | name, date started, list of places, add place, remove place,    | create, add place, remove place, add quiz, remove quiz, postpone |
| Quiz      | SIOAUT   | list of facts, name, author                                     | solve, create, add fact                                          |
| Place     | SIOAUT   | location, list of facts, list of quizes, name, 3d-media, sounds | add, add fact, add media, add quiz                               |
