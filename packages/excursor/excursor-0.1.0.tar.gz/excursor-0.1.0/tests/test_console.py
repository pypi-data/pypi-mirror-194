from excursor.console import run


def test_run(capsys):
    run()
    captured = capsys.readouterr()
    assert captured.out == "running...\n"
