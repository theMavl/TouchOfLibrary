# Touch Of Library
*A library management system*

Web application based on framework Django

Primary language - Python

### By
* [Mavl Pond](https://github.com/theMavl/)
* [Roman Solovev](https://github.com/rsolovev)
* [Evgeniia Kivotova](https://github.com/Genvekt)
* [Alexander Trushin](https://github.com/Skyine918)


## Delivery 2
### New systems
- Document adding/editing/deleting
- Document copy adding/editing/deleting
- Patron adding/editing/deleting
- Request for returning
- Document returning


### What has been fixed/added
- Reservation now actually reserves a copy to user
- Reservations older than 5 days will be automatically removed on app startup
- User can pick a copy of document he likes the most
- Overdued give-outs now hightlighted red in Librarian's dashboard
- Librarian now can set custom giving-out time (instead of the max available)
- Patron can not reserve documents if he reached his limits of booking (which is defined by patron type)
- At the end of creation a patron in Librarian Dashboard, there will be an information page containing all necessary data concerning newly created user, including log-in credentials. This page is to be printed and given out to user
