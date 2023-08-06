# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['minisignxml', 'minisignxml.internal']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.8', 'defusedxml>=0.6.0', 'lxml>=4.4.1']

setup_kwargs = {
    'name': 'minisignxml',
    'version': '21.10',
    'description': 'Minimal XML signature and verification, intended for use with SAML2',
    'long_description': '# minisignxml\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![CircleCI](https://circleci.com/gh/HENNGE/minisignxml.svg?style=svg)](https://circleci.com/gh/HENNGE/minisignxml)\n\n\nPython library to sign and verify XML documents. \n\nThis library, *on purpose*, only supports a limited part of the xmldsig specification. It is mainly aimed at allowing SAML documents to be signed and verified.\n\nSupported features:\n\n* Simple API.\n* Only support enveloped signatures (`http://www.w3.org/2000/09/xmldsig#enveloped-signature`)\n* Require and only support exclusive XML canonincalization without comments (`http://www.w3.org/2001/10/xml-exc-c14n#`)\n* Support SHA-256 (default) and SHA-1 (for compatibility, not recommended) for signing and digest (`https://www.w3.org/2000/09/xmldsig#sha1`, `https://www.w3.org/2000/09/xmldsig#rsa-sha1`, `http://www.w3.org/2001/04/xmlenc#sha256`, `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256`)\n* Only support X509 certificates and RSA private keys\n* Uses `lxml` for XML handling and `cryptography` for cryptography.\n* Only supports a single signature, with a single reference in a document.\n* Support certificate rollover by providing multiple certificates when verifying a document.\n\n`minisignxml` performs no IO and you have to manage and load the keys/certificates yourself.\n\n## API\n\n### Signing\n\n`minisignxml.sign.sign`\n\n```python\ndef sign(\n    *,\n    element: Element,\n    private_key: RSAPrivateKey,\n    certificate: Certificate,\n    config: SigningConfig = SigningConfig.default(),\n    index: int = 0\n) -> bytes:\n```\n\nSigns the given `lxml.etree._Element` with the given `cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey` private key, embedding the `cryptography.x509.Certificate` in the signature. Use `minisignxml.config.SigningConfig` to control the hash algorithms uses (default is SHA-256). The `index` controls at which index the signature element is appended to the element.\n\nIf the `element` passed in does not have an `ID` attribute, one will be set automatically. It is the callers responsibility to ensure the `ID` attribute of the `Element` is unique for the whole document.\n\nReturns `bytes` containing the serialized XML including the signature. \n\n#### SigningConfig\n\n`minisignxml.config.SigningConfig` is a `dataclass` with the following fields:\n\n* `signature_method`: A `cryptography.hazmat.primitives.hashes.HashAlgorithm` to use for the signature. Defaults to an instance of `cryptography.hazmat.primitives.hashes.SHA256`.\n* `digest_method`: A `cryptography.hazmat.primitives.hashes.HashAlgorithm` to use for the content digest. Defaults to an instance of `cryptography.hazmat.primitives.hashes.SHA256`.\n\n\n### Verifying\n\n`minisignxml.verify.extract_verified_element`\n\n```python\ndef extract_verified_element(\n    *, \n    xml: bytes, \n    certificate: Certificate,  \n    config: VerifyConfig=VerifyConfig.default()\n) -> Element:\n```\n\nVerifies that the XML document given (as bytes) is correctly signed using the private key of the `cryptography.x509.Certificate` provided. \n\nA successful call to `extract_verified_element` does not guarantee the integrity of the whole document passed to it via the `xml` parameter. Only the sub-tree returned from the function has been verified. The caller should use the returned `lxml.etree._Element` for further processing.\n\nRaises an exception (see `minisignxml.errors`, though other exceptions such as `ValueError`, `KeyError` or others may also be raised) if the verification failed. Otherwise returns the signed `lxml.etree._Element` (not necessarily the whole document passed to `extract_verified_element`), with the signature removed.\n\nYou can control the allowed signature and digest method by using a custom `VerifyConfig` instance. By default only SHA-256 is allowed.\n\n`minisignxml.verify.extract_verified_element_and_certificate`\n\n```python\ndef extract_verified_element_and_certificate(\n    *, \n    xml: bytes, \n    certificates: Collection[Certificate],  \n    config: VerifyConfig=VerifyConfig.default()\n) -> Tuple[Element, Certificate]:\n```\n\nSimilar to `extract_verified_element`, but allows specifying multiple certificates to aid certificate rollover.\nThe certificate that was used to sign the xml will be returned with the verified element.\n\n#### VerifyConfig\n\n`minisignxml.config.SigningConfig` is a `dataclass` with the following fields:\n\n* `allowed_signature_methods`: A container of `cryptography.hazmat.primitives.hashes.HashAlgorithm` types to allow for signing. Defaults to `{cryptography.hazmat.primitives.hashes.SHA256}`.\n* `allowed_digest_methods`: A container of `cryptography.hazmat.primitives.hashes.HashAlgorithm` types to allow for the content digest. Defaults to `{cryptography.hazmat.primitives.hashes.SHA256}`.\n',
    'author': 'Jonas Obrist',
    'author_email': 'jonas.obrist@hennge.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HENNGE/minisignxml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
