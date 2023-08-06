import base64
import logging
import requests
import json

from apigateway.clients import constants
from apigateway.models.route import Route
from apigateway.models.upstream import Upstream
from apigateway.models.consumer import Consumer
from apigateway.models.plugin_config import PluginConfig

from apigateway.exceptions.exceptions import APIGatewayWarningException

logger = logging.getLogger(__name__)


class ApiGatewayClient(object):

    def create_upstream(self, upstream):
        body = {
            "retries": upstream.retries,
            "retry_timeout": upstream.retry_timeout,
            "timeout": {
                "connect": upstream.connect_timeout,
                "send": upstream.send_timeout,
                "read": upstream.read_timeout
            },
            "nodes": upstream.host_list,
            "type": upstream.type,
            "name": upstream.name,
            "desc": upstream.description,
            "scheme": upstream.scheme
        }
        json_body = json.dumps(body, indent=4)
        headers = {'x-api-key': constants.API_KEY}
        try:
            upstream_created = requests.post(constants.UPSTREAM_URL, json_body, headers=headers)
            logger.info(f"Create upstream {upstream.name}")
            return upstream_created
        except ApiException as e:
            msg = (f"Error creating upstream {upstream.name}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def list_upstreams(self):
        upstream_list = []
        try:
            headers = {'x-api-key': constants.API_KEY}
            upstreams = (requests.get(constants.UPSTREAM_URL, headers=headers)).json()
        except ApiException as e:
            raise APIGatewayWarningException(e)
        except ApiTypeError as e:
            raise APIGatewayWarningException(e)

        if 'list' not in upstreams:
            return []
        for upstream in upstreams["list"]:
            print(upstream)
            upstream_object = Upstream(
                name=upstream['value']['name'],
                description=upstream['value']['desc'],
                scheme=upstream['value']['scheme'],
                type=upstream['value']['type'],
                retry_timeout=upstream['value']['retry_timeout'],
                retries=upstream['value']['retries'],
                connect_timeout=upstream['value']['timeout']['connect'],
                send_timeout=upstream['value']['timeout']['send'],
                read_timeout=upstream['value']['timeout']['read'],
                host_list=upstream['value']['nodes']
            )
            upstream_list.append(upstream_object)
        return upstream_list

    def get_upstream_detail(self, upstream_id):
        try:
            headers = {'x-api-key': constants.API_KEY}
            upstream = (requests.get(constants.UPSTREAM_URL + "/" + upstream_id, headers=headers)).json()
        except ApiException as e:
            raise APIGatewayWarningException(e)
        if not upstream:
            return None
        return Upstream(
            name=upstream['value']['name'],
            description=upstream['value']['desc'],
            scheme=upstream['value']['scheme'],
            type=upstream['value']['type'],
            retry_timeout=upstream['value']['retry_timeout'],
            retries=upstream['value']['retries'],
            connect_timeout=upstream['value']['timeout']['connect'],
            send_timeout=upstream['value']['timeout']['send'],
            read_timeout=upstream['value']['timeout']['read'],
            host_list=upstream['value']['nodes']
        )

    def update_upstream(self, upstream_id, upstream):
        body = {
            "retries": upstream.retries,
            "retry_timeout": upstream.retry_timeout,
            "timeout": {
                "connect": upstream.connect_timeout,
                "send": upstream.send_timeout,
                "read": upstream.read_timeout
            },
            "nodes": upstream.host_list,
            "type": upstream.type,
            "name": upstream.name,
            "desc": upstream.description,
            "scheme": upstream.scheme
        }
        json_body = json.dumps(body, indent=4)
        try:
            headers = {'x-api-key': constants.API_KEY}
            upstream_updated = requests.patch(constants.UPSTREAM_URL + "/" + upstream_id, json_body, headers=headers)
            logger.info(f"Update upstream with ID {upstream_id}")
            return upstream_updated
        except ApiException as e:
            msg = (f"Error updating upstream {upstream_id}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def delete_upstream(self, upstream_id):
        try:
            headers = {'x-api-key': constants.API_KEY}
            return requests.delete(constants.UPSTREAM_URL + "/" + upstream_id, headers=headers)
        except ApiException as e:
            msg = (f"Error deleting upstream with ID {upstream_id}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def create_consumer(self, consumer):
        headers = {'x-api-key': constants.API_KEY}
        body = {
            "username": consumer.username,
            "plugins": consumer.plugins,
        }
        json_body = json.dumps(body, indent=4)
        try:
            consumer_created = requests.put(constants.CONSUMER_URL, json_body, headers=headers)
            print(consumer_created)
            logger.info(f"Create consumer {consumer.username}")
            return consumer_created
        except ApiException as e:
            msg = (f"Error creating consumer {uconsumer.username}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def list_consumers(self):
        consumer_list = []
        try:
            headers = {'x-api-key': constants.API_KEY}
            consumers = (requests.get(constants.CONSUMER_URL, headers=headers)).json()
        except ApiException as e:
            raise APIGatewayWarningException(e)
        except ApiTypeError as e:
            raise APIGatewayWarningException(e)

        if 'list' not in consumers:
            return []
        for consumer in consumers["list"]:
            consumer_object = Consumer(
                username=consumer["value"]["username"],
                plugins=consumer["value"]["plugins"]
            )
            consumer_list.append(consumer_object)
        return consumer_list

    def get_consumer_detail(self, consumer_username):
        try:
            headers = {'x-api-key': constants.API_KEY}
            consumer = (requests.get(constants.CONSUMER_URL + "/" + consumer_username, headers=headers)).json()
        except ApiException as e:
            raise APIGatewayWarningException(e)
        if not consumer:
            return None
        return Consumer(
            username=consumer["value"]["username"],
            plugins=consumer["value"]["plugins"]
        )

    def delete_consumer(self, consumer_username):
        try:
            headers = {'x-api-key': constants.API_KEY}
            return requests.delete(constants.CONSUMER_URL + "/" + consumer_username, headers=headers)
        except ApiException as e:
            msg = (f"Error deleting consumer with username {consumer_username}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def create_route(route):
        headers = {'x-api-key': constants.API_KEY}
        body = {
            "uris": route.paths,
            "methods": route.methods,
            "hosts": route.hosts,
            "plugins": route.plugins,
            "name": route.name,
            "desc": route.description,
            "upstream_id": route.upstream_id
        }
        json_body = json.dumps(body, indent=4)
        try:
            route_created = requests.post(constants.ROUTE_URL, json_body, headers=headers)
            logger.info(f"Create route {route.name}")
            return route_created
        except ApiException as e:
            msg = (f"Error creating route {route.name}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def list_routes(self):
        routes_list = []
        try:
            headers = {'x-api-key': constants.API_KEY}
            routes = (requests.get(constants.ROUTE_URL, headers=headers)).json()
        except ApiException as e:
            raise APIGatewayWarningException(e)
        except ApiTypeError as e:
            raise APIGatewayWarningException(e)

        if 'list' not in routes:
            return []
        for route in routes["list"]:
            route_object = Route(
                name=route['value']['name'],
                description=route['value']['desc'],
                upstream_id=route['value']['upstream_id'],
                paths=route['value']['uris'],
                methods=route['value']['methods'],
                hosts=route['value']['hosts'],
                plugins=route['value']['plugins']
            )
            routes_list.append(route_object)
        return routes_list

    def get_route_detail(self, route_id):
        try:
            headers = {'x-api-key': constants.API_KEY}
            route = (requests.get(constants.ROUTE_URL + "/" + route_id, headers=headers)).json()
        except ApiException as e:
            raise APIGatewayWarningException(e)
        if not route:
            return None
        return Route(
            name=route['value']['name'],
            description=route['value']['desc'],
            upstream_id=route['value']['upstream_id'],
            paths=route['value']['uris'],
            methods=route['value']['methods'],
            hosts=route['value']['hosts'],
            plugins=route['value']['plugins']
        )

    def update_route(self, route_id, route):
        body = {
            "uris": route.paths,
            "methods": route.methods,
            "hosts": route.hosts,
            "plugins": route.plugins,
            "name": route.name,
            "desc": route.description,
            "upstream_id": route.upstream_id
        }
        json_body = json.dumps(body, indent=4)
        try:
            headers = {'x-api-key': constants.API_KEY}
            route_updated = requests.patch(constants.ROUTE_URL + "/" + route_id, json_body, headers=headers)
            logger.info(f"Update route with ID {route_id}")
            return route_updated
        except ApiException as e:
            msg = (f"Error updating route {route_id}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def delete_route(self, route_id):
        try:
            headers = {'x-api-key': constants.API_KEY}
            return requests.delete(constants.ROUTE_URL + "/" + route_id, headers=headers)
        except ApiException as e:
            msg = (f"Error deleting route with id {route_id}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def create_plugin_config(self, plugin_config, plugin_id):
        headers = {'x-api-key': constants.API_KEY}
        body = {
            "plugins": plugin_config.plugins,
            "desc": plugin_config.description,
            "labels": plugin_config.labels,
        }
        json_body = json.dumps(body, indent=4)
        try:
            plugin_config_created = requests.put(constants.PLUGIN_CONFIG_URL + "/" + plugin_id, json_body,
                                                 headers=headers)
            logger.info(f"Create plugin config with id {plugin_config.id}")
            return plugin_config_created
        except ApiException as e:
            msg = (f"Error creating plugin config with ID {plugin_config.id}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def list_all_plugin_config(self):
        headers = {'x-api-key': constants.API_KEY}
        plugin_config_list = []
        try:
            plugin_configs = (requests.get(constants.PLUGIN_CONFIG_URL, headers=headers)).json()
        except ApiException as e:
            raise APIGatewayWarningException(e)
        except ApiTypeError as e:
            raise APIGatewayWarningException(e)

        if 'list' not in plugin_configs:
            return []
        for plugin_config in plugin_configs["list"]:
            plugin_config_object = PluginConfig(
                id=plugin_config['value']['id'],
                plugins=plugin_config['value']['plugins'],
                description=plugin_config['value']['desc'],
                labels=plugin_config['value']['labels'],
            )
            plugin_config_list.append(plugin_config_object)
        return plugin_config_list

    def get_plugin_config_detail(self, plugin_config_id):
        try:
            headers = {'x-api-key': constants.API_KEY}
            plugin_config = (requests.get(constants.PLUGIN_CONFIG_URL + "/" + plugin_config_id, headers=headers)).json()
        except ApiException as e:
            raise APIGatewayWarningException(e)
        if not plugin_config:
            return None
        return PluginConfig(
            id=plugin_config['value']['id'],
            plugins=plugin_config['value']['plugins'],
            description=plugin_config['value']['desc'],
            labels=plugin_config['value']['labels'],
        )

    def update_plugin_config(self, plugin_config_id, plugin_config):
        headers = {'x-api-key': constants.API_KEY}
        body = {
            "plugins": plugin_config.plugins,
            "desc": plugin_config.description,
            "labels": plugin_config.labels,
        }
        json_body = json.dumps(body, indent=4)
        try:
            plugin_config_updated = requests.patch(constants.PLUGIN_CONFIG_URL + "/" + plugin_config_id, json_body,
                                                   headers=headers)
            logger.info(f"Update plugin config with ID {plugin_config_id}")
            return plugin_config_updated
        except ApiException as e:
            msg = (f"Error updating plugin config {plugin_config_id}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)

    def delete_plugin_config(self, plugin_config_id):
        try:
            headers = {'x-api-key': constants.API_KEY}
            return requests.delete(constants.PLUGIN_CONFIG_URL + "/" + plugin_config_id, headers=headers)
        except ApiException as e:
            msg = (f"Error deleting plugin config with id {plugin_config_id}."
                   f" Detail {e}")
            logger.info(msg)
            raise APIGatewayWarningException(msg)
