# mblog: A minimal markdown blog

A simple Markdown based blog that you can use every day.

## Main Features

- Very usable
- Customizable
- Simple to run

## Usage

```shell
$ pip install mblog
$ mblog
```

It launches on port **5000** and typically tries to bind on all IP addresses (`0.0.0.0`).
Usually, in a typical install, it can be accessed at http://localhost:5000. Use the [Login](/login)
link to sign in. The default password is `Password`. You should change it by following the directions
below.

## Database

Typically, when you want to run this on **Heroku** or a cloud provider, you may
want to use a MySQL database than the SQLite provider. Set the `DATABASE` environment
variable to `mysql://user:password@host/database`.

## Storage

By default, this software relies on the local file system. If you wish to use Cloud Hosting,
use **S3**, **MinIO** or some other service to host your files and images. Then use those
links directly when composing your blogs.

## Admin Credentials

You typically authenticate via the `ADMIN_PASSWORD_HASH` variable. Hashed Passwords
are obtained by hashing with **SHA-256** encoded to **Base64**:

For the default password which is `Password`, you would get its hash
as `588+9PF8OZmpTyxvYS6KiI5bECaHjk4ZOYsjvTjsIho=`

```shell
$ echo -n Password | openssl dgst -binary -sha256 | base64
588+9PF8OZmpTyxvYS6KiI5bECaHjk4ZOYsjvTjsIho=
```

## Acknowledgments

The original version of this can be found [here](<https://github.com/coleifer/peewee>).

This was taken and customized for adding File Uploads, Password Hashing, Better
Error Handling, Custom Branding with Python2 and Python3 Portability.

## Questions?

Reach out to me for any feedback.

Now Enjoy!

* Author: Karthik Kumar Viswanathan
* Web   : https://karthikkumar.org
  * Email : karthikkumar@gmail.com