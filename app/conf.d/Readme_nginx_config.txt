#####################################################
### overview
query the API in the usual way, nginx talks to uWSGI sockets, uWSGI communicates internally via sockets

# PORTS
 - agotool master branch on port 5911
 - PMID_autoupdate branch on port 10114 for STRING v11
    -- on San temporarily on 10115 to check if updates roll out smoothly #!!! should be changed to 10114

# uWSGI config
- Sockets and FIFO
    zerg.sock and app.sock (same for zerg.fifo and app.fifo) are used for both branches but are located
    in different directories on the servers (San, Phobos, Pisces, Aquarius)
    but in the same location on Ody
    /scratch/dblyon/agotool/app
    /home/dblyon/agotool_PMID_autoupdate/agotool
    /Users/dblyon/modules/cpr/agotool
- ini files
    zerg_agotool_STRING.ini
    vassal_agotool_STRING.ini
    pytest_agotool_STRING.ini

    zerg_agotool.ini
    vassal_agotool.ini
    pytest_agotool.ini

###
#####################################################


### local version on e.g. Ody to be able to talk to uWSGI socket
installed via homebrew
nginx will load all files in /usr/local/etc/nginx/servers/.
brew services start nginx
brew services stop nginx
brew services list

Important locations:
Add configs in -> /usr/local/etc/nginx/servers/
Default config -> /usr/local/etc/nginx/nginx.conf
Logs will be in -> /usr/local/var/log/nginx/
Default webroot is -> /usr/local/var/www/
Default listen address -> http://localhost:8080

# on Ody
cd /usr/local/etc/nginx
nginx -s reload
#### @ Ody
-------------------------- working v 1 --------------------------
### /usr/local/etc/nginx/servers/agotool_zerg.conf
# agotool_zerg.conf
# nginx.conf

# configuration of the server
server {
    # the port your site will be served on
    listen      5911;
    server_name localhost;

    # the domain name it will serve for
    charset     utf-8;

    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

    location ^~ /static {
      root /Users/dblyon/modules/cpr/agotool/app;
      expires 2h;
      access_log off;
      }

    location / {
      include /Users/dblyon/modules/cpr/agotool/app/conf.d/uwsgi_params;
      uwsgi_pass unix:/Users/dblyon/modules/cpr/agotool/app/app.sock;
    }
}


# zerg_agotool.ini
[uwsgi]
master = true
zergpool = /Users/dblyon/modules/cpr/agotool/app/zerg.sock:/Users/dblyon/modules/cpr/agotool/app/app.sock
safe-pidfile = uwsgi_agotool_zergpool_PID.txt

# vassal_agotool.ini
[uwsgi]
socket = /Users/dblyon/modules/cpr/agotool/app/app.sock
zerg = /Users/dblyon/modules/cpr/agotool/app/zerg.sock
... etc.
-----------------------------------------------------------------


### Docker version A
server {
    listen 80;
    server_name localhost;
    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

    location ^~ /static {
        root /var/www;
        expires 2h;
        access_log off;
    }

    location / {
        proxy_set_header   Host                 $host;
        proxy_set_header   Host                 $http_host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;

        proxy_pass http://flaskapp:5912;
#        proxy_pass http://flaskapp;
        proxy_connect_timeout       6000;
        proxy_send_timeout          6000;
        proxy_read_timeout          6000;
        send_timeout                6000;
        proxy_max_temp_file_size    0;

    }
}

### Docker version B (with 2 apps)

upstream flaskapp {
    server flaskapp_1:5912;
    server flaskapp_2:5912;
}

server {
    listen 80;
    server_name localhost;
    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

    location ^~ /static {
        root /var/www;
        expires 2h;
        access_log off;
    }

    location / {
        proxy_set_header   Host                 $host;
        proxy_set_header   Host                 $http_host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;

        proxy_pass http://flaskapp;
        proxy_connect_timeout       6000;
        proxy_send_timeout          6000;
        proxy_read_timeout          6000;
        send_timeout                6000;
        proxy_max_temp_file_size    0;

    }
}




### @ Aquarius
### @Aquarius: /etc/nginx/sites-available/agotool.org.conf
server {
    listen 80;
    listen [::]:80;

    # for pytest
    listen      5911;
    server_name localhost;

    server_name  agotool.org *.agotool.org;

    error_log   /home/srv/agotool.org/nginx/logs/error.log error;
    access_log  /home/srv/agotool.org/nginx/logs/access.log;

    large_client_header_buffers 4 8m;

    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

#    location / {
#        proxy_pass http://192.168.88.3:5911;
#        proxy_set_header Host $host;
#        add_header Access-Control-Allow-Origin *;
#
#        # pass the original IP:
#        proxy_set_header X-Real-IP $remote_addr;
#        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#    }
#
    location / {
      include /home/dblyon/agotool/app/conf.d/uwsgi_params;
      uwsgi_pass unix:/home/dblyon/agotool/app/app.sock;

      proxy_set_header Host $host;
      add_header Access-Control-Allow-Origin *;

      # pass the original IP:
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    }

    location ^~ /static {
        root /home/dblyon/agotool/app;
        expires 2h;
        access_log off;
    }
}


# install nginx
sudo apt-get install nginx

# add configuration file
sudo vim /etc/nginx/sites-available/agotool_STRING_zerg.conf

# BEGINNING
### @ San
/home/dblyon/install/nginx-1.18.0/deployed/conf/nginx.conf
# /etc/nginx/sites-available/agotool_zerg.conf
# /etc/nginx/sites-available/agotool_STRING_zerg.conf
#
# nginx.conf
# configuration of the server
server {
    # the port your site will be served on
    listen      10114;
    server_name localhost;

    # the domain name it will serve for
    charset     utf-8;

    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

    location ^~ /static {
      root /home/dblyon/PMID_autoupdate/agotool/app;
      expires 2h;
      access_log off;
      }

    location / {
      include /home/dblyon/PMID_autoupdate/agotool/app/conf.d/uwsgi_params;
      uwsgi_pass unix:/home/dblyon/PMID_autoupdate/agotool/app/app.sock;
    }
}
# END

### @ Phobos
# /etc/nginx/sites-available/agotool_PMID_branch_zerg.conf
# nginx.conf
# configuration of the server
server {
    # the port your site will be served on

    # PMID_autoupdates branch for string-db.org
    listen      10114;
    server_name localhost;

    charset     utf-8;

    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

    # string-db.org PMID_autoupdates
    location ^~ /static {
      root /home/dblyon/agotool_PMID_autoupdate/agotool/app;
      expires 2h;
      access_log off;
      }

    location / {
      include /home/dblyon/agotool_PMID_autoupdate/agotool/app/conf.d/uwsgi_params;
      uwsgi_pass unix:/home/dblyon/agotool_PMID_autoupdate/agotool/app/app.sock;
    }
}

server {
    # the port your site will be served on

    # PMID_autoupdates branch for string-db.org
    listen      10116;
    server_name localhost;

    charset     utf-8;

    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

    # string-db.org PMID_autoupdates
    location ^~ /static {
      root /home/dblyon/agotool_PMID_autoupdate/agotool/app;
      expires 2h;
      access_log off;
      }

    location / {
      include /home/dblyon/agotool_PMID_autoupdate/agotool/app/conf.d/uwsgi_params;
      uwsgi_pass unix:/home/dblyon/agotool_PMID_autoupdate/agotool/app/app_pytest.sock;
    }
}

sudo ln -s /etc/nginx/sites-available/agotool_PMID_branch_zerg_pytest.conf /etc/nginx/sites-enabled/

# create symlink
sudo ln -s /etc/nginx/sites-available/agotool_STRING_zerg.conf /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/agotool_PMID_branch_zerg.conf /etc/nginx/sites-enabled/


# start/restart nginx
sudo systemctl start nginx

# ! uncomment "default" nginx config !
# debug with
nginx -t
# or
sudo systemctl status nginx

# could be that there is an issue running nginx
# comment out "default" config of nginx because of port 80 and potentially give additional rights
sudo chown -R www-data:www-data /var/log/nginx;
sudo chmod -R 755 /var/log/nginx;




#### Phobos
dblyon@phobos /etc/nginx/sites-available
% cat agotool_PMID_branch_zerg.conf
# nginx.conf

# configuration of the server
server {
    # the port your site will be served on

    # PMID_autoupdates branch for string-db.org
    listen      10114;
    server_name localhost;

    charset     utf-8;

    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;


    # string-db.org PMID_autoupdates
    location ^~ /static {
      root /home/dblyon/agotool_PMID_autoupdate/agotool/app;
      expires 2h;
      access_log off;
      }

    location / {
      include /home/dblyon/agotool_PMID_autoupdate/agotool/app/conf.d/uwsgi_params;
      uwsgi_pass unix:/home/dblyon/agotool_PMID_autoupdate/agotool/app/app.sock;
    }
}

###
dblyon@phobos /etc/nginx/sites-available
% cat agotool_master_branch_zerg.conf
# nginx.conf

# configuration of the server
server {
    # the port your site will be served on

    # master branch for agotool.org
    listen      5911;

    charset     utf-8;

    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

    # agotool.org master
    location ^~ /static {
      root /scratch/dblyon/agotool/app;
      expires 2h;
      access_log off;
      }

    location / {
      include /scratch/dblyon/agotool/app/conf.d/uwsgi_params;
      uwsgi_pass unix:/scratch/dblyon/agotool/app/app.sock;
    }

}