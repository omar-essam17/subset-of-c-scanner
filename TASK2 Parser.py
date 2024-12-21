def IsSimpleGrammar(grammar):
    for _, rules in grammar.items():
        seen_terminals = set()
        for rule in rules:
            if not rule:
                return False
            if rule[0].islower():
                if rule[0] in seen_terminals:
                    return False
                seen_terminals.add(rule[0])
            else:
                return False
    return True


def ParsingInput(grammar, sequence, starting_symbol):
    stack = [starting_symbol]
    idx = 0

    while stack:
        current = stack.pop()

        if idx >= len(sequence):
            break

        if current.islower():
            if current == sequence[idx]:
                idx += 1
            else:
                return False, stack, sequence[idx:]
        elif current.isupper():
            matched = False
            for rule in grammar.get(current, []):
                if rule[0] == sequence[idx]:
                    stack.extend(reversed(rule))
                    matched = True
                    break
            if not matched:
                return False, stack, sequence[idx:]
        else:
            return False, stack, sequence[idx:]

    return idx == len(sequence) and not stack, stack, sequence[idx:]


def main():
    while True:
        print("\n                  Grammars ")
        grammar = {}
        non_terminals = input("Enter the non-terminals EX >> S,A: ").split(',')

        for nt in non_terminals:
            grammar[nt] = []
            for i in range(2):
                rule = input(f"Enter rule number {i+1} for non-terminal '{nt}': ").strip()
                grammar[nt].append(rule)

        if not IsSimpleGrammar(grammar):
            print("\nThe grammar isn't simple.\nTry again")
            continue

        print("\nThe grammar is Simple.\n")

        starting_symbol = non_terminals[0]
        sequence = list(input("Enter the string to be checked: "))
        is_accepted, stack, remaining = ParsingInput(grammar, sequence, starting_symbol)

        print("\nThe input String:", sequence)
        print("Stack after checking:", stack)
        print("The rest of unchecked string:", remaining)
        if is_accepted:
            print("Accepted.")
        else:
            print("Rejected.")
        print("=" * 30)

        while True:
            print("1-Another Grammar.\n2-Another String.\n3-Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                break
            elif choice == "2":
                sequence = list(input("Enter the string to be checked: "))
                is_accepted, stack, remaining = ParsingInput(grammar, sequence, starting_symbol)

                print("\nThe input String:", sequence)
                print("Stack after checking:", stack)
                print("The rest of unchecked string:", remaining)
                if is_accepted:
                    print("Your input String is Accepted.")
                else:
                    print("Your input String is Rejected.")
                print("=" * 50)
            elif choice == "3":
                print("Exiting")
                return
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
