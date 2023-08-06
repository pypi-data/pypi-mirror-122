# XBEL generator from YAML

This generator can generate XBEL for bookmark exchange and storage from YAML
format.

YAML input:

```yaml
Comics:
  xkcd: 'https://xkcd.com'
  SMBC: 'https://smbc-comics.com'
  Pepper and Carrot: 'https://www.peppercarrot.com/'
Specifications:
  Activity Streams 2.0: 'https://www.w3.org/TR/activitystreams-core/'
  SMTP: 'https://datatracker.ietf.org/doc/html/rfc5321'
```

This should generate two folders, "Comics" and "Specifications", with the first
one containing `https://xkcd.com` bookmarked under title "xkcd" and so on.
