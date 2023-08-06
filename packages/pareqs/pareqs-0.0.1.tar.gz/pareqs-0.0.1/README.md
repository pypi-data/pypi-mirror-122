# PaReqs

Tool to decode 3DS PaReq and PaRes in Python classes or dict

### Why

I want to try to make a Rust extension module in python for decoding

_**UPD**: inflation (decompression) in Rust lasts 20 times longer 🤡_


### Example PaRes

```xml
<ThreeDSecure>
    <Message id="e8ada3517761a9503f29e3afe2be56d6">
        <PARes id="msg.469297.signed">
            <version>1.0.2</version>
            <Merchant>
                <acqBIN>526571</acqBIN>
                <merID>02000000000</merID>
            </Merchant>
            <Purchase>
                <xid>MDAwMDAwMDAwMDEyMzQ1Njc4OTA=</xid>
                <date>20150216 10:17:41</date>
                <purchAmount>21601</purchAmount>
                <currency>208</currency>
                <exponent>2</exponent>
            </Purchase>
            <pan>0000000000001548</pan>
            <TX>
                <time>20150216 10:17:23</time>
                <status>Y</status>
                <cavv>jI3JBkkaQ1p8CBAAABy0CHUAAAA=</cavv>
                <eci>02</eci>
                <cavvAlgorithm>3</cavvAlgorithm>
            </TX>
        </PARes>
        <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
            <SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
                <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod>
                <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod>
                <Reference URI="#msg.469297.signed">
                    <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></DigestMethod>
                    <DigestValue>68M2cV0KugBAhzZsAXl2skj1o8c=</DigestValue>
                </Reference>
            </SignedInfo>
            <SignatureValue>rTEJqWKKFwIOv9Pstc5UygM6sEJQjgTaswur5hXgUoxLNmbF
fl+ZaMBZah4vFmtWwVVDBTWcY8wHqwo1qlGI988iFwuVlmcv
15l3DZeu46PEoes0Rg9LtXSvYcHGFUF/S+xWYzlOVTaxfCHs
w2cXEN2N+UTWlE59j+uOJ3y+XfI=
</SignatureValue>
            <KeyInfo>
                <X509Data>
                    <X509Certificate>MIID3jCCAsagAwIBAgIQGnfEoHXDJBbKvINHTsU2ajANBgkqhkiG9w0BAQUFADCBhjELMAkGA1UEBhMCVVMxHTAbBgNVBAoTFE1hc3RlckNhcmQgV29ybGR3aWRlMS4wLAYDVQQLEyVNYXN0ZXJDYXJkIFdvcmxkd2lkZSBTZWN1cmVDb2RlIEdlbiAyMSgwJgYDVQQDEx9QUkQgTUMgU2VjdXJlQ29kZSBJc3N1ZXIgU3ViIENBMB4XDTEzMTExMzEwNDAxM1oXDTE3MTExMzEwNDAxM1owXDELMAkGA1UEBhMCU0UxETAPBgNVBAoTCFNFQmFua2VuMRcwFQYDVQQLEw5BcmNvdDNEU2VydmljZTEhMB8GA1UEAxMYU0VCTWFzdGVyQ2FyZCBTZWN1cmVjb2RlMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDOw4zwtu2PlgWH6e5VIOgU2gfntaXC2fx44Glx6OvvABvv8vWglzxsncb7uqBZtCTiQ7tjUnZqIZTkwicqG7aIIa9hANiiI/yD1/d564ch1NljIx5gNq1sdI8EoKxnLPA3MYE/pIi3tDlYgj+tccg0z3HtHRgl7Fbf0M4hlpy7lQIDAQABo4H0MIHxMIGmBgNVHSMEgZ4wgZuhgYakgYMwgYAxCzAJBgNVBAYTAlVTMR0wGwYDVQQKExRNYXN0ZXJDYXJkIFdvcmxkd2lkZTEuMCwGA1UECxMlTWFzdGVyQ2FyZCBXb3JsZHdpZGUgU2VjdXJlQ29kZSBHZW4gMjEiMCAGA1UEAxMZUFJEIE1DIFNlY3VyZUNvZGUgUm9vdCBDQYIQQ3EBfDozHhKp3pmzcHr6ZzAJBgNVHRMEAjAAMA4GA1UdDwEB/wQEAwIHgDArBgNVHRAEJDAigA8yMDEzMTExMzEwNDAxM1qBDzIwMTYxMTEyMTA0MDEzWjANBgkqhkiG9w0BAQUFAAOCAQEAWHlaXtaQFoxib+7E324QXMYE2e6fjZ4bPBNSYC4qkU0DOUO6WE1QECD9sfsEsABRNK/rYKwcv7ErfD0YV4j487CdtN+TlPBI45ct7qMtYTd1DwmhPxyuV5BlpttrvVT1cWjLQCnorsiqc+wP/gpn+6HJD5T47FmoUn7JAjbY6KfSUAcKLNV+mxH1hCg5dEIJkARU5ep8aWPkBiORETeFS0YLjoR2Z1P1X0eteUxVrPMDedJVMXeqTSKk5T5BgSG9cJgzOuQlgwyjV+1h8HFoMUo198icAYfkJ5CNuVcBXGi1GJWCN5Sf5zj9NxC05AeWCR7mcxYuhzXUCjMFG52M7g==</X509Certificate>
                    <X509Certificate>MIIDzzCCAregAwIBAgIRAO6hkq6XAdKvA5IMAj3E95MwDQYJKoZIhvcNAQEFBQAwgYAxCzAJBgNVBAYTAlVTMR0wGwYDVQQKExRNYXN0ZXJDYXJkIFdvcmxkd2lkZTEuMCwGA1UECxMlTWFzdGVyQ2FyZCBXb3JsZHdpZGUgU2VjdXJlQ29kZSBHZW4gMjEiMCAGA1UEAxMZUFJEIE1DIFNlY3VyZUNvZGUgUm9vdCBDQTAeFw0xMjA2MjIwOTA4MzBaFw0yNTA2MjIwOTA4MzFaMIGAMQswCQYDVQQGEwJVUzEdMBsGA1UEChMUTWFzdGVyQ2FyZCBXb3JsZHdpZGUxLjAsBgNVBAsTJU1hc3RlckNhcmQgV29ybGR3aWRlIFNlY3VyZUNvZGUgR2VuIDIxIjAgBgNVBAMTGVBSRCBNQyBTZWN1cmVDb2RlIFJvb3QgQ0EwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDptCms6aI22T9ST60k487SZP06TKbUBpom7Z1Bo8cQQAE/tM5UOt3THMdrhT+2aIkj9T0pA35IyNMCNGDt+ejhy7tHdw1r6eDX/KXYHb4FlemY03DwRrkQSH/L+ZueS5dCfLM3m2azxBXtrVXDdNebfht8tcWRLK2Ou6vjDzdIzunuWRZ6kRDQ6oc1LSVO2BxiFO0TKowJP/M7qWRT/Jsmb6TGg0vmmQG9QEpmVmOZIexVxuYy3rn7gEbV1tv3k4aG0USMp2Xq/Xe4qe+Ir7sFqR56G4yKezSVLUzQaIB/deeCk9WU2T0XmicAEYDBQoecoS61R4nj5ODmzwmGyxrlAgMBAAGjQjBAMA8GA1UdEwQIMAYBAf8CAQEwDgYDVR0PAQH/BAQDAgEGMB0GA1UdDgQWBBQqFTcxVDO/uxI1hpFF3VSSTFMGujANBgkqhkiG9w0BAQUFAAOCAQEAhDOQ5zUX2wByVv0Cqka3ebnm/6xRzQQbWelzneDUNVdctn1nhJt2PK1uGV7RBGAGukgdAubwwnBhD2FdbhBHTVbpLPYxBbdMAyeC8ezaXGirXOAAv0YbGhPl1MUFiDmqSliavBFUs4cEuBIas4BUoZ5Fz042dDSAWffbdf3l4zrU5Lzol93yXxxIjqgIsT3QI+sRM3gg/Gdwo80DUQ2fRffsGdAUH2C/8L8/wH+E9HspjMDkXlZohPII0xtKhdIPWzbOB6DOULl2PkdGHmJc4VXxfOwE2NJAQxmoaPRDYGgOFVvkzYtyxVkxXeXAPNt8URR3jfWvYrBGH2D5A44Atg==</X509Certificate>
                    <X509Certificate>MIIEgDCCA2igAwIBAgIQQ3EBfDozHhKp3pmzcHr6ZzANBgkqhkiG9w0BAQUFADCBgDELMAkGA1UEBhMCVVMxHTAbBgNVBAoTFE1hc3RlckNhcmQgV29ybGR3aWRlMS4wLAYDVQQLEyVNYXN0ZXJDYXJkIFdvcmxkd2lkZSBTZWN1cmVDb2RlIEdlbiAyMSIwIAYDVQQDExlQUkQgTUMgU2VjdXJlQ29kZSBSb290IENBMB4XDTEyMDYyMjA5MjIxNFoXDTI1MDYyMTA5MjIxNVowgYYxCzAJBgNVBAYTAlVTMR0wGwYDVQQKExRNYXN0ZXJDYXJkIFdvcmxkd2lkZTEuMCwGA1UECxMlTWFzdGVyQ2FyZCBXb3JsZHdpZGUgU2VjdXJlQ29kZSBHZW4gMjEoMCYGA1UEAxMfUFJEIE1DIFNlY3VyZUNvZGUgSXNzdWVyIFN1YiBDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANaeBgfjTKIFls7ueMTzI2nYwAbocHwkQqd8BsIyJbZdk21E+vyq9EhX1NIoiAhP7fl+y/hosX66drjfrbyspZLalrVG6gYbdB2j2Sr8zBRQnMZKKluDwYv/266nnRBeyGYW3FwyVu8L1ACYQc04ACke+07NI/AZ8OXQSoeboEEGUO520/76o1cER5Ok9HRi0jJD8E64j8dEt36Mcg0JaKQiDjShlyTw4ABYyzZ1Vxl0/iDrfwboxNEOOooC0rcGNnCpISXMWn2NmZH1QxiFt2jIZ8QzF3/z+M3iYradh9uZauleNqJ9LPKr/aFFDbe0Bv0PLbvXOnFpwOxvJODWUj8CAwEAAaOB7TCB6jAPBgNVHRMECDAGAQH/AgEAMA4GA1UdDwEB/wQEAwIBBjAdBgNVHQ4EFgQUwTArnR3hR1+Ij1uxMtqoPBm2j7swgacGA1UdIwSBnzCBnKGBhqSBgzCBgDELMAkGA1UEBhMCVVMxHTAbBgNVBAoTFE1hc3RlckNhcmQgV29ybGR3aWRlMS4wLAYDVQQLEyVNYXN0ZXJDYXJkIFdvcmxkd2lkZSBTZWN1cmVDb2RlIEdlbiAyMSIwIAYDVQQDExlQUkQgTUMgU2VjdXJlQ29kZSBSb290IENBghEA7qGSrpcB0q8DkgwCPcT3kzANBgkqhkiG9w0BAQUFAAOCAQEA3lJuYVdiy11ELUfBfLuib4gPTbkDdVLBEKosx0yUDczeXoTUOjBEc90f5KRjbpe4pilOGAQnPNUGpi3ZClS+0ysTBp6RdYz1efNLSuaTJtpJpoCOk1/nw6W+nJEWyDXUcC/yVqstZidcOG6AMfKU4EC5zBNELZCGf1ynM2l+gwvkcDUv4Y2et/n/NqIKBzywGSOktojTma0kHbkAe6pj6i65TpwEgEpywVl50oMmNKvXDNMznrAG6S9us+OHDjonOlmmyWmQxXdU1MzwdKzPjHfwl+Z6kByDXruHjEcNsx7P2rUTm/Bt3SWW1K48VfNNhVa/WctTZGJCrV3Zjl6A9g==</X509Certificate>
                </X509Data>
            </KeyInfo>
        </Signature>
    </Message>
</ThreeDSecure>
```

```xml
<ThreeDSecure>
    <Message id="msg.1">
        <PARes id="d8349afe-58ae-46b4-a756-cb37e0cceed1">
            <version>1.0.2</version>
            <Merchant>
                <acqBIN>427600</acqBIN>
                <merID>7</merID>
            </Merchant>
            <Purchase>
                <xid>MDAwMDAwMDEzOTkyOTE1NzIwNzk=</xid>
                <date>20140505 16:06:12</date>
                <purchAmount>250000</purchAmount>
                <currency>643</currency>
                <exponent>2</exponent>
            </Purchase>
            <pan>0000000000001111</pan>
            <TX>
                <time>20140505 16:06:12</time>
                <status>Y</status>
                <cavv>AAABB3dzMhOZKRY3MyAAAAAAAAA=</cavv>
                <eci>05</eci>
                <cavvAlgorithm>2</cavvAlgorithm>
            </TX>
        </PARes>
        <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
            <SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
                <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod>
                <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod>
                <Reference URI="#d8349afe-58ae-46b4-a756-cb37e0cceed1">
                    <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></DigestMethod>
                    <DigestValue>EczgF+fG8fz33EDS+Dhgg91G3iM=</DigestValue>
                </Reference>
            </SignedInfo>
            <SignatureValue>hEOqSRAUG2jSHiqjThJDLGvBf0dc26WXhygDNXmYnQsWg+LILV/mh5OzwAdHD4du4yYM5IFisUg5OkFeC0Gz7x9rwePmD4CsU0teN10PFBaE0sSqZtR3qVIVtQFCJyD4nSymOb9CMcMx9UJvLgcgszqYUaW5bwpTxY17VNJHnbg=</SignatureValue>
            <KeyInfo>
                <X509Data>
                    <X509Certificate>MIICoTCCAgqgAwIBAgIJAPnFSzeYi+lbMA0GCSqGSIb3DQEBBQUAMEAxCzAJBgNVBAYTAlVTMRAwDgYDVQQKEwdDYXJhZGFzMQwwCgYDVQQLEwNQSVQxETAPBgNVBAMTCHBpdC1yb290MB4XDTE0MDMwNjA0MzUxMFoXDTI0MDMwMzA0MzUxMFowQDELMAkGA1UEBhMCVVMxEDAOBgNVBAoTB0NhcmFkYXMxDDAKBgNVBAsTA1BJVDERMA8GA1UEAxMIcGl0LXJvb3QwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAKG7diarDQg17UjmvJasHFSjWhPdb9/9pXZvWAKuc9wqqjD3nvU6w+uJtYIFqN4vXC+jk7ek4VF7jvkDF3R00fnHl6wOVufzQlFA7+QXpWTMGsb6yywhXMwVbcO8u14cGV/x+5VewkTgrVRbqZlOXImellNvW1fsJ5HiSVfH8eylAgMBAAGjgaIwgZ8wHQYDVR0OBBYEFNk33h9Q1BGfio7uxKNe2lYd1HuJMHAGA1UdIwRpMGeAFNk33h9Q1BGfio7uxKNe2lYd1HuJoUSkQjBAMQswCQYDVQQGEwJVUzEQMA4GA1UEChMHQ2FyYWRhczEMMAoGA1UECxMDUElUMREwDwYDVQQDEwhwaXQtcm9vdIIJAPnFSzeYi+lbMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEAIeZZtXQqlBK04a2gimGko/aL2YWMRgh04yTK+jw7OkJ/UWdA1g78UJk5/rTJ92579io5rsmLHXV+uWc6Wr6IFO4AfxiQv+GW/PMQ8pu49o8ev9yTvYaos8XP4zdUO4RsXBw9rYRuSP4Ov2tOKKPomOJLabS58GAlCouk774/xTE=</X509Certificate>
                    <X509Certificate>MIICnzCCAgigAwIBAgIJANhcG/IeHwt9MA0GCSqGSIb3DQEBBQUAMEAxCzAJBgNVBAYTAlVTMRAwDgYDVQQKEwdDYXJhZGFzMQwwCgYDVQQLEwNQSVQxETAPBgNVBAMTCHBpdC1yb290MB4XDTE0MDMwNjA0NDYzN1oXDTI0MDMwMzA0NDYzN1owPjELMAkGA1UEBhMCVVMxEDAOBgNVBAoTB0NhcmFkYXMxDDAKBgNVBAsTA1BJVDEPMA0GA1UEAxMGcGl0LWNhMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDS8wkuFUF4kaaiaSL+R56Vakz1ulgoYFq/EoXJzLSw0AtaW81eHuChye87XgDGPXuAECobKR1po7jmmv7N1mqolxdLttAo5KIrW9eON6+/+3S4tIkuKrq+6VLTyxS5tm7HtIk3VHgOauYqZAwdCxSFqIuFjsujhs+XXxvwBuo5swIDAQABo4GiMIGfMB0GA1UdDgQWBBSSeO/Apvd/IYPohAgH1IdESNp/KDBwBgNVHSMEaTBngBTZN94fUNQRn4qO7sSjXtpWHdR7iaFEpEIwQDELMAkGA1UEBhMCVVMxEDAOBgNVBAoTB0NhcmFkYXMxDDAKBgNVBAsTA1BJVDERMA8GA1UEAxMIcGl0LXJvb3SCCQD5xUs3mIvpWzAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUAA4GBACtXB0vtl0+QUUvHGlo8gqCwjjhwDLpa2VRslausKGt84WlPiX0TH2Bqxm/zmPyBjNnuXWGHmQ4KgFmqa0SeF1AfP/Y3AWeEJA6Joej58nG0hr6CcObxrC+wAMRPDIlLHO+51QyjpNF9HC+k26bxUapZs2VW/2pcP67mtQHyXiYQ</X509Certificate>
                    <X509Certificate>MIIB+TCCAWKgAwIBAgIUM9IGJukCXu4+dnuLcyZEyKu488gwDQYJKoZIhvcNAQEFBQAwPjELMAkGA1UEBhMCVVMxEDAOBgNVBAoTB0NhcmFkYXMxDDAKBgNVBAsTA1BJVDEPMA0GA1UEAxMGcGl0LWNhMB4XDTE0MDQxNjA4NTAxNFoXDTE1MDQxNjA4NTAxNFowIjEgMB4GA1UEAxMXVmlzYSBTdHJhbmdlIEV4cGlyeSBOZXcwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAIYGrQ0qMKnCbsTk4wSBinwHF9+GqtXPLj1CYK2SdmnDtM09z6ewuvLQtmcOyFvut1/B2kuQRGreSf8/G7bspFnQQWhChcS+DmA/H0OUrKiYOgBiUICL4iLgjTbdfFApeD4Fkoem15f2VlO86rVo75NsA1xXZVD0rejOfAgBfNTvAgMBAAGjEDAOMAwGA1UdEwEB/wQCMAAwDQYJKoZIhvcNAQEFBQADgYEANNd6/PTy7+qgNSJZgsb0Hni/5QiFQOku0ML354bCHmIMceh4JF/y+9ARDdISOhaN4TOS562MzY/KMlkIw/kDSEFbrgax5qsvyQDiDVu4a1IepRjc2qVsBwE2aeVJ+1M7PjnLzwpbVrzQSWSHuYwUbjRFj6oakyXFNuPWu6mb9R0=</X509Certificate>
                </X509Data>
            </KeyInfo>
        </Signature>
    </Message>
</ThreeDSecure>
```
