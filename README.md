# Gitlab Backup Manager (GLBM)

Gitlab Backup Manager is a tool to help manage Backups of Gitlab in one place.

>**Main Backup** = gitlab-rake gitlab:backup:create<br>
 __Backup Config__ = gitlab-ctl backup-etc

<hr>

## Getting started
### Configuration Options
Configuration settings are used in the following order:
>1. Config YAML file ( see order below )
>2. OS Environment Variables

The order of config file checking location
>1. local directory where executable is running (Mostly used for dev.) - config.yaml
>2. $HOME/.config/glbm/config.yaml
>3. /etc/glbm_config.yaml

#### OS Environment Variables
>**GLBM_S3_BUCKET** # Bucket name **(required)**<br>
>**GLBM_S3_ENDPOINT_URL** # URL to S3 **(required)**<br>
>**GLBM_S3_DIRECTORY** # Directory path in bucket **(required)**<br>
>**GLBM_DAYS_TO_KEEP** # Keep _X_ days worth of backups **(default: 30)**<br>
>**GLBM_NOTIFICATIONS_ENABLED** #Send to Slack **(default: "false")**<br>
>**GLBM_SLACK_TOKEN**<br>
>**GLBM_SLACK_CHANNEL_ID**<br>
>**GLBM_LOGGING_LEVEL** # INFO, DEBUG, WARNING, ERROR & CRITICAL **(defualt: INFO)**<br>

#### Config file example
*Config file used same settings as OS Env above, but lowercase, and remove `GLBM_`

>**s3_bucket**: bucket1<br>
>**s3_endpoint_url**: https://\<domain\>/\<path\>:\<port\><br>
>**s3_directory**: gl_backups<br>
>**days_to_keep**: 14<br>
>**notifications_enabled**: "true"<br>
>**slack_token**: xoxb-xxxxxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxxxxx<br>
>**slack_channel_id**: "ABCDEFGHIJC"<br>
>**logging_level**: "DEBUG"<br>


### Installation (Preferred)

```sh
$ pip installl gitlab_bm
```

After install run the following to see default opitions:

```
$ glbm
Usage: glbm [OPTIONS] COMMAND [ARGS]...

  Gitlab Backup Manager (GLBM) Ver. (x.x.x)

Options:
  --version  Show application Version
  --help     Show this message and exit.

Commands:
  backup            Run Main Backup
  backup-etc        Run Backup Config and upload to S3
  complete          Run backup, backup_etc, upload to S3
  delete-files      Delete old files from S3 based on (X) days to keep
```

<hr>

## Current Limitations

* Only supports Slack Notifications
* Manual setup of **Main Backup** in `gitlab.rb` still needed
* (Scheduling of jobs) - Need to manually setup.

### Development

Want to contribute? Great!  No specifics at this point.  Just basic GitHub Fork and Pull request.<br>
For further info, see [github guide] on contributing to opensource project.<br>

After cloning your Forked branch locally, and installing Poetry, you can run the following to setup dev env and test:

```sh
$ poetry install
```
Then to run, do the following:
```
$ poetry run glbm
```


License
----

MIT [LICENSE.txt]

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [LICENSE.txt]: <https://github.com/CodeBleu/rabbitmqStats/LICENSE.txt>
   [Github Guide]: <https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project>
