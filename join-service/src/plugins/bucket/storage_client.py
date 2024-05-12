from google.cloud import storage
import os

bucket_name = os.environ.get("BUCKET_NAME")
credentials_path = os.environ.get("CREDENTIALS_PATH")

storage_client = storage.Client.from_service_account_json(credentials_path)


bucket = storage_client.bucket(bucket_name)


def upload_image(task_id):
    source_file_name = os.path.join(
        os.getcwd(), "tmp", "results", f"{task_id}.png")

    destination_file_name = f"results/{task_id}.png"

    # Subo el fragmento al bucket
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)


def download_image(fragment_name):
    if not os.path.exists('tmp'):
        os.makedirs('tmp/fragments')

    # Descargo el fragmento original del bucket
    blob = bucket.blob(f"post-sobel/{fragment_name}")
    blob.download_to_filename(f"tmp/fragments/{fragment_name}")

    # Una vez descargado, elimina el fragmento del bucket
    blob.delete()
