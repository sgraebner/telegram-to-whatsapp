# Telegram Bot to WhatsApp

This project includes a script that listens to Telegram channels, downloads images, and forwards them to WhatsApp using a specified API.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**:
   - Update the `.env` file with your credentials and paths.

3. **Running the Script**:
   ```bash
   python run.py
   ```

## Setting Up as a Service

To ensure the script runs continuously and starts automatically at boot, you can set it up as a systemd service on Linux systems.

1. **Create a systemd service file**:
   - Open your terminal and create a new service file in `/etc/systemd/system/` using your favorite text editor (e.g., nano):
     ```bash
     sudo nano /etc/systemd/system/telegram_bot.service
     ```

2. **Add the following content to the service file**:
   - Replace `User`, `Group`, and `WorkingDirectory` with appropriate values for your setup.
   ```ini
   [Unit]
   Description=Telegram Bot Service
   After=network.target

   [Service]
   User=your_user
   Group=your_group
   WorkingDirectory=~/telegram_bot
   ExecStart=/path/to/python ~/telegram_bot/run.py

   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start the service**:
   - Reload the systemd manager configuration to include your new service:
     ```bash
     sudo systemctl daemon-reload
     ```
   - Enable the service to start at boot:
     ```bash
     sudo systemctl enable telegram_bot.service
     ```
   - Start the service immediately:
     ```bash
     sudo systemctl start telegram_bot.service
     ```

4. **Check the status of your service**:
   - You can check the status to ensure it's running properly:
     ```bash
     sudo systemctl status telegram_bot.service
     ```

## Project Structure

- `run.py`: Main script file.
- `.env`: Environment variables.
- `requirements.txt`: Python dependencies.

## License

MIT License.
```

### Notes on Creating the Service

- **User and Group**: Make sure to replace `your_user` and `your_group` with the username and group under which you want the service to run. This is typically the user you log in with if it's a personal project.
- **ExecStart**: This line should point to the absolute path of the Python interpreter and the script. If you're using a virtual environment, make sure the path points to the Python executable inside your virtual environment.
- **WorkingDirectory**: This is the directory where your script and `.env` file are located. It should be the full path to your project directory.
