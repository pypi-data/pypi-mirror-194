<img src="https://raw.githubusercontent.com/graphql-python/graphql-server/master/docs/_static/graphql-server-logo.svg" height="128px">

[![PyPI version](https://badge.fury.io/py/graphql-server.svg)](https://badge.fury.io/py/graphql-server)
[![Coverage Status](https://codecov.io/gh/graphql-python/graphql-server/branch/master/graph/badge.svg)](https://codecov.io/gh/graphql-python/graphql-server)

GraphQL-Server is a base library that serves as a helper
for building GraphQL servers or integrations into existing web frameworks using
[GraphQL-Core](https://github.com/graphql-python/graphql-core).

## Integrations built with GraphQL-Server

| Server integration          | Docs                                                                                    |
| --------------------------- | --------------------------------------------------------------------------------------- |
| Flask                       | [flask](https://github.com/graphql-python/graphql-server/blob/master/docs/flask.md)     |
| Sanic                       | [sanic](https://github.com/graphql-python/graphql-server/blob/master/docs/sanic.md)     |
| AIOHTTP                     | [aiohttp](https://github.com/graphql-python/graphql-server/blob/master/docs/aiohttp.md) |
| WebOb (Pyramid, TurboGears) | [webob](https://github.com/graphql-python/graphql-server/blob/master/docs/webob.md)     |

## Other integrations built with GraphQL-Server

| Server integration | Package                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------- |
| WSGI               | [wsgi-graphql](https://github.com/moritzmhmk/wsgi-graphql)                                              |
| Responder          | [responder.ext.graphql](https://github.com/kennethreitz/responder/blob/master/responder/ext/graphql.py) |

## Other integrations using GraphQL-Core or Graphene

| Server integration | Package                                                               |
| ------------------ | --------------------------------------------------------------------- |
| Django             | [graphene-django](https://github.com/graphql-python/graphene-django/) |

## Documentation

The `graphql_server` package provides these public helper functions:

- `run_http_query`
- `encode_execution_results`
- `load_json_body`
- `json_encode`
- `json_encode_pretty`

**NOTE:** the `json_encode_pretty` is kept as backward compatibility change as it uses `json_encode` with `pretty` parameter set to `True`.

All functions in the package are annotated with type hints and docstrings,
and you can build HTML documentation from these using `bin/build_docs`.

You can also use one of the existing integrations listed above as
blueprint to build your own integration or GraphQL server implementations.

Please let us know when you have built something new, so we can list it here.

## How to compile a new version of graphql-server
- Go to graphql_server/version.py file and update from 3.0.0b5 to 3.0.0b6 (for example)
- Commit and pushes the last changes
- Go to in the master branch (after merge pull request)
- Execute the command `python setup.py sdist`
- Make sure you have installed the python twine package (`pip install twine`).
- Execute the twine command to upload the new version of graphql-server to pypi.org (`twine upload dist/graphql-server-3.0.0b5.tar.gz`)
- In the previous step you will be asked for the pypi.org credentials are in 1password, you must request them in #password_requests
- Update all applications that use graphql-server with this version in their requirements.txt

## Contributing

See [CONTRIBUTING.md](https://github.com/graphql-python/graphql-server/blob/master/CONTRIBUTING.md)
