import sys
import os
import json
from typing import Dict, Any, List

import pandas as pd


COLUMNS = [
    'SR ID', 'Summary', 'Priority', 'Status',
    'Classification', 'Expected Path', 'Complexity', 'Interface Risk',
    'Suggested Workaround', 'Recommended Action', 'Issue Type',
    'Confidence', 'Functional Area', 'Application', 'Prediction'
]


def quality_report(path: str) -> Dict[str, Any]:
    df = pd.read_excel(path)
    report: Dict[str, Any] = {
        'file': os.path.abspath(path),
        'rows': int(len(df)),
        'columns': list(df.columns),
        'metrics': {}
    }
    if len(df) == 0:
        return report

    for col in COLUMNS:
        if col not in df.columns:
            report['metrics'][col] = {'present': False}
            continue
        series = df[col].astype(str)
        n = len(series)
        is_missing = series.isna()
        is_empty = series.str.strip().eq('')
        is_unknown = series.str.lower().isin({'unknown', 'n/a', 'none'})
        bad = (is_missing | is_empty | is_unknown)
        good_count = int((~bad).sum())
        report['metrics'][col] = {
            'present': True,
            'filled': good_count,
            'pct_filled': round(100.0 * good_count / max(n, 1), 1),
        }
    return report


def main(argv: List[str]) -> None:
    if len(argv) < 2:
        print('Usage: analyze_exports.py <file1.xlsx> [file2.xlsx]')
        sys.exit(1)
    paths = argv[1:]
    outputs = [quality_report(p) for p in paths]
    # If two files, add a quick comparison for key columns
    result: Dict[str, Any] = {'reports': outputs}
    if len(outputs) == 2:
        a, b = outputs
        diffs = {}
        for col in COLUMNS:
            if a['metrics'].get(col, {}).get('present') and b['metrics'].get(col, {}).get('present'):
                diffs[col] = {
                    'from_pct': a['metrics'][col]['pct_filled'],
                    'to_pct': b['metrics'][col]['pct_filled'],
                    'delta_pct': round(b['metrics'][col]['pct_filled'] - a['metrics'][col]['pct_filled'], 1)
                }
        result['comparison'] = diffs
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main(sys.argv)


