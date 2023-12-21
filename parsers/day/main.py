from parsers.day.source import *


def main():
    config, sections = ParseConfig('parsers/day')
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
                if raw:
                    advertise, real = ProcessData(raw, heading, word, page)
                    advertise = FilterByBarcode(advertise, barcodes)
                    real = FilterByBarcode(real, barcodes)
                    ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, advertise, heading, SHEET_ID, service, row)
                    ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, real, PREFIX + heading, SHEET_ID, service, row)
                    row += len(advertise)
                else:
                    Stamp(f'Page {page} is empty', 'w')
                Sleep(SHORT_SLEEP, ratio=0.5)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', heading, len(COLUMNS), SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', PREFIX + heading, len(COLUMNS), SHEET_ID, service)
        Stamp(f'End of processing {heading}', 'b')
    Finish(TIMEOUT, NAME)


def FilterByBarcode(list_for_filter: list, barcodes: list):
    filtered_list = []
    for sublist in list_for_filter:
        if sublist[0] in barcodes:
            filtered_list.append(sublist)
    return filtered_list


if __name__ == '__main__':
    main()
