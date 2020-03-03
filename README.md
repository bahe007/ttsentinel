# ttsentinel
 `ttsentinel` is a minimal script for website monitoring. It can be configured with a `config.json` file that follows the format of the example file (the `offline` field should be left empty). 
 
 `ttsentinel` checks periodically a list of websites for uptime, meaning if the return `HTTP 200 OK` before a set timeout interval. If a website fails to do so, `ttsentinel` sends a notification email to you. You can configure:
 
 - timeout before which a website must respond
 - websites to check, and the target email address 
 - interval to wait between website checks
 - email server
 
 Find further explainations on [dev.to](https://dev.to/bahe007/is-your-website-really-online). 
