import os


class Config:
    LOGS_FILE_PATH: str = os.environ['logs_file_path']
    DEVIATION_RANGE: int = int(os.environ['deviation_range'])
    PORT: int = 9900
    HOST: str = "0.0.0.0"

