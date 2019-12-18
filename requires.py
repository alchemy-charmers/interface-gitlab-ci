from charms.reactive import Endpoint, when, when_any, set_flag, clear_flag


class GitLabCIRegistrationError(Exception):
    """ Exception raiseed if registration fails """


class GitLabCiRequires(Endpoint):
    @when_any("endpoint.{endpoint_name}.joined", "endpoint.{endpoint_name}.changed")
    def check_ci_server(self):
        server_uri = self.all_joined_units.received.get("server_uri", None)
        server_token = self.all_joined_units.received.get("server_token", None)
        if server_uri and server_token:
            set_flag(self.expand_name("available"))
            return (server_uri, server_token)
        return None

    @when("endpoint.{endpoint_name}.departed")
    def process_relation_departed(self):
        clear_flag(self.expand_name("available"))

    def get_server_credentials(self):
        return self.check_ci_server()
