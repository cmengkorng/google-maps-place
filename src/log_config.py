
# Function to get logger in other files
def get_logger(name):
    import logging
    import os
    from logging.handlers import RotatingFileHandler

    # Ensure "logs/" directory exists
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Create logger
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)  # Capture all logs
    
    # Create rotating file handler (5MB per file, keeps 3 backups)
    file_handler = RotatingFileHandler(
        os.path.join(log_directory, "app.log"), maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)

    # Create console handler (stream handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)  # Show all logs in console

    # Define the log format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Apply formatter to both handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logging.getLogger(name)
