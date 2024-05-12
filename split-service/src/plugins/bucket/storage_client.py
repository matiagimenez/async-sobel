from google.cloud import storage
import os

bucket_name = os.environ.get("BUCKET_NAME")
credentials_path = os.environ.get("CREDENTIALS_PATH")

storage_client = storage.Client.from_service_account_json(credentials_path)


bucket = storage_client.bucket(bucket_name)


def upload_image(fragment_name):
    source_file_name = os.path.join(os.getcwd(), "tmp", fragment_name)
    destination_file_name = f"pre-sobel/{fragment_name}"

    # Subo el fragmento al bucket
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)
