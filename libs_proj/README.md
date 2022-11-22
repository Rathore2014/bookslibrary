books
=====
Books Library tracking app

Usage
-----

Here's a demo of how it works:

$ books --help
Usage: books [OPTIONS] COMMAND [ARGS]...

Lib is a small command line book tracking application.

Options:
  --help  Show this message and exit.

Commands:
  add      Add a book to library database, while adding we can assing to user as well.
  config   List the path to the Books db.
  count    Return number of books in library db.
  issue    Issue a book in db with given sn with new Reader
  list     List books from library database.
  remove   Remove book from library db with given sn.
  return   As book is returned to library set status to 'Avaiable'.
  start    Set a book status to 'Assigning'.
  update   Update a book in db with given sn with new info.
  version  Return version of Library application

$ books add Kube8

$ books
 SN   Status      Assigned_To   BookName
 ─────────────────────────────────────────
  1    Available                 Kube8

$ books add -a Shal Python

$ books list

SN   Status      Assigned_To   BookName
 ─────────────────────────────────────────
  1    Available                 Kube8
  2    Available   Shal          Python

$ books update 2 -a Sanjay

 SN   Status      Assigned_To   BookName
 ─────────────────────────────────────────
  1    Available                 Kube8
  2    Available   Sanjay        Python
  
$ books issue 1 -a Rajiv

$ books
SN   Status      Assigned_To   BookName
 ─────────────────────────────────────────
  1    Assigned    Rajiv         Kube8
  2    Available   Sanjay        Python

$ books update 1 -a Ranjan
 SN   Status     Assigned_To   BookName
 ────────────────────────────────────────
  1    Assigned   Ranjan        Kube8

$ books update 1 -b Kubernete
SN   Status     Assigned_To   BookName
 ─────────────────────────────────────────
  1    Assigned   Ranjan        Kubernete


$ books remove 2

$ books
  SN   Status     Assigned_To   BookName
 ────────────────────────────────────────
  1    Assigned   Rajiv         Kube8

