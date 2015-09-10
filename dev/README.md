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

This section describes the proxy related webconf-spec JSON fields. They can be used in the root section of webconf-spec or in "directories" or "locations" section as described later in this document.

    "proxy": {
        "protocol": "http://",
        "hostname": "localhost",
        "port": "8080",
        "alias": "/",
        "backend_alias: "/"
    }

The special options which can be used in the Proxy option are:
    
| Key | Type | Meaning |
|-----|------|---------|
| protocol | String | The protocol used to connect the backend server. For example "http://", "fcgi://" or "ajp://". |
| alias | String | The alias location of the web application on the frontend server. If the web application should be accessible on "http://domain.tld/blog", then the value of this option should be "/blog". |
| backend_alias | String | The alias location of the web application on the backend server. If the web application backend is accessible on "http://internal.domain.tld/wordpress", then the value of this option should be "/wordpress". When used in Match option, the implementation MUST configure the webserver to allow replacement of `$1` in the backend_alias value with the name of file matching the Match options. When the Match option is used in the Locations option (or Directories option), the file name used as replacement for `$1` MUST also include the path to the file starting at the location (or directory) configured in this particular Locations option (or Directories option). See the [Proxying the PHP files in http://domain.tld/blog to php-fpm server](#proxying-the-php-files-in-httpdomaintldblog-to-php-fpm-server) as an example of this configuration. |
| hostname | String | The hostname or IP address of the backend server running the web application. If the web application backend is accessible on "http://internal.domain.tld/wordpress", then the value of this option should be "internal.domain.tld". |
| port | Integer | The port of the backend server running the web application. |
| uds | String | The full path to UNIX Domain Socket which should be used to connect the backend. When both hostname/port and uds options are specified, the uds MUST be used prioritely. |

If the protocol option is set to an empty string or is not defined, but all the other options needed to proxy the requests are specified, the webconf-spec implementation MUST use "http://" as default. If the alias or the backend_alias options are set to an emptry string or are not defined, the webconf-spec implementation MUST use "/" string as default value.

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
| allow | String | Word defining the access permision to the files matching the Match option. The "all" value allows all web clients to access the files. The "local" value allows only users from localhost to access the files. The "none" value, as well as any other undefined value, denies anyone to access the file. The default value for all locations or directories is "all".|


This allows for example proxying the PHP files to php-fpm server:

    "match": {
        "\\.php$": {
            "proxy" {
                "protocol": "fcgi://",
                "backend_alias": "/wordpress/$1",
                "hostname": "localhost",
                "port:", "9000"
            },
            "allow": "all"
        }
    }

## Directories option

This section describes the directories related webconf-spec JSON options. Directories are used to configure the real directories on the webserver. Per-directory configuration set by this option MUST be applied to all sub-directories of the main directory. All the Proxy options and Match option can be used in the Directories options as well as the "index" option.

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


If Match option appears in the Directories option, all files matching the regular expression in the main directory or its sub-directories MUST be configured by this Match option.

Using Directories option, it is for example possible to disable access to particular files in particular directory:

    {
        "directories": {
            "/usr/share/wordpress/wp-content/plugins/akismet": {
                "match": {
                    "regex": "\\.(php|txt)$",
                    "allow": "none"
                }
            },
            "/usr/share/wordpress/": {
                "alias": "/blog"
            }
        }
    }

Or it is for example possible to serve static local directory as "http://domain.tld/static":

    {
        "virtualhost": "domain.tld",
        "directories": {
            "/var/www/my-static-dir": {
                "alias": "/static"
            }
        }
    }

## Locations option

This section describes the locations options. Locations are used to configure the non-real paths on the webserver as they are used in the HTTP requests. Per-location configuration set by this option MUST be applied to all sub-locations of the main location. All the Proxy options and Match option can be used in the Locations options as well as the "index" option.

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

The special options which can be used in Directories option are:

| Key | Type | Meaning |
|-----|------|---------|
| Alias | String | Sets the real directory as an alias for the location. If the content of "/var/www/html" directory should be accessible as "http://domain.tld/blog", then the value of this option should be "/var/www/html".|

If Match option appears in the Locations option, all the files matching the regular expression in the main location or its sub-locations MUST be configured by this Match option.

Using Locations option, it is for example possible to disable access to particular files in particular directory:

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

## Directories versus Locations

The Directories can be converted to locations using the "alias" option and vice-versa. When writing configuration file in webconf-spec format, the directories and locations MUST remain convertable to each other.

It is therefore wrong to write following webconf-spec file:

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

The reason why this is wrong is that the implementation has no idea on which URL the directory "/usr/share/wordpress/wp-content/plugins/akismet" is being served. To fix this, we simply have to set an alias to any prefix of the "/usr/share/wordpress/wp-content/plugins/akismet" directory:

    {
        "directories": {
            "/usr/share/wordpress/wp-content/plugins/akismet": {
                "match": {
                    "regex": "\\.(php|txt)$",
                    "allow": "none"
                }
            },
            "/usr/share/wordpress/": {
                "alias": "/blog"
            }
        }
    }

This is now correct, because the implementation can compute the correct URL for the "/usr/share/wordpress/wp-content/plugins/akismet" directory - it would be "/blog/wp-content/plugins/akismet".

This allows simpler writing of webconf-spec configuration, because the author of the configuration can decide if he wants to describe the configuration based on the locations or directories.

## Error pages option

This option is used to define error page showed to the HTTP client on particular HTTP error.

The format of error_pages option is following:

    "error_pages": {
        "404": "/error/404.html",
        "403": "/error/403.html"
    }

## Raw config option

This option is used to define the raw config for the particular webserver. This can be used to specify special directives per webserver implementation.

The format of the raw_config option is following:

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

The name of the webserver used in the raw_config option depends on the webconf-spec implementation. Allowed comparison operators are ">", "<", ">=", "<=", "==" and "!=" as known from C language. The version is in [Semantic Versioning 2.0.0](http://semver.org/spec/v2.0.0.html) format.

The raw config option can be used in the Match option, Directories option, Locations option and in the root object of the webconf-spec configuration.

The raw config option SHOULD be used only when there is no other way how to describe particular configuration using other webconf-spec options.

## Load balancing options

These options are used to define the load balancing. It defines the balancing method, session persistence method and list of backend servers user by the balancer.

The format of the balancers option is following:

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
                    "protocol": "http://",
                    "hostname": "member1",
                    "port": "8080",
                    "weight": 50,
                }
            ]
        },
        "another-balancer": {
           ...
        }
    }

The special options which can be used in balancers option are:

| Key | Type | Meaning |
|-----|------|---------|
| method | String | Defines the load balancing method. When set to `round-robin`, the requests to the application servers SHOULD be distributed in a round-robin fashion. When set to `least-connected` — next request SHOULD be assigned to the server with the least number of active connections. When not defined, the `round-robin` is used as a default method. |
| persistence | String | Defines the way how the session persistence is achieved, so all requests from the single session are handled by the same backend server. When not defined, the session persistence is not kept. |
| persistence.method | String | Defines the method used to achieve the session persistence. When set to `generate_cookie`, the webserver SHOULD generate the cookie to route requests to proper backends. When set to `use_cookie_or_url`, the webserver SHOULD use the cookie or URL id generated by the backend. When set to `none`, no session persistence is kept. In all cases, the first request is forwarded to one of the backends according to load balancing method. |
| members | String | Defines the list of members for this balancer. |
| members.protocol | String | Defines the protocol used by the backend the same way as in the Proxy option. |
| members.hostname | String | Defines the hostname or IP address of the backend the same way as in the Proxy option. |
| members.port | String | Defines the port on which the backend is listening the same was as in the Proxy option. |
| members.weight | Integer | Number between 1 and 100 which defines the normalized weighted load applied to the backend.|


## Merging the webconf-spec formatted files

Although the webconf-spec describes the configuration of the single web application, all the implementations SHOULD expect the set of webconf-spec formatted files as the input. This allows to configure multiple web applications running on the single virtualhost served in different locations. In case of two config files with the same options which are in contrast to each other, the implementation MUST treat it as an error.

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

We do not specify the alias, backend_alias or protocol here, because we can use their default values.

    {
        "virtualhost": "webapp.domain.tld",
        "proxy": {
            "hostname": "localhost",
            "port": "8080"
        }
    }

If we would like to specify all the options although it duplicates the default values, the example would look like this:

    {
        "virtualhost": "webapp.domain.tld",
        "proxy": {
            "protocol": "http://",
            "hostname": "localhost",
            "port": "8080",
            "alias": "/",
            "backend_alias: "/"
        }
    }

## Proxying the PHP files in http://domain.tld/blog to php-fpm server

This configuration sets the "/blog" location to be served from the "/usr/share/wordpress" directory. Then it defines the index.php directory index to be used in this director and its subdirectories.

The Match option is used in the locations section, so all the requests matching the ".php" files in the "/blog" location will be forwarded to the PHP-FPM server running on fcgi://localhost:9000. The value of "backend_alias" describes that the root directory for the web-application in the backend server is "/usr/share/wordpress". The request for "http://domain.tld/blog/posts/new_post.php" will be therefore forwareded to backend server which will try to serve the "/usr/shared/wordpress/blog/posts/new_post.php" file.

    {
        "virtualhost": "domain.tld",
        "locations": {
            "/blog": {
                "alias": "/usr/share/wordpress",
                "index": "index.php",
                "match": {
                    "\\.php$": {
                        "proxy": {
                            "protocol": "fcgi://",
                            "hostname": "localhost",
                            "port": "9000",
                            "backend_alias": "/usr/share/wordpress/$1",
                        },
                        "allow": "all"
                    }
                }
            }
        }
    }


