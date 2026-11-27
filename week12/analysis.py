from pathlib import Path
import pandas as pd


#################################################
#################################################
def 정제(df):
	정제된_df = df.copy()

	# 점수가 비어 있는 행을 삭제한다.
	정제된_df = 정제된_df.dropna(subset=["점수"])
	print(f"점수 결측 행 삭제 후: {len(정제된_df)}행")

	# 모든 열의 값이 완전히 같은 중복 행을 삭제한다.
	정제된_df = 정제된_df.drop_duplicates()
	print(f"중복 행 삭제 후: {len(정제된_df)}행")

	# 반과 과목 값의 앞뒤 공백을 제거한다.
	정제된_df["반"] = 정제된_df["반"].str.strip()
	정제된_df["과목"] = 정제된_df["과목"].str.strip()
	print(f"공백 제거 후: {len(정제된_df)}행")

	# 점수가 0~100 범위를 벗어난 행을 삭제한다.
	정제된_df = 정제된_df[정제된_df["점수"].between(0, 100)].copy()
	정제된_df["점수"] = 정제된_df["점수"].astype(int)
	print(f"점수 범위 정제 후: {len(정제된_df)}행")

	return 정제된_df

import pandas as pd
df = pd.read_csv(Path(__file__).parent / "scores_2026.csv")
df = 정제(df)
print(sorted(df["반"].unique())) # ['1반', '2반']       ← 세 개에서 두 개로
print(sorted(df["과목"].unique())) # ['수학','영어','프로그래밍'] ← 네 개에서 세 개로



csv_path = Path(__file__).parent / "scores_2026.csv"
df = pd.read_csv(csv_path)
print(df.shape)                      # (114, 5)
print(df["점수"].isna().sum())       # 6      ← 빈 칸이 몇 개인가
print(df.duplicated().sum())         # 4      ← 완전히 같은 행이 몇 개인가
print(df["반"].unique())             # ['2반' '1반' '1반 ']      ← 세 개?
print(df["과목"].unique())           # ['수학' '프로그래밍' '영어' '프로그래밍 ']
print(df["점수"].describe())         # max 999.0  min -5.0   ← 점수인데?

# 정제된 데이터에서 수학 과목 행만 남긴다.
정제된_df = 정제(df)
수학_df = 정제된_df[정제된_df["과목"] == "수학"]
print(f"수학 과목 행 수: {len(수학_df)}행")

# 반별 점수 평균을 계산한다.
반별_평균 = 정제된_df.groupby("반")["점수"].mean()
print(반별_평균)

# 과목과 반별 점수 평균을 계산한다.
과목_반별_평균 = 정제된_df.groupby(["과목", "반"])["점수"].mean()
print(과목_반별_평균)

# 반별 점수 개수, 평균, 중앙값, 최댓값을 표로 출력한다.
반별_통계 = 정제된_df.groupby("반").agg(
	개수=("점수", "count"),
	평균=("점수", "mean"),
	중앙값=("점수", "median"),
	최댓값=("점수", "max"),
).round(2)
print(반별_통계)



