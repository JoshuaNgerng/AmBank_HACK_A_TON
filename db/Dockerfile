FROM postgres:16

# Copy the initialization script
COPY init.sh /init.sh

# Ensure the script is executable
RUN chmod +x /init.sh

# Default PostgreSQL behavior
CMD ["/init.sh"]