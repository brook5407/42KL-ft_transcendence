# Ft_transcendence

- Python Version: 3.12.0
- Created by: <b>Brook, Qixeo, Joseph, Xuerui, Mark </b>


## Dev Setup

```bash
# Setup and activate python virtual environment for dev
$ python3 -m venv .venv
$ source .venv/bin/activate # use the deactivate command to deactivate the venv
$ pip install -r requirements.txt

# create the .env file
$ cp .env.example .env

# generate the secret key for django and copy it, paste to .env DJANGO_SECRET_KEY
$ python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

# spawn all docker containers, networks and volumes
$ make build-up

# When you change any of the django files, the django dev server will reload thanks to docker volume and watchdog

# stop all containers
$ make down
```


## Modules

### Web
- [x] Major module: Use a Framework as backend.
- [x] Minor module: Use a front-end framework or toolkit.
- [x] Minor module: Use a database for the backend.
- [x] Major module: Store the score of a tournament in the Blockchain.

### User Management
- [x] Major module: Standard user management, authentication, users across
tournaments. - -**By Brook (WIP)**
- [x] Major module: Implementing a remote authentication. -**By Brook**

### Gameplay and user experience
- [x] Major module: Remote players
- [ ] Major module: Multiplayers (more than 2 in the same game).
- [x] Major module: Add Another Game with User History and Matchmaking.
- [ ] Minor module: Game Customization Options.
- [x] Major module: Live chat.

### AI-Algo
- [x] Major module: Introduce an AI Opponent.
- [ ] Minor module: User and Game Stats Dashboards

### Cybersecurity
- [ ] Major module: ImplementWAF/ModSecurity with Hardened Configuration
and HashiCorp Vault for Secrets Management.
- [ ] Minor module: GDPR Compliance Options with User Anonymization, Local
Data Management, and Account Deletion.
- [x] Major module: Implement Two-Factor Authentication (2FA) and JWT.

### Devops
- [ ] Major module: Infrastructure Setup for Log Management.
- [ ] Minor module: Monitoring system.
- [ ] Major module: Designing the Backend as Microservices.

### Graphics
- [ ] Major module: Use of advanced 3D techniques.

### Accessibility
- [ ] Minor module: Support on all devices.
- [x] Minor module: Expanding Browser Compatibility.
- [ ] Minor module: Multiple language supports.
- [ ] Minor module: Add accessibility for Visually Impaired Users.
- [ ] Minor module: Server-Side Rendering (SSR) Integration.

### Server-Side Pong
- [ ] Major module: Replacing Basic Pong with Server-Side Pong and Implementing
an API.
- [ ] Major module: Enabling Pong Gameplay via CLI against Web Users with
API Integration.

## Reference

AllAuth Provider - 
https://www.chenshiyang.com/archives/696

