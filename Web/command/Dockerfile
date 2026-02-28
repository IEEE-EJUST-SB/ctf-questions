# Use the official PHP image with Apache
FROM php:8.2-apache

RUN apt-get update && apt-get install -y \
    libzip-dev \
    zip \
    unzip \
    git \
    iputils-ping
# Enable Apache mod_rewrite (optional)
RUN a2enmod rewrite

# Copy the application code to the Apache document root
COPY ./src/ /var/www/html/

# Set permissions (optional)
RUN chown -R www-data:www-data /var/www/html
