from google.cloud import storage
import os

bucket_name = os.environ.get("BUCKET_NAME")
credentials_path = os.environ.get("CREDENTIALS_PATH")

storage_client = storage.Client.from_service_account_json(credentials_path)

bucket = storage_client.bucket(bucket_name)


def upload_image(fragment_name):
    # Subo el fragmento sobelizado al bucket
    source_file_name = os.path.join(os.getcwd(), "tmp", "post", fragment_name)
    destination_file_name = f"post-sobel/{fragment_name}"

    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)


def download_image(fragment_name):
    if not os.path.exists('tmp'):
        os.makedirs('tmp/pre')

    # Descargo el fragmento original del bucket
    blob = bucket.blob(f"pre-sobel/{fragment_name}")
    blob.download_to_filename(f"tmp/pre/{fragment_name}")

    # Una vez descargado, elimina el fragmento del bucket
    blob.delete()
