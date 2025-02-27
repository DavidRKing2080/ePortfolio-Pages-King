#include <iostream>
#include <limits>
#include <stdexcept>

// ENHANCEMENT: Created helper function to check for numeric overflow, replacing redundant logic in add_numbers.
template <typename T>
bool check_overflow(T value, T increment) {
    return (value > std::numeric_limits<T>::max() - increment);
}

// ENHANCEMENT: Created helper function to check for numeric underflow, replacing redundant logic in subtract_numbers.
template <typename T>
bool check_underflow(T value, T decrement) {
    return (value < std::numeric_limits<T>::min() + decrement);
}

// Function to add numbers with overflow detection
// Takes a starting number, an increment value, and a number of steps to apply the increment
// ENHANCEMENT: Now uses check_overflow to prevent silent failures and throws an exception on overflow.
template <typename T>
T add_numbers(T const& start, T const& increment, unsigned long int const& steps) {
    T result = start;
    for (unsigned long int i = 0; i < steps; ++i) {
        if (check_overflow(result, increment)) {
            throw std::overflow_error("Overflow detected during addition");
        }
        result += increment;
    }
    return result;
}

// Function to subtract numbers with underflow detection
// Takes a starting number, a decrement value, and a number of steps to apply the decrement
// ENHANCEMENT: Now uses check_underflow to prevent silent failures and throws an exception on underflow.
template <typename T>
T subtract_numbers(T const& start, T const& decrement, unsigned long int const& steps) {
    T result = start;
    for (unsigned long int i = 0; i < steps; ++i) {
        if (check_underflow(result, decrement)) {
            throw std::underflow_error("Underflow detected during subtraction");
        }
        result -= decrement;
    }
    return result;
}

// Function to test overflow scenarios
// ENHANCEMENT: Now catches exceptions thrown by add_numbers and prints user-friendly error messages
template <typename T>
void test_overflow() {
    const unsigned long int steps = 5;
    const T increment = std::numeric_limits<T>::max() / steps;
    const T start = 0;

    std::cout << "Overflow Test for type: " << typeid(T).name() << std::endl;

    try {
        std::cout << "\tAdding numbers without overflow: " << add_numbers<T>(start, increment, steps) << std::endl;
        std::cout << "\tAdding numbers with overflow: " << add_numbers<T>(start, increment, steps + 1) << std::endl;
    }
    catch (const std::overflow_error& e) {
        std::cout << "\t" << e.what() << std::endl;
    }
}

// Function to test underflow scenarios
// ENHANCEMENT: Now catches exceptions thrown by subtract_numbers and prints user-friendly error messages
template <typename T>
void test_underflow() {
    const unsigned long int steps = 5;
    const T decrement = std::numeric_limits<T>::max() / steps;
    const T start = std::numeric_limits<T>::max();

    std::cout << "Underflow Test for type: " << typeid(T).name() << std::endl;

    try {
        std::cout << "\tSubtracting numbers without underflow: " << subtract_numbers<T>(start, decrement, steps) << std::endl;
        std::cout << "\tSubtracting numbers with underflow: " << subtract_numbers<T>(start, decrement, steps + 1) << std::endl;
    }
    catch (const std::underflow_error& e) {
        std::cout << "\t" << e.what() << std::endl;
    }
}

int main() {
    std::cout << "Starting Overflow and Underflow Tests" << std::endl;

    // ENHANCEMENT: Expanded test coverage to multiple data types, improving robustness.
    test_overflow<char>();
    test_overflow<wchar_t>();
    test_overflow<short int>();
    test_overflow<int>();
    test_overflow<long>();
    test_overflow<long long>();
    test_overflow<unsigned char>();
    test_overflow<unsigned short int>();
    test_overflow<unsigned int>();
    test_overflow<unsigned long>();
    test_overflow<unsigned long long>();
    test_overflow<float>();
    test_overflow<double>();
    test_overflow<long double>();

    test_underflow<char>();
    test_underflow<wchar_t>();
    test_underflow<short int>();
    test_underflow<int>();
    test_underflow<long>();
    test_underflow<long long>();
    test_underflow<unsigned char>();
    test_underflow<unsigned short int>();
    test_underflow<unsigned int>();
    test_underflow<unsigned long>();
    test_underflow<unsigned long long>();
    test_underflow<float>();
    test_underflow<double>();
    test_underflow<long double>();

    // ENHANCEMENT: Added edge case testing to ensure function stability at boundary values.
    std::cout << "\nTesting Edge Cases" << std::endl;
    try {
        std::cout << "\tAdding numbers at max limit: " << add_numbers<int>(std::numeric_limits<int>::max(), 1, 1) << std::endl;
    }
    catch (const std::overflow_error& e) {
        std::cout << "\t" << e.what() << std::endl;
    }
    try {
        std::cout << "\tSubtracting numbers at min limit: " << subtract_numbers<int>(std::numeric_limits<int>::min(), 1, 1) << std::endl;
    }
    catch (const std::underflow_error& e) {
        std::cout << "\t" << e.what() << std::endl;
    }

    std::cout << "All tests complete" << std::endl;
    return 0;
}
