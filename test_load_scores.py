from load_scores import load_scores
def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5

def test_빈_줄은_건너뛴다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5

def test_이름에_쉼표가_있어도_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5

import pytest
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError): # 예상한 에러가 일어나면 테스트 통과함.
        load_scores("없는파일.csv")

def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []

def test_이름이_비어_있으면_건너뛴다(tmp_path):
    path = tmp_path / "blank_name.csv"
    path.write_text("name,score\n,80\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [(2, ",80", "이름이 비어 있음")]

def test_명령줄_실행에서_기본_파일을_읽고_결과를_출력한다(tmp_path, monkeypatch, capsys):
    import runpy
    import sys

    (tmp_path / "scores.csv").write_text(
        "name,score\n학생,90\n잘못된점수,abc\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["load_scores.py"])

    runpy.run_module("load_scores", run_name="__main__")

    output = capsys.readouterr().out
    assert "읽은 줄 : 1개" in output
    assert "학생 90" in output
    assert "건너뛴 줄 : 1개" in output
    assert "잘못된점수,abc" in output

@pytest.mark.parametrize("점수, 유효한가", [
    (-1,  False),   # 경계 바로 아래
    (0,   True),    # ★ 아래쪽 경계
    (1,   True),
    (99,  True),
    (100, True),    # ★ 위쪽 경계
    (101, False),   # 경계 바로 위
])
def test_점수_경계값(점수, 유효한가):
    with open("임시.csv", "w", encoding="utf-8") as f:
        f.write(f"name,score\n학생,{점수}\n")
    kept, skipped = load_scores("임시.csv")
    assert (len(kept) == 1) == 유효한가

