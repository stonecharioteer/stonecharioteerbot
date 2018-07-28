# StoneCharioteerBot

This is a personal telegram bot to help me with several of the services I've built at home.

## Feature List:

- [ ] `/librarian` Library services
    - [ ] Book Search
        - [ ] Use Apache Solr backend
        - [ ] Allow natural language-based search that is converted to Lucene query syntax.
            - [ ] Example 1: "Where is my copy of the Lord of the Rings?"
            - [ ] Example 2: "Where's The Hobbit?"
            - [ ] Example 3: "Show me all books I haven't read 
        - [ ] Allow complex filtering based on criteria.
            - [ ] Example 1: "Where's the book that used to be at A11?"
            - [ ] Example 2: "Find the books I bought last May."
            - [ ] Example 3: "Find the books I bought when I bought my copy of Terry Pratchett's 5th Elephant?"
    - [ ] Book Inventory Management
        - [ ] Use Apache Solr backend
        - [ ] Allow natural language based placement of books.
            - [ ] Example 1: "I'm placing my copy of the Lord of the Rings at A12:15" 
            - [ ] Example 2: "Neil Gaiman - Smoke and Mirrors B13-14"
            - [ ] Example 3: "Moving Calvin & Hobbes: There's Treasure Everywhere to B62:78"
        - [ ] Allow movement of books through barcode photo message followed by a position.
        - [ ] Identify where a book will fit.
            - [ ] Example: "Tell me where I should put Winter's Heart."
- [ ] `/coffee`: Coffee machine timer
    - [ ] Example: "Start at 5:30 everyday."
    - [ ] Example: "Start at 5:30 and 17:30 everyday."
    - [ ] Example: "Start Now."
- [ ] `/monitor` Personal Monitor
    - [ ] Record migraines
    - [ ] Analyse migraines
    - [ ] Respond with weather report and variations in pressure.
    - [ ] Record food I've eaten.
    - [ ] Record routine
- [ ] `/price` Product price search
    - [ ] Given the link to an Amazon product page, it'll start monitoring the price every `n` minutes.
        and notify me when the price drops.
- [ ] `/shopping` Shopping List
    - [ ] Can create a shopping list. Add items, remove items. It will write to a Google Keep file.
- [ ] `/todo` To-Do List
    - [ ] Text the bot with #TODO followed by a label, it'll add it to a todo file.
    - [ ] Text just the hashtag and the label, it'll retrieve the entire todo.
- [ ] Misc. Easter Eggs
    - [ ] `/fortune` Get fortune
        - [ ] Ask for a fortune, get a fortune.
    - [ ] `/joke` Get joke
        - [ ] Ask for a joke, get a joke.
    - [ ] `/cowsay` Cowsay
        - [ ] Send text, get cowsay to respond.
    - [ ] `/quotes` Get goodreads quotes
    - [ ] `/mail` Send mail
    - [ ] `/manga` Manga Chapter Services
        - [ ] Get manga chapter (roshi wrapper)
        - [ ] Automatically notify when a chapter of a manga is out. Can subscribe to a manga.
    - [ ] `/random` Get random numbers.
- [ ] `/calendar` Schedulable responses 
    - [ ] Reminders based on events. 
        - [ ] Example: "Give me a fortune at 5:00 every day."
        - [ ] Example: "Wake me up at 2."
        - [ ] Example: "Tell me when `x` occurs."
        - [ ] Get calendar updates.

## Stack

* Search Server: `Apache Solr`
* Database: `CouchDB`
* Deployment: `Docker` + `Docker-Swarm`
* Hardware: `Raspberry Pi Zero W`
* Barcode Scanning: `OpenCV`
* Natural Language Processing: `nltk` 

## See Also

* `Shelfie`
* `TempMon`
* `W1f0`
* `Vial`
  