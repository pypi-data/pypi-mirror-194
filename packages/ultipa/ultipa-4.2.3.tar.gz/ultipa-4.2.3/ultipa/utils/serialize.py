import datetime

from ultipa.types import ULTIPA
from struct import *

from ultipa.utils.common import DateTimeIs2Str, Float_Accuracy,TimestampIs2Str
from ultipa.utils.ultipa_datetime import UltipaDatetime
from ultipa.utils.errors import ParameterException, ServerException, SerializeException, checkError


class _Serialize:
    def __init__(self, type, value, name=None, export=False,timeZoneOffset=None):
        self.type = type
        self.value = value
        self.name = name
        self.export = export
        self.timeZoneOffset = timeZoneOffset

    def serialize(self):
        # if self.name in ['id', 'from_id', 'to_id']:
        #     return False
        if self.value is None:
            if self.type in [ULTIPA.PropertyType.PROPERTY_STRING,ULTIPA.PropertyType.PROPERTY_FROM,ULTIPA.PropertyType.PROPERTY_TO]:
                return ''.encode()

        if self.type == ULTIPA.PropertyType.PROPERTY_STRING or self.type == ULTIPA.PropertyType.PROPERTY_TEXT:
            if isinstance(self.value, str):
                return self.value.encode()
            else:
                return str(self.value).encode()

        elif self.type == ULTIPA.PropertyType.PROPERTY_INT32:
            if self.value == '' or self.value is None:
                self.value = 0
            try:
                upret = pack('>i', int(self.value))
                return upret
            except Exception as e:
                error = checkError(e.args[0])
                raise SerializeException(err=f"property [%s],value=%s {error}")

        elif self.type == ULTIPA.PropertyType.PROPERTY_UINT32:
            if self.value == '' or self.value is None:
                self.value = 0
            try:
                upret = pack('>I', int(self.value))
                return upret
            except Exception as e:
                error = checkError(e.args[0])
                raise SerializeException(err=f"property [%s],value=%s {error}")

        elif self.type == ULTIPA.PropertyType.PROPERTY_INT64:
            if self.value == '' or self.value is None:
                self.value = 0
            try:
                upret = pack('>q', int(self.value))
                return upret
            except Exception as e:
                error = checkError(e.args[0])
                raise SerializeException(err=f"property [%s],value=%s {error}")


        elif self.type == ULTIPA.PropertyType.PROPERTY_UINT64:
            if self.value == '' or self.value is None:
                self.value = 0
            try:
                upret = pack('>Q', int(self.value))
                return upret
            except Exception as e:
                error = checkError(e.args[0])
                raise SerializeException(err=f"property [%s],value=%s {error}")

        elif self.type == ULTIPA.PropertyType.PROPERTY_FLOAT:
            if self.value == '' or self.value is None:
                self.value = 0

            try:
                upret = pack('>f', self.value)
                return upret
            except Exception as e:
                error = checkError(e.args[0])
                raise SerializeException(err=f"property [%s],value=%s {error}")

        elif self.type == ULTIPA.PropertyType.PROPERTY_DOUBLE:
            if self.value == '' or self.value is None:
                self.value = 0
            try:
                upret = pack('>d', self.value)
                return upret
            except Exception as e:
                error = checkError(e.args[0])
                raise SerializeException(err=f"property [%s],value=%s {error}")

        elif self.type == ULTIPA.PropertyType.PROPERTY_DATETIME:
            if self.value is None:
                self.value = 0
            else:
                self.value = UltipaDatetime.datetimeStr2datetimeInt(self.value)
            try:
                upret = pack('>Q', self.value)
            except Exception as e:
                error = checkError(e.args[0])
                raise SerializeException(err=f"property [%s],value=%s {error}")
            return upret

        elif self.type == ULTIPA.PropertyType.PROPERTY_TIMESTAMP:
            if self.value is None:
                self.value = 0
            else:
                if isinstance(self.value,datetime.datetime):
                    self.value = str(self.value)
                if isinstance(self.value, str):
                    self.value = UltipaDatetime.timestampStr2timestampInt(self.value,self.timeZoneOffset)
            try:
                upret = pack('>I', self.value)
                return upret
            except Exception as e:
                error = checkError(e.args[0])
                raise SerializeException(err=f"property [%s],value=%s {error}")

    def unserialize(self):
        try:
            if self.type != ULTIPA.PropertyType.PROPERTY_STRING and len(self.value) == 0:
                return None

            elif self.type == ULTIPA.PropertyType.PROPERTY_STRING or self.type == ULTIPA.PropertyType.PROPERTY_TEXT or type is None:
                return self.value.decode()

            elif self.type == ULTIPA.PropertyType.PROPERTY_INT32:
                if len(self.value) >= 4:
                    ls = len(self.value) // 4 * 'i' or 'i'
                elif len(self.value) == 2:
                    ls = len(self.value) // 2 * 'h' or 'h'
                else:
                    ls = 'h'
                upret = unpack(f'>{ls}', self.value)
                ret = upret[0]
                return ret

            elif self.type == ULTIPA.PropertyType.PROPERTY_UINT32:
                ls = len(self.value) // 4 * 'I' or 'I'
                upret = unpack(f'>{ls}', self.value)
                ret = upret[0]
                return ret

            elif self.type == ULTIPA.PropertyType.PROPERTY_INT64:
                ls = len(self.value) // 8 * 'q' or 'q'
                upret = unpack(f'>{ls}', self.value)
                ret = upret[0]
                return ret

            elif self.type == ULTIPA.PropertyType.PROPERTY_UINT64:
                ls = len(self.value) // 8 * 'Q' or 'Q'
                upret = unpack(f'>{ls}', self.value)
                ret = upret[0]
                return ret

            elif self.type == ULTIPA.PropertyType.PROPERTY_FLOAT:
                ls = len(self.value) // 4 * 'f' or 'f'
                upret = unpack(f'>{ls}', self.value)
                ret = upret[0]
                if Float_Accuracy:
                    return round(ret,7)
                return ret

            elif self.type == ULTIPA.PropertyType.PROPERTY_DOUBLE:
                ls = len(self.value) // 8 * 'd' or 'd'
                upret = unpack(f'>{ls}', self.value)
                ret = upret[0]
                return ret

            elif self.type == ULTIPA.PropertyType.PROPERTY_DATETIME:
                ls = len(self.value) // 8 * 'Q' or 'Q'
                upret = unpack(f'>{ls}', self.value)
                ret = upret[0]
                if DateTimeIs2Str:
                    ret = UltipaDatetime.datetimeInt2datetimeStr(ret)
                return ret

            elif self.type == ULTIPA.PropertyType.PROPERTY_TIMESTAMP:
                ls = len(self.value) // 4 * 'I' or 'I'
                upret = unpack(f'>{ls}', self.value)
                ret = upret[0]
                if TimestampIs2Str:
                    ret = UltipaDatetime.timestampInt2timestampStr(ret)
                return ret

            # elif isinstance(self.value, bytes):
            #     return self.value.decode()
            else:
                raise ServerException('服务端返回类型错误')

        except Exception as e:
            # print(e)
            # if isinstance(value, bytes):
            #     return value.decode()
            raise ParameterException(err=e)
            # return str(self.value)

    def setDefaultValue(self):
        if self.type == ULTIPA.PropertyType.PROPERTY_STRING:
            self.value = ""
            return
        elif self.type == ULTIPA.PropertyType.PROPERTY_INT32:
            self.value = 0
            return
        elif self.type == ULTIPA.PropertyType.PROPERTY_UINT32:
            self.value = 0
            return
        elif self.type == ULTIPA.PropertyType.PROPERTY_INT64:
            self.value = 0
            return
        elif self.type == ULTIPA.PropertyType.PROPERTY_UINT64:
            self.value = 0
            return
        elif self.type == ULTIPA.PropertyType.PROPERTY_FLOAT:
            self.value = 0
            return
        elif self.type == ULTIPA.PropertyType.PROPERTY_DOUBLE:
            self.value = 0
            return
        elif self.type == ULTIPA.PropertyType.PROPERTY_TEXT:
            self.value = ""
            return
        elif self.type == ULTIPA.PropertyType.PROPERTY_DATETIME:
            self.value = "1970-01-01"
            return
        elif self.type == ULTIPA.PropertyType.PROPERTY_TIMESTAMP:
            self.value = "1970-01-01"
            return
