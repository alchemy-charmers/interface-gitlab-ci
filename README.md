This interface is intended to allow the exchange of registration information between GitLab CI and a GitLab CI Runner unit.

All relation states should check for 'triggered' state to be sure it is a relation based event.

Expected flow:
 - Requires:
   - when 'ready' and when_not 'configured' call the configure function to provide a registration token and hostname
 - Provides:
   - when 'changed' apply self.config to the configuration. *This is a list of configurations to apply*
   - return a feedback about the config via the set_cfg_status function
 - Requires:
   - if cfg_status is a failure interface will log any provided status and fail
   - if cfg_status is a success a success will be logegd via 'INFO' and no other state is applied

Departed:
 - Provides:
  - when 'departed' remove self.config from the configuration

Proxy Configuration Keys:
 - description: Description of the runner
 - tags: Tags to configure on this runner
