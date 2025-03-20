import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand
from dashboard.models import EnergyValveData

class Command(BaseCommand):
    help = 'Import comprehensive energy data from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Users/peter/Downloads/table1_3M.csv')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        self.stdout.write(f"Importing data from {csv_file}")
        
        # Read CSV with pandas, handling various potential issues
        try:
            df = pd.read_csv(csv_file, low_memory=False)
            initial_rows = len(df)
            self.stdout.write(f"Successfully read CSV with {len(df)} rows and {len(df.columns)} columns")
            self.stdout.write(f"Columns found: {', '.join(df.columns)}")
        except Exception as e:
            self.stderr.write(f"Error reading CSV file: {e}")
            return
        
        # Display initial data stats
        self.stdout.write(f"Data preview: {df.head(2)}")
        
        # Clean and process data
            # 1. Handle datetime columns
        time_columns = [col for col in df.columns if 'time' in col.lower()]
        self.stdout.write(f"Found time columns: {time_columns}")

        if 'sample_time' in df.columns:
            df['sample_time'] = pd.to_datetime(df['sample_time'], errors='coerce')
            # Filter out rows with NaT values
            df = df.dropna(subset=['sample_time'])
            self.stdout.write(f"Removed {initial_rows - len(df)} rows with invalid sample_time")
        elif 'cloud_received_time' in df.columns:
            df['sample_time'] = pd.to_datetime(df['cloud_received_time'], errors='coerce')
            # Filter out rows with NaT values
            df = df.dropna(subset=['sample_time'])
            self.stdout.write(f"Removed {initial_rows - len(df)} rows with invalid sample_time")
        else:
            # Try to find any datetime column
            datetime_found = False
            for col in time_columns:
                try:
                    df['sample_time'] = pd.to_datetime(df[col], errors='coerce')
                    # Filter out rows with NaT values
                    rows_before = len(df)
                    df = df.dropna(subset=['sample_time'])
                    self.stdout.write(f"Using {col} as sample_time")
                    self.stdout.write(f"Removed {rows_before - len(df)} rows with invalid {col}")
                    datetime_found = True
                    break
                except:
                    continue
            
            if not datetime_found:
                self.stderr.write("No valid datetime column found. Cannot import data.")
                return
            
        # 2. Remove duplicates
        initial_rows = len(df)
        df = df.drop_duplicates()
        self.stdout.write(f"Removed {initial_rows - len(df)} duplicate rows")
        
        # 3. Replace inf values with NaN
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # 4. Create device_id if it doesn't exist
        if 'device_id' not in df.columns:
            if 'device' in df.columns:
                df['device_id'] = df['device']
            else:
                self.stdout.write("No device_id column found. Creating default device_id.")
                df['device_id'] = 'default_device'
        
        # Map column names to model fields - be flexible with naming variations
        field_mappings = {
            # Temperature fields
            'T1_remote_K': 't1_remote_k',
            'T1_Remote_K': 't1_remote_k',
            't1_remote_k': 't1_remote_k',
            'T1': 't1_remote_k',
            
            'T2_embeded_K': 't2_embeded_k',
            'T2_embedded_K': 't2_embeded_k',
            'T2_Embedded_K': 't2_embeded_k',
            't2_embeded_k': 't2_embeded_k',
            'T2': 't2_embeded_k',
            
            # Delta T fields
            'DeltaT_K': 'delta_t_k',
            'Delta_T_K': 'delta_t_k',
            'deltaT': 'delta_t_k',
            'delta_t': 'delta_t_k',
            'delta_t_k': 'delta_t_k',
            
            # Flow fields
            'Flow_Volume_total_m3': 'flow_volume_total_m3',
            'Flow_Volume': 'flow_volume_total_m3',
            'flow_volume_total_m3': 'flow_volume_total_m3',
            'Flow': 'flow_volume_total_m3',
            
            # Operating hours fields
            'OperatingHours': 'operating_hours',
            'Operating_Hours': 'operating_hours',
            'operating_hours': 'operating_hours',
        }
        
        # Find matching columns and map them
        model_fields = {}
        for csv_col in df.columns:
            if csv_col in field_mappings:
                model_fields[field_mappings[csv_col]] = csv_col
                self.stdout.write(f"Mapped {csv_col} to {field_mappings[csv_col]}")
        
        # Check if we've found essential fields
        essential_fields = ['t1_remote_k', 't2_embeded_k', 'delta_t_k', 'flow_volume_total_m3', 'operating_hours']
        missing_fields = [field for field in essential_fields if field not in model_fields]
        
        if missing_fields:
            self.stdout.write(f"Warning: Missing essential fields: {missing_fields}")
            self.stdout.write(f"We'll import the data with null values for these fields.")
        
        # Create model instances
        records = []
        successful = 0
        failed = 0
        
        for _, row in df.iterrows():
            try:
                record = EnergyValveData(
                    device_id=row.get('device_id', 'unknown'),
                    sample_time=row['sample_time'],
                    t1_remote_k=row.get(model_fields.get('t1_remote_k')) if 't1_remote_k' in model_fields else None,
                    t2_embeded_k=row.get(model_fields.get('t2_embeded_k')) if 't2_embeded_k' in model_fields else None,
                    delta_t_k=row.get(model_fields.get('delta_t_k')) if 'delta_t_k' in model_fields else None,
                    flow_volume_total_m3=row.get(model_fields.get('flow_volume_total_m3')) if 'flow_volume_total_m3' in model_fields else None,
                    operating_hours=row.get(model_fields.get('operating_hours')) if 'operating_hours' in model_fields else None
                )
                records.append(record)
                successful += 1
            except Exception as e:
                failed += 1
                if failed < 10:  # Only show first 10 errors to avoid flooding console
                    self.stderr.write(f"Error processing row: {e}")
        
        # Bulk create records
        try:
            # Process in smaller batches to help identify problematic records
            batch_size = 1000
            for i in range(0, len(records), batch_size):
                batch = records[i:i+batch_size]
                try:
                    EnergyValveData.objects.bulk_create(batch)
                    self.stdout.write(f"Successfully imported batch {i//batch_size + 1}/{(len(records) + batch_size - 1)//batch_size}")
                except Exception as e:
                    self.stderr.write(f"Error during bulk create of batch {i//batch_size + 1}: {e}")
                    # Try to identify the problematic record
                    for j, record in enumerate(batch):
                        try:
                            record.save()
                        except Exception as record_error:
                            self.stderr.write(f"Error with record {i+j}: {record_error}")
                            # Print problematic record details for debugging
                            self.stderr.write(f"Record details: device_id={record.device_id}, sample_time={record.sample_time}")
            
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {successful} records. Failed: {failed}"))
        except Exception as e:
            self.stderr.write(f"Error during bulk create: {e}")