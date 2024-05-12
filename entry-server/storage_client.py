from google.cloud import storage
import os

bucket_name = os.environ.get("BUCKET_NAME")
credentials_path = os.environ.get("CREDENTIALS_PATH")

storage_client = storage.Client.from_service_account_json(credentials_path)

bucket = storage_client.bucket(bucket_name)


def check_result(task_id):
    # if not os.path.exists('tmp'):
    #     os.makedirs('tmp/results')

    bucket_object = f"results/{task_id}.png"
    blob = bucket.blob(bucket_object)

    if not blob.exists():
        return False

    return blob.public_url

    # Descargo el resultado final desde el bucket
    # blob.download_to_filename(f"tmp/results/{task_id}.png")

    # Una vez descargado, elimina el fragmento del bucket
    # blob.delete()
