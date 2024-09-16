#!/bin/bash

# Define variables
PROJECT_DIR=/home/nath/Documents/Projects/alx_workspace/Linguify
PROJECT_NAME=Linguify
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=awosanminathaniel0@gmail.com
VENV_DIR=$PROJECT_DIR/env
NGINX_CONF=/etc/nginx/sites-available/$PROJECT_NAME
NGINX_ENABLED=/etc/nginx/sites-enabled/$PROJECT_NAME

# Update package lists and install necessary packages
echo "Updating package lists..."
sudo apt update

echo "Installing necessary packages..."
sudo apt install -y nginx python3 python3-pip python3-venv python3-dev libpq-dev build-essential

# Create a virtual environment and activate it
echo "Setting up virtual environment..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Install Django and Gunicorn
echo "Installing Django and Gunicorn and requirements.txt..."
pip install -r requirements.txt
pip install django gunicorn

# Migrate and create superuser for Django
cd $PROJECT_DIR
echo "Running migrations..."
python manage.py migrate

echo "Creating Django superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Deactivate virtual environment
deactivate

# Create Gunicorn systemd service
echo "Setting up Gunicorn systemd service..."
sudo bash -c "cat > /etc/systemd/system/$PROJECT_NAME.service" <<EOF
[Unit]
Description=gunicorn daemon for $PROJECT_NAME
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$VENV_DIR/bin/gunicorn --workers 3 --bind unix:$PROJECT_DIR/$PROJECT_NAME.sock $PROJECT_NAME.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start Gunicorn service
sudo systemctl daemon-reload
sudo systemctl start $PROJECT_NAME
sudo systemctl enable $PROJECT_NAME

# Configure Nginx
echo "Configuring Nginx..."
sudo bash -c "cat > $NGINX_CONF" <<EOF
server {
    listen 80;
    server_name your_server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $PROJECT_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/$PROJECT_NAME.sock;
    }
}
EOF

# Enable Nginx site and restart service
sudo ln -s $NGINX_CONF $NGINX_ENABLED
sudo nginx -t
sudo systemctl restart nginx

echo "Deployment completed successfully!"
