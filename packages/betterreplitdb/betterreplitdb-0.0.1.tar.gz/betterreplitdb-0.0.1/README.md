# Better Replit DB (Python)

*Adds a memcache to the standard replit database*

To perform database operations such as reading, writing and deleting data, the official `replit` package simply sends the corresponding request to your REPL's database URL. However, this can be made more efficient by caching the database in RAM using a python dictionary, initialized when the database is created/when the REPL starts. For `AsyncDatabase`, read operations read from the cache and update/delete operations will update the cache, then perform the action asynchronously as before. The same occurs for the synchronous `Database` but with regular/synchronous update operations.

## Usage

### Async:

Replace

``` python
from replit.database import AsyncDatabase

async_db = AsyncDatabase(replit_db_url)
```

with

``` python
from betterreplitdb import AsyncDatabase

async_db = AsyncDatabase(replit_db_url)
async_db.init_cache()
```
*Note: Replit's [docs](https://replit-py.readthedocs.io/en/latest/db_tutorial.html#async-usage) say that you need to use AsyncDatabase() to construct a DB. This is false, please use `AsyncDatabase(environ["REPLIT_DB_URL"])` instead, where environ is `os.environ`.*


### Sync:

Replace

``` python
from replit import db
```

with

``` python
from betterreplitdb import db
```

## Version Tracking

This repo is up to date with the [main repo](https://github.com/replit/replit-py) with commits:

- [replit@b36030a](https://github.com/replit/replit-py/commit/b36030a22281542fb755aa8505b3e2e020a9d18d) database.py
- [replit@a48d6a2](https://github.com/replit/replit-py/commit/a48d6a2bec48377e50936cb2835bf8222589b6f1) src/replit/database/default_db.py
- [replit@59225fb](https://github.com/replit/replit-py/commit/59225fb2f9cd1b22087a08876756a287604e0552) unit tests

If these are not the latest commits on these files, please open an issue/PR.

## Copyright

This repo is forked from Replit's, which is licensed under the ISC license, as is this project.

Copyright disclaimer for replit/replit-py

```
Copyright 2021 Replit

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```
