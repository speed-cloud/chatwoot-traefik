# chatwoot-traefik
Provides a simple way to dynamicly provision Chatwoot portal domains on Traefik.

## How to configure?
This project is only available for Docker installations of Chatwoot. <br />
No support will be provided for running this script on baremetal environment.

Only add this code to your stack: 
```yaml
services:
  # (...)

  traefik-provider:
    image: ghcr.io/speed-cloud/chatwoot-traefik
    env_file: .env
```

To configure Traefik, please refer to [their documentation](https://doc.traefik.io/traefik/providers/http/).

✅ A healthcheck is already included in the image. <br />
✅ No ports need to be exposed to the outside world. <br />
✅ The code is understable by everyone with a little bit of knowledge. <br />

Happy Chatwoot-ing!

*This project is nor endorsed, nor affiliated with Chatwoot, Inc.* <br />
*All support is provided by Groupe Speed Cloud, a nonprofit based in France 🇫🇷.*
