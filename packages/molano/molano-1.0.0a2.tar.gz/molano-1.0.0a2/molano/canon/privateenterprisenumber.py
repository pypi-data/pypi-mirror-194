 # Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import canonical


NAME_MAP: dict[str, str] = {
    'apple'     : '1.3.6.1.4.1.63',
    'samsung'   : '1.3.6.1.4.1.236'
}


class PrivateEnterpriseNumber(canonical.StringType):
    __module__: str = 'molano.canon'

    @classmethod
    def parse_name(cls, value: str) -> 'PrivateEnterpriseNumber':
        value = str.lower(value)
        if value not in NAME_MAP:
            raise LookupError(f"Unknown manufacturer: {value[:64]}")
        return cls(NAME_MAP[value])

    @classmethod
    def validate(cls, v: str) -> str:
        if v in NAME_MAP:
            v = NAME_MAP[v]
        return cls(v)