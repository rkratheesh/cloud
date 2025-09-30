FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y wget ca-certificates gnupg --no-install-recommends && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/postgresql-keyring.gpg] http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && \
    apt-get install -y supervisor nano procps gettext libcairo2-dev gcc postgresql-client-16 --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app/

# Upgrade pip inside the venv
RUN pip install --upgrade pip

# Copy only requirements first (to use Docker caching)
COPY requirements.txt .

RUN pip install -r requirements.txt 


# Create necessary directories
RUN mkdir -p /var/log /var/run /etc/supervisor/conf.d && chmod 755 /var/log /var/run

# Copy the supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#copying the temp 

# Copy the rest of the application files
COPY . .

# Expose the application port 
EXPOSE 8000            
  
# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make it executable
RUN chmod +x /entrypoint.sh

# Use entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Start Supervisor
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
