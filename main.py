from src.database.schema import create_all_tables

from src.database.loader import load_dataframe

from src.etl.loader import (
    validate_files_exist,
    load_all_files
)

from src.etl.audit import save_audit

from src.validators.validator import (
    validate_table,
    save_validation_report
)


def main():

    print("\n" + "=" * 50)
    print("NIFTY 100 FINANCIAL INTELLIGENCE PLATFORM")
    print("=" * 50)

    print("\nChecking files...\n")

    missing_files = validate_files_exist()

    if missing_files:

        print("Missing files detected:\n")

        for file in missing_files:
            print(f"❌ {file}")

        print("\nPlease add missing files and try again.")
        return

    print("✅ All files found.\n")

    print("=" * 50)
    print("CREATING DATABASE SCHEMA")
    print("=" * 50)

    create_all_tables()

    print("\nDatabase schema created successfully.\n")

    print("=" * 50)
    print("LOADING DATASETS")
    print("=" * 50)

    data = load_all_files()

    print("\nLoading data into SQLite...\n")

    for table_name, df in data.items():

        load_dataframe(
            df,
            table_name
        )

    print("\nLoaded Datasets:\n")

    for name, df in data.items():

        print(
            f"✅ {name:<20} Rows: {df.shape[0]:<6} Columns: {df.shape[1]}"
        )

    print("\n" + "=" * 50)
    print("RUNNING VALIDATIONS")
    print("=" * 50)

    for table_name, df in data.items():

        print(f"Validating {table_name}...")

        validate_table(
            df,
            table_name
        )

    save_validation_report()

    print("✅ Validation completed")

    print("\n" + "=" * 50)
    print("GENERATING AUDIT REPORT")
    print("=" * 50)

    save_audit()

    print("✅ load_audit.csv generated")
    print("✅ validation_failures.csv generated")

    print("\n" + "=" * 50)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 50)

    print("\nGenerated Files:")

    print("📄 nifty100.db")
    print("📄 load_audit.csv")
    print("📄 validation_failures.csv")

    print("\nProject Ready For:")
    print("➡ Day 05 - Full Data Load Validation")
    print("➡ Foreign Key Validation")
    print("➡ Row Count Verification")


if __name__ == "__main__":
    main()