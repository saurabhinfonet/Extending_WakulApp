
Changes made mostly in importer.py,directory.html,map.html,left_aside.html, views.py,url.py.. Added sentimental_analysis.html, first_nation.html, map2.html.
In importer.py there is an addition to import the data for stating type and description of outlet , articles urls, and uncommenting outlet data import.


# These are the packages to download before running the system.
# Installing wa-django on Ubuntu 16.04 LTS

## Install Python packages
`sudo apt-get install python-dev python-pip python3-pip`  
`sudo apt-get install git`

## Install PostGreSQL
`sudo apt-get install libpq-dev postgresql postgresql-contrib`

### Install geospatial libraries for PostGIS
[Django Documentation - Installing Geospatial libraries](https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/#geosbuild)

#### GEOS
`wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2`  
`tar xjf geos-3.4.2.tar.bz2`  
`cd geos-3.4.2`  
`./configure`  
`make`  
`sudo make install`  
`cd ..`

#### PROJ.4
`wget http://download.osgeo.org/proj/proj-4.9.1.tar.gz`  
`wget http://download.osgeo.org/proj/proj-datumgrid-1.5.tar.gz`  
`tar xzf proj-4.9.1.tar.gz`  
`cd proj-4.9.1/nad`  
`tar xzf ../../proj-datumgrid-1.5.tar.gz`  
`cd ..`  
`./configure`  
`make`  
`sudo make install`  
`cd ..`

#### GDAL
`wget http://download.osgeo.org/gdal/2.1.0/gdal-2.1.0.tar.gz`  
`tar xzf gdal-2.1.0.tar.gz`  
`cd gdal-2.1.0`  
`./configure`  
`make`  
`sudo make install`  
`cd ..`  

### Make a PostGreSQL database
[Digital Ocean - How to use PostGreSQL with your Django application on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)

`sudo su - postgres`  
`psql`  
`CREATE DATABASE wakulapp;`  
`CREATE USER wadmin WITH PASSWORD 'password';`  
`ALTER ROLE wadmin SET client_encoding TO 'utf8';`  
`ALTER ROLE wadmin SET default_transaction_isolation TO 'read committed';`  
`ALTER ROLE wadmin SET timezone TO 'UTC';`  
`GRANT ALL PRIVILEGES ON DATABASE wakulapp TO wadmin;`  
`\q`  
`exit`  

### Install PostGIS
`sudo apt-get install postgresql-9.5-postgis-2.2`  
`sudo apt-get install postgresql-server-dev-9.5`

#### Bunch of libraries that helped
`sudo apt-get install libgeoip1 python-gdal binutils libproj-dev gdal-bin libxml2-dev libgdal1-dev liblwgeom-2.2-5 liblwgeom-dev`

#### Install PostGIS from source
`wget http://postgis.net/stuff/postgis-2.2.6dev.tar.gz`  
`tar xvfz postgis-2.2.6dev.tar.gz`  
`cd postgis-2.2.6dev/`  
`./configure`  
`make`  
`sudo make install` 
`sudo ldconfig` 
`cd ..`

#### Add the PostGIS extension to our database
`sudo su - postgres`  
`psql wakulapp`  
`CREATE EXTENSION postgis;`  
`\q`  
`exit`

## Install Python libraries

`sudo pip install Django==1.10.2`  
`sudo pip install psycopg2==2.6.2`  
`sudo pip install django-el-pagination==3.0.1`  
`sudo pip install PyYAML==3.10`  
`sudo pip install CouchDB==1.1`

# Database migrations
`python manage.py collectstatic --noinput --clear`  
`python manage.py makemigrations news`  
`python manage.py migrate`

# Launching the development server
`python3 manage.py runserver 127.0.0.1:8000`

# Installing WSGI
`sudo apt-get install libapache2-mod-wsgi`
