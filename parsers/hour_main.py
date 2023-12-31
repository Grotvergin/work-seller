from parsers.source import *


def Main():
    config, sections = ParseConfig(NAME.lower())
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        column, sheet_id = ParseCurrentHeading(config, heading, 'Hour')
        row = 2
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', heading, len(COLUMNS), sheet_id, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', PREFIX + heading, len(COLUMNS), sheet_id, service)
        barcodes = GetColumn(config[heading]['Column'], service, 'Barcodes', TIMEOUT, NAME, sheet_id, LONG_SLEEP)
        words = GetColumn(config[heading]['Column'], service, 'Words', TIMEOUT, NAME, sheet_id, LONG_SLEEP)
        empty = PrepareEmpty(len(COLUMNS), BLANK_ROWS)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, heading, sheet_id, service, row)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, PREFIX + heading, sheet_id, service, row)
        for word in words:
            Stamp(f'Processing template: {word}', 'i')
            for page in range(1, PAGES_QUANTITY + 1):
                Stamp(f'Processing page {page}', 'i')
                PARAMS['page'] = page
                PARAMS['query'] = word
                raw = GetData(TIMEOUT, NAME)
                advertise, real = ProcessData(raw, word, page)
                advertise = FilterByBarcode(advertise, barcodes)
                real = FilterByBarcode(real, barcodes)
                ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, advertise, heading, sheet_id, service, row)
                ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, real, PREFIX + heading, sheet_id, service, row)
                row += len(advertise)
                Sleep(SHORT_SLEEP, 0.5)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', heading, len(COLUMNS), sheet_id, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', PREFIX + heading, len(COLUMNS), sheet_id, service)
    Finish(TIMEOUT, NAME)


if __name__ == '__main__':
    Main()
