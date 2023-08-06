from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CanonicalizationMethod:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


@dataclass
class DigestMethod:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


@dataclass
class Merchant:
    acq_bin: Optional[int] = field(
        default=None,
        metadata={
            "name": "acqBIN",
            "type": "Element",
        }
    )
    mer_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "merID",
            "type": "Element",
        }
    )


@dataclass
class Purchase:
    xid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purch_amount: Optional[int] = field(
        default=None,
        metadata={
            "name": "purchAmount",
            "type": "Element",
        }
    )
    currency: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    exponent: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class SignatureMethod:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


@dataclass
class Tx:
    class Meta:
        name = "TX"

    time: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    status: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    cavv: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    eci: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    cavv_algorithm: Optional[int] = field(
        default=None,
        metadata={
            "name": "cavvAlgorithm",
            "type": "Element",
        }
    )


@dataclass
class X509Data:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    x509_certificate: List[str] = field(
        default_factory=list,
        metadata={
            "name": "X509Certificate",
            "type": "Element",
        }
    )


@dataclass
class KeyInfo:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    x509_data: Optional[X509Data] = field(
        default=None,
        metadata={
            "name": "X509Data",
            "type": "Element",
        }
    )


@dataclass
class Pares:
    class Meta:
        name = "PARes"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    merchant: Optional[Merchant] = field(
        default=None,
        metadata={
            "name": "Merchant",
            "type": "Element",
        }
    )
    purchase: Optional[Purchase] = field(
        default=None,
        metadata={
            "name": "Purchase",
            "type": "Element",
        }
    )
    pan: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    tx: Optional[Tx] = field(
        default=None,
        metadata={
            "name": "TX",
            "type": "Element",
        }
    )


@dataclass
class Reference:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "URI",
            "type": "Attribute",
        }
    )
    digest_method: Optional[DigestMethod] = field(
        default=None,
        metadata={
            "name": "DigestMethod",
            "type": "Element",
        }
    )
    digest_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "DigestValue",
            "type": "Element",
        }
    )


@dataclass
class SignedInfo:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    canonicalization_method: Optional[CanonicalizationMethod] = field(
        default=None,
        metadata={
            "name": "CanonicalizationMethod",
            "type": "Element",
        }
    )
    signature_method: Optional[SignatureMethod] = field(
        default=None,
        metadata={
            "name": "SignatureMethod",
            "type": "Element",
        }
    )
    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "name": "Reference",
            "type": "Element",
        }
    )


@dataclass
class Signature:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    signed_info: Optional[SignedInfo] = field(
        default=None,
        metadata={
            "name": "SignedInfo",
            "type": "Element",
        }
    )
    signature_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "SignatureValue",
            "type": "Element",
        }
    )
    key_info: Optional[KeyInfo] = field(
        default=None,
        metadata={
            "name": "KeyInfo",
            "type": "Element",
        }
    )


@dataclass
class Message:
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    pares: Optional[Pares] = field(
        default=None,
        metadata={
            "name": "PARes",
            "type": "Element",
        }
    )
    signature: Optional[Signature] = field(
        default=None,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )


@dataclass
class ThreeDSecure:
    class Meta:
        name = "ThreeDSecure"

    message: Optional[Message] = field(
        default=None,
        metadata={
            "name": "Message",
            "type": "Element",
        }
    )
