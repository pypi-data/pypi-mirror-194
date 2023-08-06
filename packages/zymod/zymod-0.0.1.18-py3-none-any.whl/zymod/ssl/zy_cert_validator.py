from typing import Any

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.x509 import Name, ObjectIdentifier, Certificate
from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from happy_python import HappyLog

from zymod.event import ZyInternalEvent, ZyEventLevel
from zymod.ssl import ZyCert
from zymod.util import TimeDurationCalculator


class ZyCertValidator:
    """
    HTTP SSL证书校验器

    1、检查证书文件、密钥文件以及根证书文件有效性；
    2、确认证书文件和密钥文件是否匹配；
    3、导出证书信息
    """
    __cert: Certificate = None
    __cert_chain: Certificate = None
    __hlog = HappyLog.get_instance()
    __private_key: Any = None

    __cert_path: str = ''
    __root_cert_path: str = ''
    __private_key_path: str = ''

    def __init__(self, cert_path: str, root_cert_path: str, private_key_path: str):
        self.__cert_path = cert_path
        self.__root_cert_path = root_cert_path
        self.__private_key_path = private_key_path

    @staticmethod
    def __get_nameoid_value(name: Name, oid: ObjectIdentifier) -> str:
        r = name.get_attributes_for_oid(oid)

        # <未包含在证书中>
        return r[0].value if r else "<Not Part of Certificate>"

    @staticmethod
    def __load_cert_path(file: str, desc: str) -> Certificate:
        try:
            with open(file, 'rb') as f_handler:
                return x509.load_pem_x509_certificate(data=f_handler.read(), backend=default_backend())
        except ValueError:
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='无效的%s文件：%s' % (desc, file))
        except OSError as e:  # IsADirectoryError | FileNotFoundError | ...
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='载入%s文件时，出现系统错误：%s' % (desc, e))

    def __load_cert(self, file: str) -> None:
        self.__cert = self.__load_cert_path(file, 'SSL证书')

    def __load_root_cert(self, file: str) -> None:
        self.__cert_chain = self.__load_cert_path(file, 'SSL证书密钥')

    def __load_private_key(self) -> None:
        try:
            with open(self.__private_key_path, 'rb') as f_handler:
                self.__private_key = serialization.load_pem_private_key(data=f_handler.read(),
                                                                        password=None,
                                                                        backend=default_backend())
        except ValueError:
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='无效的SSL密钥文件：%s' % self.__private_key_path,
                                  trigger='无效的SSL密钥文件')
        except OSError as e:  # IsADirectoryError | FileNotFoundError | ...
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='载入SSL密钥文件时，出现系统错误：%s' % e,
                                  trigger='载入SSL密钥文件时，出现系统错误')

    def __step1_verify_cert_files(self) -> None:
        """
        验证证书（公钥）文件和根证书文件（如fullchain.pem, chain.pem）
        :return:
        """
        self.__load_cert(self.__cert_path)
        self.__load_root_cert(self.__root_cert_path)

    def __step2_verify_cert(self) -> None:
        """
        证书是否由指定CA机构颁发（如fullchain.pem->chain.pem）
        :return:
        """
        try:
            self.__cert_chain.public_key().verify(
                signature=self.__cert.signature,
                data=self.__cert.tbs_certificate_bytes,
                padding=padding.PKCS1v15(),
                algorithm=self.__cert.signature_hash_algorithm)
        except InvalidSignature:
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='证书（%s）不是指定CA机构（%s）颁发的' % (self.__cert_path, self.__root_cert_path),
                                  trigger='证书不是由指定CA机构颁发')

    def __step3_verify_private_key_file(self) -> None:
        """
        验证密钥文件（如privkey.pem）
        :return:
        """
        self.__load_private_key()

    def __step4_verify_signature(self) -> None:
        """
        验证签名

        完整执行一次明文->密文（签名字符串）->明文的加解密流程，验证证书和密钥是否匹配（如fullchain.pem+privkey.pem）
        :return:
        """
        plain_text = b'Hello world!'

        cipher_text = self.__private_key.sign(data=plain_text,
                                              padding=padding.PKCS1v15(),
                                              algorithm=self.__cert.signature_hash_algorithm)

        try:
            self.__cert.public_key().verify(
                signature=cipher_text,
                data=plain_text,
                padding=padding.PKCS1v15(),
                algorithm=self.__cert.signature_hash_algorithm)
        except InvalidSignature:
            raise ZyInternalEvent(level=ZyEventLevel.Alert,
                                  summary='SSL证书验证失败',
                                  description='签名验证失败，证书文件：%s，密钥文件：%s' % (self.__cert_path, self.__private_key_path),
                                  trigger='签名验证失败')

    def verify(self):
        self.__step1_verify_cert_files()
        self.__step2_verify_cert()
        self.__step3_verify_private_key_file()
        self.__step4_verify_signature()

    def dump_formatted_data(self) -> ZyCert:
        """
        导出格式化后的证书数据
        :return:
        """
        assert self.__cert

        subject_alt_name_oid_value = \
            self.__cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME).value

        try:
            dns_names: list[str] = list()
            get_values_for_type_func = getattr(subject_alt_name_oid_value, 'get_values_for_type')

            for dns in get_values_for_type_func(x509.DNSName):
                dns_names.append(dns)
        except AttributeError:
            assert False

        time_duration = TimeDurationCalculator.calculate(self.__cert.not_valid_after, self.__cert.not_valid_before)

        output = ZyCert(cert_path=self.__cert_path,
                        root_cert_path=self.__root_cert_path,
                        private_key_path=self.__private_key_path,
                        issued_to=ZyCert.IssuedTo(
                            common_name=self.__get_nameoid_value(self.__cert.subject, NameOID.COMMON_NAME),
                            organization=self.__get_nameoid_value(self.__cert.subject, NameOID.ORGANIZATION_NAME),
                            organization_unit=self.__get_nameoid_value(self.__cert.subject,
                                                                       NameOID.ORGANIZATIONAL_UNIT_NAME)),
                        issued_by=ZyCert.IssuedBy(
                            common_name=self.__get_nameoid_value(self.__cert.issuer, NameOID.COMMON_NAME),
                            organization=self.__get_nameoid_value(self.__cert.issuer, NameOID.ORGANIZATION_NAME),
                            organization_unit=self.__get_nameoid_value(self.__cert.issuer,
                                                                       NameOID.ORGANIZATIONAL_UNIT_NAME)),
                        validity_period=ZyCert.ValidityPeriod(issued_on=self.__cert.not_valid_before,
                                                              expires_on=self.__cert.not_valid_after,
                                                              time_left=time_duration),
                        subject_alt_name=ZyCert.SubjectAltName(dns_names=dns_names))

        return output
