import os
import csv
import tempfile
import pytest
from calculate_ges import calculate_ges

def write_csv(rows, fieldnames):
    tmp = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
    writer = csv.DictWriter(tmp, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    tmp.close()
    return tmp.name

def test_empty_log():
    path = write_csv([], ['topic', 'revision_cycles', 'final_decision', 'grounded'])
    result = calculate_ges(path)
    os.unlink(path)
    assert result == {
        'ges': 0.0,
        'approval_rate': 0.0,
        'avg_revision_cycles': 0.0,
        'groundedness_rate': 0.0
    }

def test_all_approved_grounded():
    rows = [
        {'topic': 'A', 'revision_cycles': '2', 'final_decision': 'approve', 'grounded': 'True'},
        {'topic': 'B', 'revision_cycles': '1', 'final_decision': 'approve', 'grounded': 'True'}
    ]
    path = write_csv(rows, ['topic', 'revision_cycles', 'final_decision', 'grounded'])
    result = calculate_ges(path)
    os.unlink(path)
    assert result['approval_rate'] == 1.0
    assert result['groundedness_rate'] == 1.0
    assert result['avg_revision_cycles'] == 1.5
    assert 0.0 <= result['ges'] <= 1.0

def test_mixed():
    rows = [
        {'topic': 'A', 'revision_cycles': '4', 'final_decision': 'approve', 'grounded': 'False'},
        {'topic': 'B', 'revision_cycles': '2', 'final_decision': 'reject', 'grounded': 'False'},
        {'topic': 'C', 'revision_cycles': '3', 'final_decision': 'approve', 'grounded': 'True'}
    ]
    path = write_csv(rows, ['topic', 'revision_cycles', 'final_decision', 'grounded'])
    result = calculate_ges(path)
    os.unlink(path)
    assert abs(result['approval_rate'] - 2/3) < 1e-6
    assert abs(result['groundedness_rate'] - 0.5) < 1e-6
    assert abs(result['avg_revision_cycles'] - 3.0) < 1e-6
    assert 0.0 <= result['ges'] <= 1.0

def test_no_approved():
    rows = [
        {'topic': 'A', 'revision_cycles': '2', 'final_decision': 'reject', 'grounded': 'True'}
    ]
    path = write_csv(rows, ['topic', 'revision_cycles', 'final_decision', 'grounded'])
    result = calculate_ges(path)
    os.unlink(path)
    assert result['approval_rate'] == 0.0
    assert result['groundedness_rate'] == 0.0
    assert result['avg_revision_cycles'] == 2.0
    assert 0.0 <= result['ges'] <= 1.0
