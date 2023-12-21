from parsers.hour.source import *


def main():
    config, sections = ParseConfig('parsers/hour')
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', heading, len(COLUMNS), SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', PREFIX + heading, len(COLUMNS), SHEET_ID, service)
        row = 2
        words = GetColumn(config[heading]['Column'], service, 'Words', TIMEOUT, NAME, SHEET_ID, LONG_SLEEP)
        empty = PrepareEmpty(len(COLUMNS), BLANK_ROWS)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, heading, SHEET_ID, service, row)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, PREFIX + heading, SHEET_ID, service, row)
        for word in words:
            Stamp(f'Processing template: {word}', 'i')
            for page in range(1, PAGES_QUANTITY + 1):
                Stamp(f'Processing page {page}', 'i')
                PARAMS['page'] = page
                PARAMS['query'] = word
                raw = GetData(TIMEOUT, NAME)
                if raw:
                    advertise, real = ProcessData(raw, heading, word, page)
                    ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, advertise, heading, SHEET_ID, service, row)
                    ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, real, PREFIX + heading, SHEET_ID, service, row)
                    row += len(advertise)
                else:
                    Stamp(f'Page {page} is empty', 'w')
                Sleep(SHORT_SLEEP, 0.5)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', heading, len(COLUMNS), SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', PREFIX + heading, len(COLUMNS), SHEET_ID, service)
        Stamp(f'End of processing {heading}', 'b')
    Finish(TIMEOUT, NAME)


if __name__ == '__main__':
    main()
