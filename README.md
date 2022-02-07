<img src=".github/media/banner.png" width="100%"/>

---

This little python script fetches all your starred repositories from your GitHub account and clones them to your server so you will never lose important resources!

# Usage

This script is designed to be used with cron. So, first of all, please install cron if it is not already installed.

You can configure the script either via environment variables (keys uppercase with `SG_` as prefix) or via a configuration file located in the current work directory, in your home directory at `.stargrab/config.*` or at `/etc/stargrab/config.*`. Both `yaml` and `json` files are accepted as config file formats.

These are the available configurations.
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `github_token` | `string` | Yes | The GitHub API token to authenticate you against the API. It can be obtained from [here](https://github.com/settings/tokens). |
| `target` | `string` | No (default: `repositories`) | The target location where repository mirros should be stored. |
| `user` | `string` | No (default: `viewer`) | The user to grab starred repositories from. Defaultly, this will be the user authenticated with the GitHub token. |
| `ignore` | `string` | No | A regular expression applied on the lowercased `username/reponame` of each repository. When it matches, the repository is ignored. |
| `depth` | `number` | No | Specify a maximum commit depth for repositories on initial clone. |

## Run barely

Of course, you need python3 and git to be installed on your system.

Now, clone the repository into your home directory.
```
git clone https://github.com/zekrotja/stargrab ~/stargrab
```

Then, you want to install the required dependencies of the script.
```
python3 -m pip install -r ~/stargrab/requirements.txt
```

After that, create a location to store the repository mirrors to.
```
mkdir ~/stargrab_repos
```

Following, create the config in your home directory and enter your configuration.
```
mkdir ~/.stargrab
vim ~/.stargrab/config.yml
```

Next, create a crontab entry to execute the script periodically.
```
crontab -e
```

The entry could look like following. This will execute the mirroring every day at 3am.
```
0 3 * * * python3 /home/<yourUserName>/stargrab/stargrab/main.py >> /home/<yourUserName>/stargrab/log 2>&1
```

## Run with Docker

Therefore, you need Docker to be installed on your system, of course.

First, pull the image from GHCR.
```
docker pull ghcr.io/zekrotja/stargrab:latest
```

Optionally, you can now tag the image for simplicity.
```
docker tag ghcr.io/zekrotja/stargrab:latest stargrab:latest
```

Next, create a crontab entry to execute the Docker image periodically.
```
crontab -e
```

The entry could look like following. This will execute the mirroring every day at 3am.
```
0 3 * * * docker run --rm --env SG_GITHUB_TOKEN="<yourGitHubToken>" -v /home/<yourUserName>/stargrab_repos:/var/repos stargrab
```
