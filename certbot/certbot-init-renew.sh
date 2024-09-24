#!/bin/sh

# Check if certificates already exist
if [ ! -d "/etc/letsencrypt/live/aispong.brookchin.tech" ]; then
    # If not, run initial certificate request
    certbot certonly --webroot --webroot-path /var/www/certbot \
        -d aispong.brookchin.tech --email chunyong96@gmail.com --agree-tos --no-eff-email \
        --force-renewal
else
    # If they exist, try to renew
    certbot renew
fi

# Reload nginx to pick up new certificates
docker exec tcd_nginx nginx -s reload