"""All the steps in building a webservice for alexa suck."""

import sys
import os
import os.path


CERT_CONF_TEMPLATE = """
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = NY
L = Who cares
O = Who cares
CN = Who cares

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @subject_alternate_names

[subject_alternate_names]
DNS.1 = {domain_name}
"""


NGINX_TEMPLATE = """
server {{
    listen 443;
    ssl on;
    ssl_certificate /etc/ssl/{hostname}.pem;
    ssl_certificate_key /etc/ssl/{hostname}.key;

    server_name {hostname};
    location /alexacast/ {{
        proxy_pass http://localhost:8080/$uri
    }}
}}
"""


def generate_certificate():
    """Generate the TLS private key and certificate"""
    hostname = raw_input('DNS Hostname: ')

    print '>> generating private key'
    os.system("openssl genrsa -out key.pem 2048")

    with open('cert.conf', 'w') as fp:
        fp.write(CERT_CONF_TEMPLATE.format(domain_name=hostname))

    print '>> creating certificate'
    os.system("openssl req -new -x509 -key key.pem \
-config cert.conf -out server.crt")

    print '>> writing nginx template'
    with open('alexacast.nginx.conf', 'w') as fp:
        NGINX_TEMPLATE.format(hostname=hostname)

    print '''
    up to you now depending on your setup.

    probably something like this:

    sudo cp alexacasst.nginx.conf /etc/nginx/sites-enabled/alexacast.conf
    sudo service nginx restart
    '''


if __name__ == '__main__':
    out_dir = raw_input('Output directory: ')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    os.chdir(out_dir)

    generate_certificate()
