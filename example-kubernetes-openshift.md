# Configuring the web applications in Kubernetes/Openshift environment

This document describes the benefits of using webconf-spec in the Kubernetes/Openshift environment.

*This document is not final yet and can change without any notice. For now, it is mainly intended to be a working place where the ideas are put.*

## How is webconf-spec useful in Kubernetes/Openshift environment?

The developer of the web application writting the Kubernetes/Openshift service can bundle the generic, server independent, configuration for the web application and he does not have to care what frontend webserver or reverse proxy is used in the cloud.

The deployer of the web application does not have to waste time understanding the configuration of reverse proxy used in the cloud. He can just start the web application as shipped by the developer and change only the needed parameters like virtualhost, URI or certificates used by the web application. The reverse-proxy or webserver frontend in the cloud can then pick-up the configuration automatically.

When the deployer of the web application switches between Kubernetes or Openshift, he does not have to change the webserver related configuration.

## Example of webconf-spec for Kubernetes/Openshift

The web applications configuration files are part of the Kubernetes service file shipped with the application itself in the `metadata` section:

    {
        "kind": "Service",
        "apiVersion": "v1beta3",
        "metadata": {
            "name": "webapp-owncloud",
            "annotations": {
                "webconfig": "{\"version\":\"dev\", \"virtualhost\": \"domain.tld\",\"proxy\": { \"url\": \"http://webapp-address/owncloud",\"alias\": \"/owncloud\"}}"
            }
        },
        "spec": {
            "selector": {
                "name": "webapp-owncloud"
            },
            "ports": [
                {
                    "name": "http-port",
                    "protocol": "TCP",
                    "port": 80,
                    "targetPort": 80
                }
            ]
        }
    }

The webserver or the reverse proxy used by the Kubernetes/Openshift can then use the Kubernetes/Openshift API-server to detect the service with `webconfig` field in `metadata` section and serve it automatically without any further configuration by the deployer.

Note that using the Nulecule and Atomicapp, it is even possible to parametrize the webconf-spec, so the deployer does not have to touch the `webconfig` webconf-spec JSON, but can just set the virtualhost or alias using the atomicapp user interface.

The way described here is already implemented as the micro-webapps project.
