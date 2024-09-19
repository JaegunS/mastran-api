from mastran import verify_credentials, get_headers, get_results, fuzzy_match

def main():
    """Shows basic usage of the MASTRAN API.
    """
    service = verify_credentials()
    print("Getting the headers for the Fluids Parameters1 table")
    headers = get_headers("Fluids Parameters1", service)
    print(headers)

    print("\nGetting the results for the Thrust parameter from Engine Parameters table")
    result = get_results("Thrust", "Engine Parameters", service)
    print(result)

    print("\nFuzzy matching for 'Thrust'")
    fuzzy = fuzzy_match("Thrust", service)
    print(fuzzy)

    print("\nGetting the results for the fuzzy match")
    fuzzy_result = get_results(fuzzy[0]["value"], fuzzy[0]["table"], service)
    print(fuzzy_result)


if __name__ == "__main__":
    main()

