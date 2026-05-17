import pandas as pd



def main():
    df = pd.read_csv("logs/signals.csv")

    print(f"Total setups: {len(df)}")

    print("\nSetup types:")
    print(df["setup_type"].value_counts().to_string())

    print(f"\nAverage score: {df['score'].mean():.2f}")

    print(f"Average RSI: {df['rsi'].mean():.2f}")

    print("\nScore distribution:")
    print(df["score"].value_counts().to_string())


if __name__ == "__main__":
    main()