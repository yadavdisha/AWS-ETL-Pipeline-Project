import pyodbc
import boto3
from datetime import datetime

# Generate filename with timestamp to avoid overwrites
filename = f'export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

try:
    # Connect to SQL Server
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=Hospital-Raw-data;'
        'UID=sa;'
        'PWD=Dy@1997&&'
    )
    
    # Export data to CSV
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM hospital")  # Verify table name is correct
        
        # Write to CSV with headers
        with open(filename, 'w', newline='') as f:
            # Write column headers
            headers = [column[0] for column in cursor.description]
            f.write(','.join(headers) + '\n')
            
            # Write data rows
            for row in cursor:
                f.write(','.join(map(str, row)) + '\n')
    
    # Upload to S3
    s3 = boto3.client('s3')
    s3.upload_file(
        filename,
        'hospital-de-raw-data-dev',
        f'hospital/raw_data/{filename}'  # Now using valid filename
    )
    print("Upload successful!")

except Exception as e:
    print(f"Error occurred: {str(e)}")
finally:
    if 'conn' in locals():
        conn.close()