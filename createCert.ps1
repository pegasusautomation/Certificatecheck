New-SelfSignedCertificate -DnsName *.test.com -CertStoreLocation cert:\CurrentUser\My -NotAfter (Get-Date).AddYears(3)