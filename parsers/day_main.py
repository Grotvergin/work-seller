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
            page = 1
            while page <= PAGES_QUANTITY:
                Stamp(f'Processing page {page}', 'i')
                PARAMS['page'] = page
                PARAMS['query'] = word
                raw = GetData(proxies)
                if not InDict('data', raw):
                    Stamp('No key <<data>> in response, processing again', 'w')
                    page -= 1
                    continue
                advertise, real = ProcessData(raw, word, page)
                real_pages += FilterByBarcode(real, barcodes)
                advertise_pages += FilterByBarcode(advertise, barcodes)
                page += 1
                AccurateSleep(SHORT_SLEEP, 0.5)
            UploadData(advertise_pages, heading, sheet_id, service, row)
            UploadData(real_pages, PREFIX + heading, sheet_id, service, row)
            row += len(advertise_pages)


if __name__ == '__main__':
    Main()
