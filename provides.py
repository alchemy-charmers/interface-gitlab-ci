from charms.reactive import Endpoint
from charmhelpers.core import hookenv


class GitlabCIProvides(Endpoint):
    """Provides side of relationship"""

    def publish(self, uri, token):
        """Publish server information for runners to register"""
        for relation in self.relations:
            hookenv.log(
                "Publishing  CI credentials on {}:{}".format(
                    relation.application_name, relation.endpoint_name
                ),
                "DEBUG",
            )
            relation.to_publish["server_uri"] = uri
            relation.to_publish["server_token"] = token
