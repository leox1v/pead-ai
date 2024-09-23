import boto3
import pandas as pd
from typing import Dict, List, Tuple

class TableImageToCSV:
    def __init__(self, region_name: str, aws_access_key_id: str, aws_secret_access_key: str):
        self.textract = boto3.client(
            'textract',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    def process_image(self, image_path: str) -> str:
        with open(image_path, 'rb') as document:
            image_bytes = document.read()

        response = self.textract.analyze_document(
            Document={'Bytes': image_bytes},
            FeatureTypes=['TABLES']
        )

        blocks = response['Blocks']
        blocks_map = {block['Id']: block for block in blocks}
        table_blocks = [block for block in blocks if block['BlockType'] == "TABLE"]

        return self._generate_csv(table_blocks, blocks_map)

    def _generate_csv(self, table_blocks: List[Dict], blocks_map: Dict) -> str:
        return '\n\n'.join(self._generate_table_csv(table, blocks_map, index)
                           for index, table in enumerate(table_blocks, 1))

    def _generate_table_csv(self, table: Dict, blocks_map: Dict, table_index: int) -> str:
        rows, _ = self._get_rows_columns_map(table, blocks_map)
        return '\n'.join(','.join(cols[col_index] for col_index in sorted(cols))
                         for row_index, cols in sorted(rows.items()))

    def _get_rows_columns_map(self, table: Dict, blocks_map: Dict) -> Tuple[Dict[int, Dict[int, str]], List[str]]:
        rows = {}
        scores = []
        for relationship in table['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell = blocks_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        rows.setdefault(row_index, {})[col_index] = self._get_text(cell, blocks_map)
                        scores.append(str(cell['Confidence']))
        return rows, scores

    def _get_text(self, result: Dict, blocks_map: Dict) -> str:
        text_parts = []
        if 'Relationships' in result:
            for relationship in result['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        word = blocks_map[child_id]
                        if word['BlockType'] == 'WORD':
                            text = word['Text']
                            if ',' in text and text.replace(',', '').isnumeric():
                                text = f'"{text}"'
                            text_parts.append(text)
                        elif word['BlockType'] == 'SELECTION_ELEMENT' and word['SelectionStatus'] == 'SELECTED':
                            text_parts.append('X')
        return ' '.join(text_parts)

# # Usage
# converter = TableImageToCSV(
#     region_name='eu-central-1',
#     aws_access_key_id='YOUR_ACCESS_KEY',
#     aws_secret_access_key='YOUR_SECRET_KEY'
# )
# csv_content = converter.process_image('path/to/your/image.jpg')
# print(csv_content)