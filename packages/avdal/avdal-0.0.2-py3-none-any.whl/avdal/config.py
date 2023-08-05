import os
import re
import requests as req
from util.iam import IAM

_envre = re.compile(r'''^(?:export\s*)?([_a-zA-Z][\w_]*)\s*=\s*(.*)$''')
_varre = re.compile(r'''\$([_a-zA-Z][\w_]*)''')
_include_re = re.compile(r'''^#include\s+(.*)\s*$''')


def load_envs(*files, includes=True):
    for file in files:
        if not os.path.isfile(file):
            continue

        with open(file, "r") as f:
            for line in f.readlines():
                includes_match = _include_re.match(line)
                if includes and includes_match:
                    include_file = includes_match.group(1).strip()
                    load_envs(include_file, includes=False)

                match = _envre.match(line)
                if match is not None:
                    value = match.group(2).strip('"').strip("'")
                    for var in _varre.findall(value):
                        value = value.replace(f"${var}", os.environ.get(var, ""))
                    os.environ[match.group(1)] = value

        return


class Config:
    def __init__(self, appname=None):
        load_envs(".env", "../.env")

        self.appname = os.environ.get("APP_NAME", appname or "").upper()

        self._load_configs()

    def _load_configs(self):
        iam_host = self("IAM_HOST", default="iam.avd.al", prefixed=False)
        configs_host = self("CONFIGS_HOST", default="configs.avd.al", prefixed=False)
        client_id = self("CONFIGS_CLIENT_ID", default="") or self("CONFIGS_CLIENT_ID", default="", prefixed=False)
        client_secret = self("CONFIGS_CLIENT_SECRET", default="") or self("CONFIGS_CLIENT_SECRET", default="", prefixed=False)

        if not client_id:
            print("CONFIGS_CLIENT_ID not set. Skipping remote configs")
            return

        iam = IAM(iam_host, client_id, client_secret)
        token, error = iam.get_token()

        if not token:
            print("failed to get a token due to", error)
            return

        def load_role(role):
            res = req.get(f"https://{configs_host}/api/v1/roles/{role}/configs", headers={
                "Authorization": f"Bearer {token}",
            })

            if not res.ok:
                return

            for k, v in res.json().items():
                os.environ[k] = str(v)

        load_role(self.appname.lower())
        load_role("common")

    def __call__(self, name, default=None, cast=None, validator=None, prefixed=True):
        if self.appname and prefixed:
            name = f"{self.appname}_{name}"

        value = os.environ.get(name, default=default)

        if value is None:
            raise Exception(f"{name} not set")

        if cast:
            try:
                value = cast(value)
            except ValueError:
                raise Exception(f"cannot cast '{value}' into {cast.__name__}")

        if validator and not validator(value):
            raise ValueError(f"{name} set to invalid value: {value}")

        return value
