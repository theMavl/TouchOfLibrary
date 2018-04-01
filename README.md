
# Touch Of Library
*A library management system*

Web application based on framework Django

### Tools used
 - Back end - Python + Django
 - Front end - HTML + Bootstrap

### By
* [Mavl Pond](https://github.com/theMavl/)
* [Roman Solovev](https://github.com/rsolovev)
* [Evgeniia Kivotova](https://github.com/Genvekt)
* [Alexander Trushin](https://github.com/Skyine918)


## Delivery 3
### New systems
- Priority queue
- Document renew
- GUI


### What has been fixed/added
- User interface became nice and cute
- New fields for `patron_type` - `max_renewed_times`, `priority`
- Lifetime of copy reservation decreased to **2 days**
- User can make a request if there are no available copies. The request will be saved in the Queue.
- Position in the Queue is calculated by a formula that considers patron's priority and the date when the request was made. Output range - (0, 1)
- As soon as any copy will be returned back to library, it will be reserved for the first patron from the queue. The user will be notified via email.
- User has to confirm that he received the notification within 2 days (the system will automatically re-send mails every day)
- After user's confirmation, he has 2 more days to come to the library and check out the reserved book.
- A librarian can mark someone's request as outstanding - it will instantly set it's priority to 1.0.
- A librarian can renew someone's `giveout`, but only if patron haven't reached his `max_renewed_times` and there is no outstanding request for the document.
- Overdue days and calculated fine now can be seen in patron's Dashboard and patron's information page.
