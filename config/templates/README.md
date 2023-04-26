# Templates

## Adding your own template

You can create your own Jinja templates. The only thing you need to know is that
when rendering occurs the Jinja context contains two variables:

- `challenge_config`: an instance of `ChallengeConfig` (defined in
  `mkctf.api.config.challenge`)
- `repository_config`: an instance of `RepositoryConfig` (defined in
  `mkctf.api.config.repository`)

You can access members of both instances within the template.

**Warning: keep in mind that you should not alter these configurations from
           your template!**
