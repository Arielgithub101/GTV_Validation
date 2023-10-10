from pydantic import BaseModel, Field


class FileInfo(BaseModel):
    account_name: str = Field(..., min_length=3, max_length=50,
                              description="Account name must be between 3 and 50 characters")
    container_name: str = Field(..., min_length=3, max_length=50,
                                description="Container name must be between 3 and 50 characters")
    blob_name: str = Field(..., min_length=3, max_length=50,
                           description="Folder name must be between 3 and 50 characters")
