import os
import requests
import boto3
from datetime import datetime, timedelta
from stream_unzip import stream_unzip
from airflow import DAG
from airflow.operators.python import PythonOperator

# Define environment metadata metrics
DEFAULT_ARGS = {
    'owner': 'Martins Ifeanyi Nnadi',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Strict byte-chunk normaliser for boto3 multi-part compatibility
class FixedSizeStreamReader:
    def __init__(self, generator):
        self.gen = generator
        self.buffer = b''

    def read(self, size=-1):
        if size is None or size < 0:
            out = self.buffer + b''.join(self.gen)
            self.buffer = b''
            return out
        while len(self.buffer) < size:
            try:
                chunk = next(self.gen)
                self.buffer += chunk
            except StopIteration:
                break
        out = self.buffer[:size]
        self.buffer = self.buffer[size:]
        return out

def stream_chunks(source_url):
    headers = {'User-Agent': 'Mozilla/5.0 DataEngineeringPipeline/1.0'}
    with requests.get(source_url, headers=headers, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=65536): # 64KB network buffer
            yield chunk

def stream_sensor_package_to_s3():
    """
    High-capacity cloud data ingestion for streaming sensor data.
    Streams and de-serializes the archive directly to AWS staging boundaries without disk overhead.
    """
    print("[1/2] Initiating streaming connection to high-frequency sensor cache...")
    # This is the exact verified working URL from your execution
    SOURCE_URL = "https://uni-siegen.sciebo.de/public.php/dav/files/HGdUkoNlW1Ub0Gx"
    S3_BUCKET_NAME = "hcai-wesad-bronze-landing"
    
    try:
        s3_client = boto3.client('s3')
        zipped_chunks = stream_chunks(SOURCE_URL)

        print("[2/2] De-serializing archive in-flight and injecting straight into Amazon S3...")
        for file_name, file_size, unzipped_chunks in stream_unzip(zipped_chunks):
            s3_key_path = file_name.decode('utf-8')
            
            # Skip empty directory metadata anchors
            if s3_key_path.endswith('/'):
                continue
                
            print(f" Syncing stream: {s3_key_path} ({file_size} bytes)")
            
            # Re-packetize the unzipped stream data for boto3 compliance
            wrapped_stream = FixedSizeStreamReader(unzipped_chunks)
            s3_client.upload_fileobj(wrapped_stream, S3_BUCKET_NAME, s3_key_path)

        print(f"\n🚀 SUCCESS: Telemetry package successfully landed inside AWS storage boundaries.")
        
    except Exception as e:
        print(f"❌ AWS INGESTION FAILURE ERROR: {str(e)}")
        raise e

# Initialize the master scheduler control DAG
with DAG(
    'wesad_bronze_sensor_ingestion',
    default_args=DEFAULT_ARGS,
    description='Automated HCAI Ingestion Pipeline for high-frequency wearable streaming data',
    schedule_interval='@weekly',
    catchup=False,
) as dag:

    execute_ingestion_task = PythonOperator(
        task_id='stream_wesad_to_bronze_s3',
        python_callable=stream_sensor_package_to_s3,
    )
