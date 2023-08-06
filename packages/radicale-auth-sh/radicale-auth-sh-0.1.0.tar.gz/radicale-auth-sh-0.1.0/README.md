# radicale-auth-sh

A simple Radicale **salted and hashed password** authentication plugin. This
uses a static password as described in the [docs][docs]. However in contrast to
the original example, the password is not stored in plain-text, but encrypted
using [Argon2][Argon2].

[docs]: https://radicale.org/3.0.html#documentation/plugins/getting-started
[Argon2]: https://argon2-cffi.readthedocs.io/

## Usage

To set the password:

    python -m radicale_auth_sh.config

And enter the password. Remember to note it down somewhere, preferably in your
password manager. Restart the Radicale server to start the authentication.

To reset the password, go to `~/.config/radicale/config` and delete the
`[auth]` section.

## Limitations

- Only a user level `~/.config/radicale/config` is supported
- Suits single user / single master password usage
