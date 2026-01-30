## 1. Configuration Setup

- [x] 1.1 Add batch configuration constants (`BATCH_SIZE`, `BATCH_PREFIX`)
- [x] 1.2 Add function `get_batch_config()` to read from Variable/DAG config
- [x] 1.3 Add `start_batch` config support for resume functionality

## 2. Batch Extraction

- [x] 2.1 Create function `split_dataframe_to_batches(df, batch_size)` using numpy.array_split
- [x] 2.2 Create function `write_batch_files(batches, prefix, data_dir)` with zero-padded naming
- [x] 2.3 Modify `extract_data()` to use batch splitting
- [x] 2.4 Update XCom return value with batch metadata structure

## 3. Batch Upload

- [x] 3.1 Create function `upload_batch(batch_file, config_dir, process_name)` for single batch
- [x] 3.2 Create function `upload_all_batches(batch_files, start_batch)` with sequential processing
- [x] 3.3 Add per-batch success/error log handling
- [x] 3.4 Create function `aggregate_logs(batch_files, log_dir)` to merge all batch logs
- [x] 3.5 Modify `run_dataloader` task to use batch upload logic

## 4. Batch Validation

- [x] 4.1 Modify `validate_extract_data()` to validate each batch file
- [x] 4.2 Add per-batch run_name for GX Data Docs separation
- [x] 4.3 Create function `aggregate_validation_results(batch_results)`
- [x] 4.4 Modify `validate_postmig_data()` to use aggregated success log
- [x] 4.5 Add per-batch reconciliation logging

## 5. Error Handling

- [x] 5.1 Add warning when batch_size < 1000
- [x] 5.2 Add handling for empty extraction (0 records)
- [x] 5.3 Add batch failure detection and logging
- [x] 5.4 Implement stop-on-failure for complete batch failures

## 6. Testing & Documentation

- [x] 6.1 Test with small batch size (100) to verify splitting logic
- [x] 6.2 Test resume functionality with `start_batch` config
- [x] 6.3 Update GREAT_EXPECTATIONS_PIPELINE.md with batch validation flow
- [x] 6.4 Add batch configuration to CLAUDE.md
