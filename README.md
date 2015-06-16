# What is webconfig-spec?
Webconfig-spec is specification of webserver configuration for web applications configuration. The goal of webconfig-spec is to provide a way how to configure widely used webservers like Apache httpd, Nginx or HAProxy using the single configuration file.

# What is it useful for?

It can be used to deploy web application without dependency on any particular webserver implementation. In this case, the web application developer writes single configuration file in JSON, which is translated to the particular webserver's configuration on the user's machine when he deploys the application. This is achieved by the webconfig-spec implementation shipped together with the webserver.

# Table of Contents

  * [Description of webconfig-spec - development version](dev/README.md)
  * Current implementations:
    * [httpd-cfg](httpd-cfg.md) - Implementation generating Apache httpd configuration files.
    * [haproxy-cfg](haproxy-cfg.md) - Implementation generating HAProxy configuration files.
  * The example usages of webconfig-spec:
    * [Configuring the web applications in UNIX distribution-like environment](example-distro.md)
    * [Configuring the web applications in Kubernetes/Openshift environment](example-kubernetes-openshift.md)
    * [Configuring the web applications in Docker environment](example-docker.md)
    * [Configuring the web applications distributed as Nulecules (atomicapp)](example-nulecule.md)
