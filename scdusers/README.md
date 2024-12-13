# Cert stuff.

openssl genpkey -algorithm RSA -out ca.key -aes256
openssl req -x509 -new -nodes -key ca.key -out ca.crt -days 3650 -config openssl-ca.cnf
openssl genpkey -algorithm RSA -out john.key -aes256
openssl genpkey -algorithm RSA -out jane.key -aes256
openssl req -new -key john.key -out john.csr
openssl req -new -key jane.key -out jane.csr
openssl x509 -req -in john.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out john.pem -days 3650 -sha256
openssl x509 -req -in jane.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out jane.pem -days 3650 -sha256

keys for john and jane (code demo accounts) are encrypted with their user password.

Ideally the code would do this for them, create stuff and stuff, but I can't be bothered to figure 
out how to do that especially since we were told we could make the certs outside the code.