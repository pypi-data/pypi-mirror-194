## Termforces
Termforces is a CLI wrapper for scraper. Currently it has a python module and a shell script

## Quickstart
Use `termforces login <username>` to login, it will store your session,
so you're not needed to do it often.

Then enter a directory you want and use `termforces strap --contest-id <contest_id> --indices <indices>`.

Indices should be separated with space, i.e `termforces strap --contest-id 1329 --indices "A B1 B2 C D E"`.
It will create folders `problem$index` for each index you specified.

You may also specify template folder with `--template <path-to-template-folder>`, in this case script will copy
its contents to all problem subfolders.

You can check your results with `termforces results` and submit files with `termforces submit <filename>`.
Script will determine contest id from parent .rc file and problem index from folder name. You may run it either from parent or from child
directory.
