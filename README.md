# What is webconf-spec?
Webconfig-spec is specification of webserver configuration for web applications configuration. The goal of webconf-spec is to provide a way how to configure widely used webservers or proxies like Apache httpd, Nginx or HAProxy using the single configuration file.

# What is it useful for?

It can be used to create web applications without dependency on any particular webserver implementation. In this case, the web application developer writes single configuration file in JSON, which is translated to the particular webserver's configuration on the user's machine when he deploys the application. This is achieved by the webconf-spec implementation shipped together with the webserver.

# Table of Contents

  * [Description of webconf-spec - development version](dev/README.md)
  * [JSON Schema of webconf-spec in Docson](http://micro-webapps.github.io/webconf-spec/#https://raw.githubusercontent.com/micro-webapps/webconf-spec/master/dev/schema.json)
  * Current implementations:
    * [httpd-cfg](https://github.com/micro-webapps/httpd-cfg) - Implementation generating Apache httpd configuration files.
    * [haproxy-cfg](https://github.com/micro-webapps/haproxy-cfg) - Implementation generating HAProxy configuration files.
    * [nginx-cfg](https://github.com/micro-webapps/nginx-cfg) - Implementation generating nginx configuration files.
  * The example usages of webconf-spec:
    * [Configuring the web applications in UNIX distribution-like environment](example-distro.md)
    * [Configuring the web applications in Kubernetes/Openshift environment](example-kubernetes-openshift.md)
    * [Configuring the web applications in Docker environment](example-docker.md)
    * [Configuring the web applications distributed as Nulecules (atomicapp)](example-nulecule.md)
