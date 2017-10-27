def print_iterarion(ttl):
    print_separator()
    print("Sending. Iteration: " + str(ttl))
    print_separator()


def print_separator():
    print("\n" + "-------------------------------------------------" + "\n")


def print_responses(responses):
    for responses_with_same_tll in responses:
        print_separator()
        for response in responses_with_same_tll['responses']:
            if response is None:
                print("No response")
            else:
                print(response.src)
        print("Average Time: ", responses_with_same_tll['average_time'])
        print_separator()
