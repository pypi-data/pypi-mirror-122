# target-s3-json

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pipelinewise-target-s3-csv.svg)](https://pypi.org/project/pipelinewise-target-s3-csv/)
[![License: Apache2](https://img.shields.io/badge/License-Apache2-yellow.svg)](https://opensource.org/licenses/Apache-2.0)

[Singer](https://www.singer.io/) target that uploads loads data to S3 in JSON format
following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

## How to use it

## Install

First, make sure Python 3 is installed on your system or follow these
installation instructions for [Mac](http://docs.python-guide.org/en/latest/starting/install3/osx/) or
[Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04).

It's recommended to use a virtualenv:

```bash
  python3 -m venv env-target-s3-json
  pip install target-s3-json
```

Install the package target-s3-json in the virtualenv:

```bash
  source env-target-s3-json/bin/activate
  pip install git+https://github.com/ScalefreeCOM/scalefree-target-s3-json
  deactivate
```

### To run

Like any other target that's following the singer specification:

```bash
  some-singer-tap --catalog [catalog.json] | ~/environment/env-target-s3-json/bin/python3 env-target-s3-json/lib/python3.7/site-packages/target_s3_json/__init__.py --config [config.json]
```

**Note**: To avoid version conflicts run `tap` and `targets` in separate virtual environments.

### Configuration settings

Running the target connector requires a `config.json` file. An example with the minimal settings:

   ```json
   {
	"aws_access_key_id": "ACCESS-KEY",
	"aws_secret_access_key": "SECRET",
	"s3_bucket": "BUCKET",
	"s3_key_prefix": "SOME-PREFIX/",
	"delimiter": ","
   }
   ```

## License

Apache License Version 2.0

See [LICENSE](LICENSE) to see the full text.
