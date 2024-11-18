# Pokémon App Deployment (Linux)

This project allows users to interact with Pokémon data from the PokeAPI. The app includes a game where users can draw Pokémon, view their stats, and save them to a local file or a database. Additionally, the project includes a deployment script to set up the application on an AWS EC2 instance using Python and Boto3.

## Features

### Game Features
- Fetch random Pokémon details using the PokeAPI.
- Save Pokémon details to a JSON file or database.
- Display a list of saved Pokémon.
- Prevent duplicate Pokémon from being saved.

### Deployment Features
- Automatically provisions AWS infrastructure, including:
  - EC2 instance with a free-tier eligible AMI.
  - Security group with appropriate rules.
  - Key pair for SSH access.
- Installs dependencies and deploys the app from a GitHub repository.
- Configures the EC2 instance to run the app.

---

## Prerequisites

### Game
- Python 3.7 or higher

### Deployment
- AWS CLI configured with appropriate permissions
- Python 3.7 or higher
- Boto3 library (install using `pip install boto3`)
- An AWS account with free-tier eligibility

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/levi-ochana/Pokemon-API-and-JSON.git
   cd Pokemon-API-and-JSON

2. Ensure the AWS CLI is configured And Set Up PEM for SSH Access:
   ```bash
   aws configure
   vi ~/.ssh/my-key-pair.pem
   chmod 400 ~/.ssh/my-key-pair.pem

   
3. Run the deployment script:
   ```bash
   python3 deployment.py

4. After the script finishes, you will see the instance's public IP address in the output. Use it to connect via SSH. For example:
   ```bash
   ssh -i ~/.ssh/my-key-pair.pem ec2-user@<INSTANCE_PUBLIC_IP>

5. Run the game:
   ```bash
   cd Pokemon-API-and-JSON
   sudo python3 game.py


## Game Workflow
1. Draw a Pokémon: Fetches a random Pokémon and displays its details. If it's not already saved, it will be added to the local file/database.

2. View Saved Pokémon: Lists all Pokémon saved so far.

3. Exit: Ends the program.
