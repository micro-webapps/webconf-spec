# Configuring the web applications in UNIX distribution-like environment

This document describes the benefits of using webconf-spec in the UNIX distribution-like environment. It also shows an example way how to integrate the webconf-spec implementations with the webservers in the distribution.

*This document is not final yet and can change without any notice. For now, it is mainly intended to be a working place where the ideas are put.*

## How is webconf-spec useful for the distribution?

The webserver related configuration files for the web applications can be stored in a single directory shared by the webservers. It is therefore possible to install the web application and let the admin decide with which server he wants to use the web application, because the configuration shipped with the web application is not server-specific anymore.

## Example of webconf-spec in the distribution

The web applications configuration files are installed into following tree in the `/etc` directory:

* `/etc/webapps.d/available/` - Directory containing webconf-spec JSON configuration files for all the web-applications available on the system.
* `/etc/webapps.d/enabled/` - Directory for the enabled web applications containing symbolic links to available configurations from the `/etc/webapps.d/available/` directory.

Once the web application is installed, its webconf-spec configuration file is added into `/etc/webapps.d/available/` directory. When the admin decides to enable to web application, he creates the symbolic link to its configuration file in the `/etc/webapps.d/enabled/` directory.

He can then restart the webserver. The part of restart process (basically the part of the initscript or systemd service file) is the execution of the webconf-spec implementation (like httpd-cfg, haproxy-cfg or nginx-cfg), which generates the native webserver's configuration files from the webconf-spec configuration files located in `/etc/webapps.d/enabled/` directory.
