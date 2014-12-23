# Sherpa Fact UI Installation Guide

## 0. Dependencies

The Sherpa Fact UI has been written to work under Linux, with an Elasticsearch storage back-end.  The application
itself is written in Python and JavaScript, so a Python environment is required on the server.

Install, configure and start Elasticsearch 0.9.x (does not currently work with Elasticsearch 1.x) from [http://www.elasticsearch.org/downloads/0-90-13/](http://www.elasticsearch.org/downloads/0-90-13/) - see also 
the **Security** section below.

## 1. Obtain all the code

Clone the project from github

    git clone https://github.com/CottageLabs/fact.git

get all the submodules

    cd fact
    git submodule init
    git submodule update

This will initialise and clone the submodule dependencies

Then get the submodules for the magnificent-octopus dependency:

    cd fact/magnificent-octopus
    git submodule init
    git submodule update

Create your python virtualenv and activate it

    virtualenv /path/to/venv
    source /path/tovenv/bin/activate

Install esprit and magnificent octopus (in that order)

    cd fact/esprit
    pip install -e .
    
    cd fact/magnificent-octopus
    pip install -e .
    
Create your local config

    cd fact
    touch local.cfg

We will use this later to override localised configuration options.

Finally install the fact application itself into the virtualenv:

    cd fact
    pip install -e .

## 2. Configure the application

The application is already pre-configured for normal usage, but you must provide a Sherpa Romeo API key of your own for interactions with the FACT API to 
succeed.

In fact/local.cfg, insert the following:

    ROMEO_API_KEY = "<your romeo api key>"

If you wish to change any other key settings for the application see the application config: [https://github.com/CottageLabs/fact/blob/master/config/service.py](https://github.com/CottageLabs/fact/blob/master/config/service.py)

Any value in the application config can be overridden in local.cfg

## 3. Initialising the dataset

The journal autocomplete feature requires that the journal list from Romeo be pre-loaded into the Elasticsearch index.

This codebase comes with a version of that Romeo data already in the file "romeo.csv".  If you wish to refresh this, the latest data can be downloaded from Romeo's downloads page: [http://www.sherpa.ac.uk/downloads/](http://www.sherpa.ac.uk/downloads/) (make sure to download the csv version)

To import the data, just run

    python service/scripts/autocomplete_data.py

If you want to use a file you downloaded yourself, with a different name, use

    python service/scripts/autocomplete_data.py -s /path/to/file.csv


## 4. Start the application

### 4a. Start as a default python webapp

**NOT RECOMMENDED FOR PRODUCTION SERVICES**

The application can be started for testing/demonstration with

    cd fact
    python service/web.py

This will start the application on port 5015 (or other, if you have overridden the PORT configuration option).

### 4b. Start as nginx site, with supervisor

**RECOMMENDED FOR PRODUCTION SERVICES**

This approach relies on Supervisor, a process control system [http://supervisord.org/](http://supervisord.org/)

Copy the file

    fact/magnificent-octopus/deploy/site-available

to your nginx sites-available directory, with a suitable name (e.g. sherpa-fact).

Edit this file replacing the placeholders with the appropriate values.

Activate a the application by creating a symlink in your nginx sites-enabled directory to this file.

Copy the file

    fact/magnificent-octopus/supervisor/service.conf
    
to your supervisor configuration directory, with a suitable name (e.g. sherpa-fact.conf)

Edit this file, updating all the commands with the appropriate paths.

Reload your supervised applications with:

    sudo supervisorctl reload

You can then stop/start the application individually with
    
    sudo supervisorctl restart sherpa-fact

Reload the nginx configuration with

    sudo nginx -s reload


## Security Information

* There is no user information transmitted between the client and the server, so the application does not need to run under HTTPS

* The application provides a proxy for the Elasticsearch storage interface, so the Elasticsearch instance only needs to be available to localhost.
This means that connections to port 9200 from outside the server can be safely blocked.

* The JavaScript AJAX requests communicate with the server over port 80

* For extra security, disable Elasticsearch dynamic scripting, by adding the following line to the elasticsearch/config/elasticsearch.yml file:

    script.disable_dynamic: true

