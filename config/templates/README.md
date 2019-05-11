# Templates

## Adding your own template

You can create your own Jinja templates. The only thing you need to know is that when rendering occurs the
Jinja context contains two variables:

- `repo_conf`: an instance of `RepositoryConfiguration` (defined in `mkctf.model.config.repository`)
- `chal_conf`: an instance of `ChallengeConfiguration` (defined in `mkctf.model.config.challenge`)

You can access members of both instances within the template.

**Warning: keep in mind that you should not alter these configurations from your template!**
