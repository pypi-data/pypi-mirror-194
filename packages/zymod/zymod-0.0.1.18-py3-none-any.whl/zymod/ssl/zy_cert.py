from dataclasses import dataclass
from datetime import datetime

from zymod.util import TimeDuration


@dataclass
class ZyCert:
    @dataclass
    class IssuedTo:
        common_name: str
        organization: str
        organization_unit: str

    @dataclass
    class IssuedBy:
        common_name: str
        organization: str
        organization_unit: str

    @dataclass
    class ValidityPeriod:
        """
        UTC时间戳
        """
        issued_on: datetime
        expires_on: datetime
        time_left: TimeDuration

    @dataclass
    class SubjectAltName:
        dns_names: list[str]

    """
    不要在此设置字段默认值，限制用户必须使用__init__初始化ZyCert。
    否则，会出现类成员变量数据累加问题。而不是作为类实例成员变量，每次都将被初始化。
    """
    cert_path: str
    root_cert_path: str
    private_key_path: str
    issued_to: IssuedTo
    issued_by: IssuedBy
    validity_period: ValidityPeriod
    subject_alt_name: SubjectAltName

    def asdict(self) -> dict:
        return {
            'Certificate Path': self.cert_path,
            'Private Key Path': self.private_key_path,
            'Root Certificate Path': self.root_cert_path,
            'Certificate': {
                'Issued To': {
                    'Common Name': self.issued_to.common_name,
                    'Organization': self.issued_to.organization,
                    'Organization Unit': self.issued_to.organization_unit,
                },
                'Issued By': {
                    'Common Name': self.issued_by.common_name,
                    'Organization': self.issued_by.organization,
                    'Organization Unit': self.issued_by.organization_unit,
                },
                'Subject Alternative Name': {
                    'DNS Names': self.subject_alt_name.dns_names
                },
                'Validity Period': {
                    'Issued On': self.validity_period.issued_on,
                    'Expires On': self.validity_period.expires_on,
                    'Time Left': self.validity_period.time_left.asdict(),
                }
            }
        }
