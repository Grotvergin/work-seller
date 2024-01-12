from parsers.source import *


@Inspector('day_main')
def Main():
    config, sections = ParseConfig(NAME)
    service = BuildService()
    for heading in sections:
        Stamp(f'Processing {heading}', 'b')
        column, sheet_id, proxies = ParseCurrentHeading(config, heading, 'Day')
        barcodes = GetColumn(column, service, 'Barcodes', sheet_id)
        words = GetColumn(column, service, 'Words', sheet_id)
        row = len(GetColumn('A', service, heading, sheet_id)) + 2
        for word in words:
            Stamp(f'Processing template: {word}', 'i')
            real_pages = []
            advertise_pages = []
            for page in range(1, PAGES_QUANTITY + 1):
                Stamp(f'Processing page {page}', 'i')
                PARAMS['page'] = page
                PARAMS['query'] = word
                raw = GetData(proxies)
                advertise, real = ProcessData(raw, word, page)
                real_pages += FilterByBarcode(real, barcodes)
                advertise_pages += FilterByBarcode(advertise, barcodes)
                Sleep(SHORT_SLEEP)
            UploadData(advertise_pages, heading, sheet_id, service, row)
            UploadData(real_pages, PREFIX + heading, sheet_id, service, row)
            row += len(advertise_pages)


if __name__ == '__main__':
    Main()
