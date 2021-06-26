
from datetime import datetime

import bleach


class Tools:

    @staticmethod
    def bleach_clean(txt):
        return bleach.clean(txt)

    @staticmethod
    def utcnow():
        return datetime.utcnow()

    @staticmethod
    def str_to_bool(val):
        return_value = False
        if type(val) == bool:
            return_value = val
        elif type(val) == str:
            if val.lower() in ('y', 'yes', 't', 'true', 'on', '1'):
                return_value = True
        return return_value