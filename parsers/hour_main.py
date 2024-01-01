from parsers.source import *


def Main():
    config, sections = ParseConfig(NAME)
    service = BuildService()
    for heading in sections:
        Stamp(f'Processing {heading}', 'b')
        column, sheet_id = ParseCurrentHeading(config, heading, 'Hour')
        row = 2
        barcodes = GetColumn(config[heading]['Column'], service, 'Barcodes', sheet_id)
        words = GetColumn(config[heading]['Column'], service, 'Words', sheet_id)
        CleanSheet(len(COLUMNS), heading, sheet_id, service)
        CleanSheet(len(COLUMNS), PREFIX + heading, sheet_id, service)
        for word in words:
            Stamp(f'Processing template: {word}', 'i')
            for page in range(1, PAGES_QUANTITY + 1):
                Stamp(f'Processing page {page}', 'i')
                PARAMS['page'] = page
                PARAMS['query'] = word
                raw = GetData()
                advertise, real = ProcessData(raw, word, page)
                advertise = FilterByBarcode(advertise, barcodes)
                real = FilterByBarcode(real, barcodes)
                UploadData(advertise, heading, sheet_id, service, row)
                UploadData(real, PREFIX + heading, sheet_id, service, row)
                row += len(advertise)
                Sleep(SHORT_SLEEP, 0.5)
    Finish(NAME)


if __name__ == '__main__':
    Main()
