Table of Contents
=================

*This is development version of the webconf-spec and can change without any previous notice.*

  * [Development version](#development-version)
    * [Versioning](#versioning)
  * [What is webconf-spec?](#what-is-webconf-spec)
  * [What is it useful for?](#what-is-it-useful-for)
  * [Are there any implementation already?](#are-there-any-implementation-already)
  * [Format](#format)
  * [Description of webconf-spec specification](#description-of-webconf-spec-specification)
    * [General options](#general-options)
    * [Redirects option](#redirects-option)
    * [Proxy options](#proxy-options)
    * [Match option](#match-option)
    * [Locations option](#locations-option)
    * [Error pages option](#error-pages-option)
    * [Raw config option](#raw-config-option)
    * [Load balancing options](#load-balancing-options)
    * [Merging the webconf-spec formatted files](#merging-the-webconf-spec-formatted-files)
  * [Examples of webconf-spec specification](#examples-of-webconf-spec-specification)
    * [Serving the static directory on http://domain.tld/static](#serving-the-static-directory-on-httpdomaintldstatic)
    * [Serving the static directory with SSL support](#serving-the-static-directory-with-ssl-support)
    * [Serving the static directory with SSL support, redirecting HTTP to HTTPS](#serving-the-static-directory-with-ssl-support-redirecting-http-to-https)
    * [The default Wordpress configuration as seen in Fedora](#the-default-wordpress-configuration-as-seen-in-fedora)
    * [Proxying the webapp.domain.tld to another HTTP server](#proxying-the-webappdomaintld-to-another-http-server)
    * [Proxying the PHP files in http://domain.tld/blog to php-fpm server](#proxying-the-php-files-in-httpdomaintldblog-to-php-fpm-server)

# Development version

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](http://www.ietf.org/rfc/rfc2119.txt).

The Webconf-spec specification is licensed under [GNU Free Documentation License Version 1.3, 3 November 2008](https://www.gnu.org/copyleft/fdl.html).

## Versioning

Within this specification we follow [the semantic versioning pattern](http://semver.org/spec/v2.0.0.html).

# What is webconf-spec?
Webconfig-spec is specification of webserver configuration for web applications configuration. The goal of webconf-spec is to provide a way how to configure widely used webservers or proxies like Apache httpd, Nginx or HAProxy using the single configuration file.

# What is it useful for?

It can be used to create web applications without dependency on any particular webserver implementation. In this case, the web application developer writes single configuration file in JSON, which is translated to the particular webserver's configuration on the user's machine when he deploys the application. This is achieved by the webconf-spec implementation shipped together with the webserver.

# Are there any implementation already?

Yes, we have following implementations generating the native webserver's configuration from the webconf-spec files:

- [httpd-cfg](https://github.com/micro-webapps/httpd-cfg) - Reads the .json webconf-spec files from input directory and generates the Apache httpd configuration in the output directory.
- [haproxy-cfg](https://github.com/micro-webapps/haproxy-cfg) - Reads the .json webconf-spec files from input directory and generates the HAProxy configuration in the output directory.
- [nginx-cfg](https://github.com/micro-webapps/nginx-cfg) - Reads the .json webconf-spec files from input directory and generates the nginx configuration in the output directory.

# Format

The files describing a webserver configuration in accordance with the Webconf-spec specification are represented using [JSON](http://json.org/).

All field names in the specification are **case sensitive**.

# Description of webconf-spec specification

It is important to note that the webconf-spec is not trying to be full featured webserver configuration specification. Usually, the web applications do not use all features of the webservers and therefore we have tried to keep things simple and support only features which are widely used by web applications to configure the webserver and which are shared between all widely used webservers.

## General options

This section describes the general webconf-spec JSON fields. They are used only in the root JSON object, except of the `index` option, which can be used in the in other JSON objects as described later in this specification. 

| Key | Type | Meaning |
|-----|------|---------|
| certificate | String | The full path to file containing the certificate to be used for the virtualhost or server. When using this option, the SSL for this virtualhost or server MUST be enabled by the implementation. |
| certificate_key | String | The full path to file containing the certificate key to be used for the virtualhost or server. When using this option, the SSL for this virtualhost or server MUST be enabled by the implementation. |
| document_root | String | The full path to directory acting as root directory for the virtualhost or server. |
| index | String | Name (or white-space seperated list of names) of the files which SHOULD be served by default when found in directory ("index.html" for example). It can be also set to value `disabled` to disable to the index file completely. The value of `autoindex` will enable automatic generation of indexes similar to the Unix ls command or the Win32 dir shell command. |
| version | String | The version of the webconf-spec used in this configuration file. For the development version of webconf-spec, the value of this option should be set to "dev". This field MUST be always included. |
| virtualhost | String | Virtual host on which the web application should run. |


If the virtualhost option is set to an empty string or is not defined, the webconf-spec implementation SHOULD treat all the options as global (It means not bound to any virtualhost). If any of the other options is set to an empty string or is not defined, the webconf-spec implementation MUST ignore the option completely.

## Redirects option

This section describes redirects option used to redirect from one URL or path to another URL. The Redirects option can be used only in the root object of the webconf-spec.

The format of redirects option is following:

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

The special options which can be used in redirects option are:

| Key | Type | Meaning |
|-----|------|---------|
| to | String | The URL to which the client is redirected. |

The implementation MUST configure the webserver to redirect from the `from` URL to `to` URL.

## Proxy options

This section describes the proxy related webconf-spec JSON fields. They can be used in the root section of webconf-spec or in `locations` or `match` sections as described later in this document.

    "proxy": {
        "url": "http://localhost:8080/"
        "alias": "/",
    }

The special options which can be used in the Proxy option are:
    
| Key | Type | Meaning |
|-----|------|---------|
| url| String | URL on which the backend servers listens to requests. The path part of the URL can contain special `$1` string. When used in the `match` option, the implementation MUST configure the webserver to replace `$1` with the name of file matching the `match` options. When the `match` option is used in the `locations` option, the file name used as replacement for `$1` MUST also include the path to the file starting at the location configured in this particular `locations` option. See the [Proxying the PHP files in http://domain.tld/blog to php-fpm server](#proxying-the-php-files-in-httpdomaintldblog-to-php-fpm-server) for an example of this configuration. When the scheme used in the URL is `balancer://`, then the hostname defines the name of load balancer used for the load balancing. See the [Load balancing options](#load-balancing-options) for more information. |
| alias | String | The alias location of the web application on the frontend server. If the web application should be accessible on "http://domain.tld/blog", then the value of this option should be "/blog". If the `alias` option is set to an emptry string or is not defined, the webconf-spec implementation MUST use "/" string as default value. |
| uds | String | The full path to UNIX Domain Socket which should be used to connect the backend. When both `url` and `uds` options are specified, the `uds` MUST be used prioritely. |

## Match option

This section describes the match option. This option is used to match files served by the webserver based on their names and configure the way webserver handles them. All the Proxy options can be used in the Match option.

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
| allow | String | Word defining the access permision to the files matching the Match option. The "all" value allows all web clients to access the files. The "local" value allows only users from localhost to access the files. The "none" value, as well as any other undefined value, denies anyone to access the file. The default value for all `locations` is "all".|


This allows for example proxying the PHP files to php-fpm server:

    "match": {
        "\\.php$": {
            "proxy" {
                "url": "fcgi://localhost:9000/wordpress/$1"
            },
            "allow": "all"
        }
    }


## Locations option

This section describes the locations options. Locations are used to configure the mapping of path part of URL to real directories on the webserver. Per-location configuration set by this option MUST be applied to all sub-locations of the main location. The `proxy` and `match` options can be used in the `locations` option as well as the `index` option.

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

The special options which can be used in `locations` option are:

| Key | Type | Meaning |
|-----|------|---------|
| Alias | String | Sets the real directory as an alias for the location. If the content of "/var/www/html" directory should be accessible as "http://domain.tld/blog", then the value of this option should be "/var/www/html".|

If the `match` option appears in the `locations` option, all the files matching the regular expression in the main location or its sub-locations MUST be configured by this `match` option.

Using the `locations` option, it is for example possible to disable access to particular files in particular directory:

    {
        "locations": {
            "/blog/wp-content/plugins/akismet": {
                "match": {
                    "regex": "\\.(php|txt)$",
                    "allow": "none"
                }
            },
            "/blog": {
                "alias": "/usr/share/wordpress"
            }
        }
    }

Or it is for example possible to serve static local directory as "http://domain.tld/static":

    {
        "virtualhost": "domain.tld",
        "locations": {
            "/static": {
                "alias": "/var/www/my-static-dir"
            }
        }
    }

## Error pages option

This option is used to define error page showed to the HTTP client on particular HTTP error.

The format of `error_pages` option is following:

    "error_pages": {
        "404": "/error/404.html",
        "403": "/error/403.html"
    }

## Raw config option

This option is used to define the raw config for the particular webserver. This can be used to specify special directives per webserver implementation.

The format of the `raw_config` option is following:

    "raw_config": {
        "httpd >= 2.4.0": [
            "<IfModule mod_fcgid.c>",
            "   <IfModule mod_setenvif.c>",
            "       <IfModule mod_headers.c>",
            "           SetEnvIfNoCase ^Authorization$ \"(.+)\" XAUTHORIZATION=$1",
            "           RequestHeader set XAuthorization %{XAUTHORIZATION}e env=XAUTHORIZATION",
            "       </IfModule>",
            "   </IfModule>",
            "</IfModule>"
        ],
        "nginx >= 1.6.0": [
            "location ~* ^.+\.(jpg|jpeg|gif|bmp|ico|png|css|js|swf)$ {",
            "   expires 30d;",
            "   # Optional: Don't log access to assets",
            "   access_log off;",
            "}"
        ]
    }

The name of the webserver used in the `raw_config` option depends on the webconf-spec implementation. Allowed comparison operators are ">", "<", ">=", "<=", "==" and "!=" as known from C language. The version is in [Semantic Versioning 2.0.0](http://semver.org/spec/v2.0.0.html) format.

The `raw config` option can be used in the `match` option, `locations` option and in the root object of the webconf-spec configuration.

The `raw config` option SHOULD be used only when there is no other way how to describe particular configuration using other webconf-spec options.

## Load balancing options

These options are used to define the load balancing. It defines the balancing method, session persistence method and list of backend servers user by the balancer.

The format of the `balancers` option is following:

    "balancers" {
        "balancer-name": {
            "method": "round-robin",
            "persistence": {
                "method": "use_cookie_or_url",
                "cookie_name": "JSESSIONID",
                "url_id": "jsessionid"
            }.
            "members": [
                {
                    "url": "http://member1:8080/
                    "weight": 50,
                }
            ]
        },
        "another-balancer": {
           ...
        }
    }

The name of the balancer is used in the [Proxy options](#proxy-options) to define the proxying of requests to the load balancer.

The special options which can be used in `balancers` option are:

| Key | Type | Meaning |
|-----|------|---------|
| method | String | Defines the load balancing method. When set to `round-robin`, the requests to the application servers SHOULD be distributed in a round-robin fashion. When set to `least-connected` — next request SHOULD be assigned to the server with the least number of active connections. When not defined, the `round-robin` is used as a default method. |
| persistence | String | Defines the way how the session persistence is achieved, so all requests from the single session are handled by the same backend server. When not defined, the session persistence is not kept. |
| persistence.method | String | Defines the method used to achieve the session persistence. When set to `generate_cookie`, the webserver SHOULD generate the cookie to route requests to proper backends. When set to `use_cookie_or_url`, the webserver SHOULD use the cookie or URL id generated by the backend. When set to `none`, no session persistence is kept. In all cases, the first request is forwarded to one of the backends according to load balancing method. |
| persistence.cookie_name | String | Defines the name of the cookie used to achive the session persistence. |
| persistence.url_id | String | Defines the name of the URL-based parameter used to achieve the session persistence. |
| members | String | Defines the list of members for this balancer. |
| members.url| String | URL on which the backend servers listens to requests. The path part of the URL is ignored. |
| members.weight | Integer | Number between 1 and 100 which defines the normalized weighted load applied to the backend. The requests are divided between balancer members in the ratio defined by their weights. When no weight is defined, the webconf-spec implementation MUST use 1 as default. When there are for example 3 balancer members with weights 3, 1 and 1, then every 5 new requests MUST be distributed across the backends as the following: 3 requests will be directed to member1, one request will go to member2, and another one to member3. |


## Merging the webconf-spec formatted files

Although the webconf-spec describes the configuration of the single web application, all the implementations SHOULD expect the set of webconf-spec formatted files as the input. This allows to configure multiple web applications running on the single virtualhost served in different locations. In case of two config files with the same options which are in contrast to each other, the implementation MUST treat it as an error.

The example of merging two configuration files using the locations section. The first configuration:

    {
        "version": "dev",
        "virtualhost": "domain.tld",
        "certificate": "/etc/pki/tls/certs/domain.tld.crt",
        "certificate_key": "/etc/pki/tls/private/domain.tld.key",
        "locations": {
            "/static": {
                "alias": "/var/www/my-static-dir"
            }
        }
    }

The second configuration:

    {
        "version": "dev",
        "virtualhost": "domain.tld",
        "locations": {
            "/static2": {
                "alias": "/var/www/my-static-dir"
            }
        }
    }

Resulting configuration:

    {
        "version": "dev",
        "virtualhost": "domain.tld",
        "certificate": "/etc/pki/tls/certs/domain.tld.crt",
        "certificate_key": "/etc/pki/tls/private/domain.tld.key",
        "locations": {
            "/static": {
                "alias": "/var/www/my-static-dir"
            },
            "/static2": {
                "alias": "/var/www/my-static-dir"
            }
        }
    }

In case when the "certificate" option would be used in both input configuration files with different valud, the implentation would have to return an error. The same would for example happen when both input files define the same location.

# Examples of webconf-spec specification

This sections contains few commented examples of the webconf-spec configuration files.

## Serving the static directory on http://domain.tld/static

    {
        "version": "dev",
        "virtualhost": "domain.tld",
        "locations": {
            "/static": {
                "alias": "/var/www/my-static-dir"
            }
        }
    }

## Serving the static directory with SSL support

    {
        "version": "dev",
        "virtualhost": "domain.tld",
        "certificate": "/etc/pki/tls/certs/domain.tld.crt",
        "certificate_key": "/etc/pki/tls/private/domain.tld.key",
        "locations": {
            "/static": {
                "alias": "/var/www/my-static-dir"
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
        "locations": {
            "/static": {
                "alias": "/var/www/my-static-dir"
            }
        }
    }
    
## The default Wordpress configuration as seen in Fedora

    {
        "version": "dev",
        "locations": {
            "/wordpress": {
                "alias": "/usr/share/wordpress",
                "allow": "local"
            },
            "/wordpress/wp-content/plugins/akismet": {
                "match": {
                    "\\.(php|txt)$": {
                        "allow": "none"
                    }
                }
            }
        }
    }

## Proxying the webapp.domain.tld to another HTTP server

    {
        "virtualhost": "webapp.domain.tld",
        "proxy": {
            "url": "http://localhost:8080/"
        }
    }

## Proxying the PHP files in http://domain.tld/blog to php-fpm server

This configuration sets the "/blog" location to be served from the "/usr/share/wordpress" directory. Then it defines the index.php directory index to be used in this director and its subdirectories.

The Match option is used in the locations section, so all the requests matching the ".php" files in the "/blog" location will be forwarded to the PHP-FPM server running on fcgi://localhost:9000/. The path part of the `url` describes that the root directory for the web-application in the backend server is "/usr/share/wordpress". The request for "http://domain.tld/blog/posts/new_post.php" will be therefore forwareded to backend server which will try to serve the "/usr/shared/wordpress/blog/posts/new_post.php" file.

    {
        "virtualhost": "domain.tld",
        "locations": {
            "/blog": {
                "alias": "/usr/share/wordpress",
                "index": "index.php",
                "match": {
                    "\\.php$": {
                        "proxy": {
                            "url": "fcgi://localhost:9000/usr/share/wordpress/$1"
                        },
                        "allow": "all"
                    }
                }
            }
        }
    }


