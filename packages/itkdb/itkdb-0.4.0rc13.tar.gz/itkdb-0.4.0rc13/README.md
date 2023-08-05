# ITk DB v0.4.0rc13

[![PyPI version](https://badge.fury.io/py/itkdb.svg)](https://badge.fury.io/py/itkdb)
[![Downloads](https://pepy.tech/badge/itkdb)](https://pepy.tech/project/itkdb)
[![Downloads](https://pepy.tech/badge/itkdb/month)](https://pepy.tech/project/itkdb)
[![Downloads](https://pepy.tech/badge/itkdb/week)](https://pepy.tech/project/itkdb)

To install as a user

```
pip install itkdb
```

or if you wish to develop/contribute

```
git clone ...
pip install -e .[develop]
```

or

```
git clone ...
pip install -e .[complete]
```

## Using

Command line available via

```
itkdb --help
```

## Environment Variables

See [itkdb/settings/base.py](src/itkdb/settings/base.py) for all environment
variables that can be set. All environment variables for this package are
prefixed with `ITKDB_`. As of now, there are:

- `ITKDB_ACCESS_CODE1`: access code #1 for authentication
- `ITKDB_ACCESS_CODE2`: access code #2 for authentication
- `ITKDB_ACCESS_SCOPE`: scope for the access token authentication request
- `ITKDB_AUTH_URL`: authentication server
- `ITKDB_SITE_URL`: API server
- `ITKDB_CASSETTE_LIBRARY_DIR`: for tests, where to store recorded
  requests/responses

## Develop

### Bump Version

Run `bump2version x.y.z` to bump to the next version. We will always tag any
version we bump, and this creates the relevant commits/tags for you. All you
need to do is `git push --tags` and that should be it.

# Examples

```python
import itkdb

client = itkdb.Client()
comps = client.get(
    "listComponents", json={"project": "P", "pageInfo": {"pageSize": 32}}
)

for i, comp in enumerate(comps):
    print(i, comp["code"])
```

# FAQ

## SSL Error with CERN websites

If you run into SSL errors with CERN websites, you might need the CERN
certificate chain to sign the certificates correctly. Just add a `verify`
keyword into your calls:

```python
client.get(..., verify=itkdb.data / "CERN_chain.pem")
```

and it should work.

## EOS Uploads?

To do EOS uploads, you need to install this package with the `eos` option like
so

```
python -m pip install itkdb[eos]
```

If there are further errors, see below in the FAQ.

## pycurl error

If you try running `itkdb` and run into an issue like:

```
Traceback (most recent call last):
  File "script.py", line 1, in <module>
    import itkdb
  File "/Users/kratsg/itkdb/src/itkdb/__init__.py", line 7, in <module>
    from .client import Client
  File "/Users/kratsg/itkdb/src/itkdb/client.py", line 8, in <module>
    import pycurl
ImportError: pycurl: libcurl link-time ssl backends (secure-transport, openssl) do not include compile-time ssl backend (none/other)
```

You will need to reinstall pycurl and force re-compilation. This can be done by
first checking the config for `curl` on your machine:

```
$ curl-config --features
AsynchDNS
GSS-API
HTTPS-proxy
IPv6
Kerberos
Largefile
MultiSSL
NTLM
NTLM_WB
SPNEGO
SSL
UnixSockets
alt-svc
libz
```

and then setting the appropriate compile flags. For example, on a Mac, I have
`openssl` so I do the following:

### on MacOS

```
$ brew info openssl
...
...

For compilers to find openssl@3 you may need to set:
  export LDFLAGS="-L/usr/local/opt/openssl@3/lib"
  export CPPFLAGS="-I/usr/local/opt/openssl@3/include"

...
```

which tells me to export the above lines and then I can reinstall correctly:

```
$ export LDFLAGS="-L/usr/local/opt/openssl@3/lib"
$ export CPPFLAGS="-I/usr/local/opt/openssl@3/include"
$ python -m pip install --no-cache-dir --compile --ignore-installed --install-option="--with-openssl" pycurl
```

### on lxplus (CC7)

Assuming a virtual environment like

```
$ lsetup "views dev4 latest/x86_64-centos7-gcc11-opt"
$ python3 -m venv venv
$ source venv/bin/activate
```

I looked up the locations of the installations on lxplus for you already:

```
$ export LDFLAGS="-L/usr/local/lib/openssl"
$ export CPPFLAGS="-I/usr/local/include/openssl"
$ export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/lib/pkgconfig/
$ python -m pip install --no-cache-dir --compile --ignore-installed --install-option="--with-nss" pycurl
```

### on SWAN

Assuming a virtual environment like

```
$ python3 -m venv venv
$ source venv/bin/activate
```

which came with `python3.9` by default on [swan](https://swan.cern.ch), the
installation flags needed are:

```
$ export LDFLAGS="-L/usr/lib64/openssl"
$ export CPPFLAGS="-I/usr/include/openssl"
$ export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/lib64/pkgconfig/
$ python -m pip install --no-cache-dir --compile --ignore-installed --install-option="--with-nss" pycurl
```
