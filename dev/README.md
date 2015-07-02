Table of Contents
=================

*This is development version of the webconf-spec and can change without any previous notice.*

  * [What is webconf-spec?](#what-is-webconf-spec)
  * [What is it useful for?](#what-is-it-useful-for)
  * [Are there any implementation already?](#are-there-any-implementation-already)
  * [Description of webconf-spec specification](#description-of-webconf-spec-specification)
    * [General options](#general-options)
    * [Redirect option](#redirect-option)
    * [Proxy options](#proxy-options)
    * [Match option](#match-option)
    * [Directories option](#directories-option)
    * [Locations option](#locations-option)
    * [Merging the webconf-spec formatted files](#merging-the-webconf-spec-formatted-files)
  * [Examples of webconf-spec specification](#examples-of-webconf-spec-specification)
    * [Serving the static directory on http://domain.tld/static](#serving-the-static-directory-on-httpdomaintldstatic)
    * [Serving the static directory with SSL support](#serving-the-static-directory-with-ssl-support)
    * [Serving the static directory with SSL support, redirecting HTTP to HTTPS](#serving-the-static-directory-with-ssl-support-redirecting-http-to-https)
    * [The default Wordpress configuration as seen in Fedora](#the-default-wordpress-configuration-as-seen-in-fedora)
    * [Proxying the webapp.domain.tld to another HTTP server](#proxying-the-webappdomaintld-to-another-http-server)
    * [Proxying the PHP files in http://domain.tld/blog to php-fpm server](#proxying-the-php-files-in-httpdomaintldblog-to-php-fpm-server)

# What is webconf-spec?
Webconfig-spec is specification of webserver configuration for web applications configuration. The goal of webconf-spec is to provide a way how to configure widely used webservers or proxies like Apache httpd, Nginx or HAProxy using the single configuration file.

# What is it useful for?

It can be used to create web applications without dependency on any particular webserver implementation. In this case, the web application developer writes single configuration file in JSON, which is translated to the particular webserver's configuration on the user's machine when he deploys the application. This is achieved by the webconf-spec implementation shipped together with the webserver.

# Are there any implementation already?

Yes, we have following implementations generating the native webserver's configuration from the webconf-spec files:

- [httpd-cfg](https://github.com/micro-webapps/httpd-cfg) - Reads the .json webconf-spec files from input directory and generates the Apache httpd configuration in the output directory.
- [haproxy-cfg](https://github.com/micro-webapps/haproxy-cfg) - Reads the .json webconf-spec files from input directory and generates the HAProxy configuration in the output directory.
- [nginx-cfg](https://github.com/micro-webapps/nginx-cfg) - Reads the .json webconf-spec files from input directory and generates the nginx configuration in the output directory.

# Description of webconf-spec specification

It is important to note that the webconf-spec is not trying to be full featured webserver configuration specification. Usually, the web applications do not use all features of the webservers and therefore we have tried to keep things simple and support only features which are widely used by web applications to configure the webserver and which are shared between all widely used webservers.

## General options

This section describes the general webconf-spec JSON fields. They are used only in the root JSON object, except of the `index` option, which can be used in the in other JSON objects as described later in this specification. 

| Key | Type | Meaning |
|-----|------|---------|
| certificate | String | The full path to file containing the certificate to be used for the virtualhost or server. When using this option, the SSL for this virtualhost or server will be enabled. |
| certificate_key | String | The full path to file containing the certificate key to be used for the virtualhost or server. When using this option, the SSL for this virtualhost or server will be enabled. |
| document_root | String | The full path to directory acting as root directory for the virtualhost or server. |
| index | String | Name (or white-space seperated list of names) of the files which should be server by default when found in directory ("index.html" for example). It can be also set to value `disabled` to disable to the index file completely. The value of `autoindex` will enable automatic generation of indexes similar to the Unix ls command or the Win32 dir shell command. |
| version | String | The version of the webconf-spec used in this configuration file. For the development version of webconf-spec, the value of this option should be set to "dev". |
| virtualhost | String | Virtual host on which the web application should run. |


If the virtualhost option is set to an empty string or is not defined, the webconf-spec implementation should treat all the options as global (It means not bound to any virtualhost). If any of the other options is set to an empty string or is not defined, the webconf-spec implementation should ignore the option completely.

## Redirects option

This section describes redirects option used to redirect from one URL or path to another URL. The Redirect option can be used only in the root object of the webconf-spec.

The format of directories option is following:

    "redirects": {
        "/from/url": {
            "option1": "value",
            "option2": "value"
        },
        "/from/another/url": {
            "option1": "value",
            "option2": "value"
        }
    }

The special options which can be used in redirect option are:

| Key | Type | Meaning |
|-----|------|---------|
| to | String | The URL to which the client is redirected. |

## Proxy options

This section describes the proxy related webconf-spec JSON fields. They can be used in the root section of webconf-spec or in "directories" or "locations" section as described later in this document.

| Key | Type | Meaning |
|-----|------|---------|
| proxy_protocol | String | The protocol used to connect the backend server. For example "http://", "fcgi://" or "ajp://". |
| proxy_alias | String | The alias location of the web application on the frontend server. If the web application should be accessible on "http://domain.tld/blog", then the value of this option should be "/blog". |
| proxy_backend_alias | String | The alias location of the web application on the backend server. If the web application backend is accessible on "http://internal.domain.tld/wordpress", then the value of this option should be "/wordpress". |
| proxy_hostname | String | The hostname or IP address of the backend server running the web application. If the web application backend is accessible on "http://internal.domain.tld/wordpress", then the value of this option should be "internal.domain.tld". |
| proxy_port | String | The port of the backend server running the web application. |

If the proxy_protocol option is set to an emptry string or is not defined, but all the other options needed to proxy the requests are specified, the webconf-spec implementation should use "http://" as default. If the proxy_alias or the proxy_backend_alias options are set to an emptry string or are not defined, the webconf-spec implementation should use "/" string as default value.

## Match option

This section describes the match option. This option is used to match files served by the webserver based on their names and configure the way webserver handle them. All the Proxy options can be used in the Match option.

    "match": {
        "\\.regex_to_match_the_files$": {
            "option1": "value",
            "option2": "value"
        },
        "\\.php$": {
            "option1": "value",
            "option2": "value"
        }
    }

The special options which can be used in Match option are:

| Key | Type | Meaning |
|-----|------|---------|
| allow | String | Word defining the access permision to the files matching the Match option. The "all" value allows all web clients to access the files. The "local" value allows only users from localhost to access the files. Any other value denies anyone to access the file. |


This allows for example proxying the PHP files to php-fpm server:

    "match": {
        "\\.php$": {
            "proxy_protocol": "fcgi://",
            "proxy_backend_alias": "/wordpress/$1",
            "proxy_hostname": "localhost",
            "proxy_port:", "9000",
            "allow": "all"
        }
    }

## Directories option

This section describes the directories related webconf-spec JSON options. Directories are used to configure the real directories on the webserver. Per-directory configuration set by this option is applied to all sub-directories of the main directory. All the Proxy options and Match option can be used in the Directories options as well as the "index" option.

The format of directories option is following:

    "directories": {
        "/full/path/to/directory": {
            "option1": "value",
            "option2": "value"
        },
        "/full/path/to/another/directory": {
            "option1": "value",
            "option2": "value"
        }
    }

The special options which can be used in Directories option are:

| Key | Type | Meaning |
|-----|------|---------|
| Alias | String | Sets the alias for the directory. If the directory should be accessible as "http://domain.tld/blog", then the value of this option should be "/blog".|


If Match option appears in the Directories option, all the files matching the regular expression in the main directory or its sub-directories should be configured by this Match option.

Using Directories option, it is for example possible to disable access to particular files in particular directory:

    {
        "directories": {
            "/usr/share/wordpress/wp-content/plugins/akismet": {
                "match": {
                    "regex": "\\.(php|txt)$",
                    "allow": "none"
                }
            }
        }
    }

Or it is for example possible to serve static local directory as "http://domain:.tld/static":

    {
        "virtualhost": "domain.tld",
        "directories": {
            "/var/www/my-static-dir": {
                "alias": "/static"
            }
        }
    }

## Locations option

This section describes the locations options. Locations are used to configure the non-real paths on the webserver as they are used in the HTTP requests. Per-location configuration set by this option is applied to all sub-locations of the main location. All the Proxy options and Match option can be used in the Locations options as well as the "index" option.

The format of locations option is following:

    "locations": {
        "/first/location": {
            "option1": "value",
            "option2": "value"
        },
        "/second/location": {
            "option1": "value",
            "option2": "value"
        }
    }

If Match option appears in the Locations option, all the files matching the regular expression in the main location or its sub-locations should be configured by this Match option.

## Merging the webconf-spec formatted files

Although the webconf-spec describes the configuration of the single web application, all the implementations must expect the set of webconf-spec formatted files as the input. This allows to configure multiple web applications running on the single virtualhost served in different locations. In case of two config files with the same options which are in contrast to each other, the implementation should treat it as an error.

# Examples of webconf-spec specification

This sections contains few commented examples of the webconf-spec configuration files.

## Serving the static directory on http://domain.tld/static

    {
        "version": "dev",
        "virtualhost": "domain.tld",
        "directories": {
            "/var/www/my-static-dir": {
                "alias": "/static"
            }
        }
    }

## Serving the static directory with SSL support

    {
        "version": "dev",
        "virtualhost": "domain.tld",
        "certificate": "/etc/pki/tls/certs/domain.tld.crt",
        "certificate_key": "/etc/pki/tls/private/domain.tld.key",
        "directories": {
            "/var/www/my-static-dir": {
                "alias": "/static"
            }
        }
    }

## Serving the static directory with SSL support, redirecting HTTP to HTTPS

    {
        "version": "dev",
        "virtualhost": "domain.tld",
        "certificate": "/etc/pki/tls/certs/domain.tld.crt",
        "certificate_key": "/etc/pki/tls/private/domain.tld.key",
        "redirects": {
            "/": {
                "to": "https://domain.tld/"
            }
        },
        "directories": {
            "/var/www/my-static-dir": {
                "alias": "/static"
            }
        }
    }
    
## The default Wordpress configuration as seen in Fedora

    {
        "version": "dev",
        "directories": {
            "/usr/share/wordpress": {
                "alias": "/wordpress",
                "allow": "local"
            },
            "/usr/share/wordpress/wp-content/plugins/akismet": {
                "match": {
                    "\\.(php|txt)$": {
                        "allow": "none"
                    }
                }
            }
        }
    }

## Proxying the webapp.domain.tld to another HTTP server

We do not specify the proxy_alias, proxy_backend_alias or proxy_protocol here, because we can use their default values.

    {
        "virtualhost": "webapp.domain.tld",
        "proxy_hostname": "localhost",
        "proxy_port": "9000",
    }

If we would like to specify all the options although it duplicates the default values, the example would look like this:

    {
        "virtualhost": "webapp.domain.tld",
        "proxy_protocol": "http://",
        "proxy_hostname": "localhost",
        "proxy_port": "9000",
        "proxy_alias": "/",
        "proxy_backend_alias: "/"
    }

## Proxying the PHP files in http://domain.tld/blog to php-fpm server

This configuration defines index.php directory index for /usr/share/wordpress directory. Sets the /blog alias for that directory and configures the webserver to proxy all the PHP files from the /blog location (and its sub-locations) to PHP-FPM server running on fcgi://localhost:9000.

    {
        "virtualhost": "domain.tld",
        "directories": {
            "/usr/share/wordpress": {
                "alias": "/blog",
                "index": "index.php"
            }
        },
        "locations": {
            "/blog": {
                "match": {
                    "\\.php$": {
                        "proxy_protocol": "fcgi://",
                        "proxy_hostname": "localhost",
                        "proxy_port": "9000",
                        "proxy_backend_alias": "/usr/share/wordpress/$1",
                        "allow": "all"
                    }
                }
            }
        }
    }


