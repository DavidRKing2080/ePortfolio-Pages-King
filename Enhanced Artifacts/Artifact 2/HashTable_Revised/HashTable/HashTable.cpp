#include <iostream>
#include <vector>
#include <string>

#include "CSVparser.hpp"

using namespace std;

const unsigned int DEFAULT_SIZE = 179;
const int PRIME_MULTIPLIER = 31; // Used for improved hash function

// Define a structure to hold bid information
struct Bid {
    string bidId;
    string title;
    string fund;
    double amount;
    Bid() : amount(0.0) {}
};

class HashTable {
private:
    struct Node {
        Bid bid;
        unsigned int key;
        Node* next;
        Node() : key(UINT_MAX), next(nullptr) {}
        Node(Bid aBid, unsigned int aKey) : bid(aBid), key(aKey), next(nullptr) {}
    };

    vector<Node*> table;
    unsigned int tableSize;

    // ENHANCEMENT: Multiplicative Hash Function for better distribution
    // This function takes a string key and converts it into a hash value
    // using a prime number multiplier to reduce collisions.
    unsigned int hash(string key) {
        unsigned int hashValue = 0;
        for (char ch : key) {
            hashValue = (hashValue * PRIME_MULTIPLIER + ch) % tableSize;
        }
        return hashValue;
    }

    // ENHANCEMENT: Resizing function to dynamically grow the hash table
    // When the table becomes too full, this function doubles its size
    // and rehashes all existing entries to new positions.
    void resize() {
        unsigned int newTableSize = tableSize * 2;
        vector<Node*> newTable(newTableSize, nullptr);

        for (unsigned int i = 0; i < tableSize; ++i) {
            Node* node = table[i];
            while (node) {
                unsigned int newIndex = hash(node->bid.bidId) % newTableSize;
                Node* newNode = new Node(node->bid, newIndex);
                newNode->next = newTable[newIndex];
                newTable[newIndex] = newNode;
                node = node->next;
            }
        }
        table = move(newTable);
        tableSize = newTableSize;
    }

public:
    // Constructor initializes the hash table with a given size.
    HashTable(unsigned int size = DEFAULT_SIZE) : tableSize(size) {
        table.resize(size, nullptr);
    }

    // Destructor releases dynamically allocated memory for each node.
    ~HashTable() {
        for (auto node : table) {
            while (node) {
                Node* temp = node;
                node = node->next;
                delete temp;
            }
        }
    }

    // ENHANCEMENT: Open Addressing with Linear Probing
    // This function inserts a bid into the hash table using linear probing
    // to resolve collisions instead of chaining.
    void insert_with_open_addressing(Bid bid) {
        unsigned int index = hash(bid.bidId) % tableSize;
        while (table[index] != nullptr) {
            index = (index + 1) % tableSize; // Linear probing
        }
        table[index] = new Node(bid, index);
    }

    // Prints all stored bids in the hash table.
    void printAll() {
        for (unsigned int i = 0; i < tableSize; ++i) {
            if (table[i]) {
                cout << table[i]->bid.bidId << " | " << table[i]->bid.title << " | "
                    << table[i]->bid.amount << " | " << table[i]->bid.fund << endl;
            }
        }
    }
};

int main() {
    // Create a hash table instance
    HashTable hashTable;

    // Create bid entries and insert them into the hash table
    Bid bid1 = { "1001", "Laptop", "IT Fund", 1200.50 };
    Bid bid2 = { "1002", "Printer", "Office Fund", 350.00 };

    hashTable.insert_with_open_addressing(bid1);
    hashTable.insert_with_open_addressing(bid2);

    // Print all stored bids in the table
    cout << "All Bids in Hash Table:" << endl;
    hashTable.printAll();

    return 0;
}
