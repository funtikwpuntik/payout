import pytest
from main import get_head_idx, report_payout

@pytest.fixture
def sample_csv_file(tmp_path):
    csv_data = """id,email,name,department,hours_worked,hourly_rate
1,test1@example.com,John Doe,IT,40,50
2,test2@example.com,Jane Smith,HR,35,45
3,test3@example.com,Bob Johnson,IT,45,55"""

    file_path = tmp_path / "sample.csv"
    file_path.write_text(csv_data)
    return str(file_path)

@pytest.fixture
def sample_dict_data():
    return {
        "department": ["IT", "HR", "IT"],
        "name": ["John Doe", "Jane Smith", "Bob Johnson"],
        "hours_worked": [40, 35, 45],
        "hourly_rate": [50, 45, 55],
    }

def test_get_head_idx():
    headers = ["id", "email", "name", "department", "hours_worked", "hourly_rate"]
    expected = [0, 1, 2, 3, 4, 5]
    assert get_head_idx(headers) == expected

    headers_with_rate = ["hours_worked", "name", "email", "department", "id", "rate"]
    expected = [4, 2, 1, 3, 0, 5]
    assert get_head_idx(headers_with_rate) == expected

def test_report_payout(sample_dict_data, capsys):
    report_payout(sample_dict_data)
    captured = capsys.readouterr()

    assert "IT" in captured.out
    assert "HR" in captured.out
    assert "John Doe" in captured.out
    assert "Jane Smith" in captured.out
    assert "Bob Johnson" in captured.out
    assert "$2000" in captured.out  # 40 * 50
    assert "$1575" in captured.out  # 35 * 45
    assert "$2475" in captured.out  # 45 * 55

def test_main_with_valid_file(sample_csv_file, capsys):
    from main import main
    main([sample_csv_file], "payout")
    captured = capsys.readouterr()

    assert "IT" in captured.out
    assert "HR" in captured.out
    assert "John Doe" in captured.out
    assert "Jane Smith" in captured.out
    assert "Bob Johnson" in captured.out

def test_main_with_nonexistent_file(capsys):
    from main import main
    main(["nonexistent.csv"], "payout")
    captured = capsys.readouterr()
    assert "не существует" in captured.out

def test_main_with_invalid_report_type(sample_csv_file, capsys):
    from main import main
    main([sample_csv_file], "invalid_report")
    captured = capsys.readouterr()
    assert "Не существует отчета" in captured.out

def test_main_with_empty_list_files(sample_csv_file, capsys):
    from main import main
    main([], "invalid_report")
    captured = capsys.readouterr()
    assert "Отсутствует список файлов" in captured.out