from parsers.source import *

NAME = 'Day Parser'
SHEET_ID = '15tTuPqeiD418ts7DHZeX-GyaqRxETS5qmQFClfjfTYQ'


def main():
    config, sections = ParseConfig('parsers')
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', heading, len(COLUMNS), SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', PREFIX + heading, len(COLUMNS), SHEET_ID, service)
        barcodes = GetColumn(config[heading]['Column'], service, 'Barcodes', TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
        words = GetColumn(config[heading]['Column'], service, 'Words', TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
        row = len(GetColumn('A', service, heading, TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)) + 2
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
                ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, advertise, heading, SHEET_ID, service, row)
                ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, real, PREFIX + heading, SHEET_ID, service, row)
                row += len(advertise)
                Sleep(SHORT_SLEEP, 0.5)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', heading, len(COLUMNS), SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', PREFIX + heading, len(COLUMNS), SHEET_ID, service)
        Stamp(f'End of processing {heading}', 'b')
    Finish(TIMEOUT, NAME)


if __name__ == '__main__':
    main()
