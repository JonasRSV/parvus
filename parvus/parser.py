from typing import Tuple


class URLParser:
    @staticmethod
    def parse(path: str) -> Tuple[str, dict]:
        a = path.split("?")
        if len(a) == 1:
            return path, {}

        if len(a) > 2:
            raise ValueError(f"URLArgsParser failed, more than one ? in {path}")

        args = a[1].split("&")

        res = dict()
        for arg in args:
            kv = arg.split("=")
            if len(kv) == 1:
                res[kv[0]] == True
            elif len(kv) == 2:
                res[kv[0]] = kv[1]
            else:
                raise ValueError(f"URLArgsParser failed, key value arguments had unexpected format {path}")

        return a[0], res
