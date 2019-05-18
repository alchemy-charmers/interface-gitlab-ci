from charms.reactive import RelationBase, scopes, hook
from charmhelpers.core import hookenv

import json


class GitLabCIRegistrationError(Exception):
    ''' Exception raiseed if registration fails '''


class GitLabCIRequires(RelationBase):
    scope = scopes.UNIT
    # auto_accessors=['hostname','ports']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hookenv.atexit(lambda: self.remove_state('{relation_name}.triggered'))
        hookenv.atexit(lambda: self.remove_state('{relation_name}.departed'))

    @hook('{requires:gitlab-ci}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.triggered')
        hookenv.log('gitlab-ci.triggered', 'DEBUG')
        if self.hostname and self.token:
            hookenv.log('gitlab-ci.ready', 'INFO')
        self.set_state('{relation_name}.ready')
        hookenv.log('gitlab-runner.ready', 'DEBUG')
        if self.cfg_status is None:
            hookenv.log('GitLab CI not yet finished configuration', 'INFO')
        elif self.cfg_status.startswith('passed'):
            hookenv.log(self.cfg_status, 'INFO')
        elif self.cfg_status.startswith('failed'):
            hookenv.log(self.cfg_status, 'ERROR')
            raise GitLabCIRegistrationError(self.cfg_status)

    @hook('{requires:reverseproxy}-relation-{departed}')
    def departed(self):
        self.set_state('{relation_name}.triggered')
        self.set_state('{relation_name}.departed')
        self.remove_state('{relation_name}.configured')
        self.remove_state('{relation_name}.ready')
        hookenv.log('reverseproxy.departed', 'INFO')

    def configure(self, config):
        # Error if missing required configs
        if not config['tags']:
            raise GitLabCIRegistrationError('Setting tags configuation is required')
        if not config['description']:
            raise GitLabCIRegistrationError('Setting a description for the runner is required')

        self.set_remote('config', json.dumps(config))
        self.set_state('{relation_name}.configured')

    @property
    def cfg_status(self):
        return self.get_remote(hookenv.local_unit() + '.cfg_status')

    @property
    def hostname(self):
        return self.get_remote('hostname')

    @property
    def token(self):
        return self.get_remote('token')
