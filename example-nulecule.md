# Configuring the web applications distributed as Nulecules (atomicapp)

This document describes the benefits of using webconf-spec for the web applications distributed as Nulecules (atomicapp).

*This document is not final yet and can change without any notice. For now, it is mainly intended to be a working place where the ideas are put.*

## How is webconf-spec useful for the Nulecule?

Using the webconf-spec, the developer of the Nulecule file can create self-contained web application which includes also the server-independent configuration for the webserver or reverse proxy used in the multi-container environment.

The key benefits are similar to one described on the [Configuring the web applications in Kubernetes/Openshift environment](example-kubernetes-openshift.md) page, so please refer to it.

## Example of webconf-spec for Nulecule

The web applications configuration files are part of the Kubernetes service file shipped with the application itself in the `metadata` section. The webconf-spec is parametrized using the Nulecule:

    {
        "kind": "Service",
        "apiVersion": "v1beta3",
        "metadata": {
            "name": "webapp-owncloud",
            "annotations": {
                "webconfig": "{\"version\":\"dev\", \"virtualhost\": \"$vhost\",\"proxy\": { \"url\": \"http://webapp/owncloud\", \"alias\": \"$alias\"}}"
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

The Nulecule file for the webapp described by the Kubernetes service file above could look like this:

    ---
    specversion: 0.0.1-alpha
    id: webapp-owncloud-atomicapp
    metadata:
    name: Owncloud
    appversion: 2015-50-21-001
    description: >
        This is a nulecule that will get you the container with Owncloud which
        is able to run with mwa-httpd-frontend.
    graph:
    webapp-owncloud:
        params:
        vhost:
            description: >
            Virtual-host where Owncloud should be served.
            default: localhost
        alias:
            description: >
            Alias which should be used to serve the Owncloud.
            default: /owncloud
        artifacts:
        kubernetes:
            - file://artifacts/kubernetes/owncloud-pod.yaml
            - file://artifacts/kubernetes/owncloud-service.json
        openshift:
            - inherit:
            - kubernetes

The developer of the web application can now ship the web application and be sure, that the deployer will be able to configure the virtualhost or alias on which the web application will be served and will use the same configuration file as he did when developing the web application.

For the deployer, it is easy to deploy the web application, because he does not even have to open any configuration file, because everything is parametrized.

Once the web application is deployed, the frontend or reverse proxy running in the cloud picks-up the configuration automatically using the Kubernetes/Openshift API-server or gets it from shared Docker volume in case of plain Docker containers and starts serving it as defined in the configuration.