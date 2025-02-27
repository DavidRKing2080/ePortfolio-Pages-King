//============================================================================
// Name        : HashTable.cpp
// Author      : David King
// Version     : 1.2 (Enhanced)
// Copyright   : Copyright © 2025 SNHU COCE
// Description : Enhanced Hash Table in C++, Ansi-style
//============================================================================

#include <algorithm>
#include <climits>
#include <iostream>
#include <string> // atoi
#include <vector>
#include <time.h>

#include "CSVparser.hpp"

using namespace std;

const unsigned int DEFAULT_SIZE = 179;
const double LOAD_FACTOR_THRESHOLD = 0.7;
const unsigned int PRIME_MULTIPLIER = 31;

// Forward declarations
double strToDouble(string str, char ch);

struct Bid {
    string bidId;
    string title;
    string fund;
    double amount;
    Bid() { amount = 0.0; }
};

class HashTable {
private:
    struct Node {
        Bid bid;
        unsigned int key;
        bool occupied;
        Node() : key(UINT_MAX), occupied(false) {}
        Node(Bid aBid, unsigned int aKey) : bid(aBid), key(aKey), occupied(true) {}
    };

    vector<Node> nodes;
    unsigned int tableSize;
    unsigned int itemCount;

    void resize();
    unsigned int hash(string key);
    unsigned int probe(unsigned int index);

public:
    HashTable();
    HashTable(unsigned int size);
    virtual ~HashTable();
    void Insert(Bid bid);
    void PrintAll();
    void Remove(string bidId);
    Bid Search(string bidId);
};

// Constructor initializes table with default size
HashTable::HashTable() : tableSize(DEFAULT_SIZE), itemCount(0) { nodes.resize(tableSize); }

// Constructor allows specifying table size
HashTable::HashTable(unsigned int size) : tableSize(size), itemCount(0) { nodes.resize(tableSize); }

// Destructor clears hash table
HashTable::~HashTable() { nodes.clear(); }

// ENHANCEMENT: Resizes the hash table when load factor exceeds threshold
void HashTable::resize() {
    unsigned int newSize = tableSize * 2;
    vector<Node> newNodes(newSize);
    for (auto& node : nodes) {
        if (node.occupied) {
            unsigned int newIndex = hash(node.bid.bidId) % newSize;
            while (newNodes[newIndex].occupied) {
                newIndex = (newIndex + 1) % newSize;
            }
            newNodes[newIndex] = node;
        }
    }
    nodes = move(newNodes);
    tableSize = newSize;
}

// ENHANCEMENT: Hash function using prime multiplication for better distribution
unsigned int HashTable::hash(string key) {
    unsigned int hashValue = 0;
    for (char ch : key) {
        hashValue = (hashValue * PRIME_MULTIPLIER + ch) % tableSize;
    }
    return hashValue;
}

// ENHANCEMENT: Probing function for open addressing (linear probing)
unsigned int HashTable::probe(unsigned int index) {
    while (nodes[index].occupied) {
        index = (index + 1) % tableSize;
    }
    return index;
}

// ENHANCEMENT: Inserts a bid into the hash table, dynamically resizing if necessary
void HashTable::Insert(Bid bid) {
    if (itemCount / (double)tableSize >= LOAD_FACTOR_THRESHOLD) {
        resize();
    }
    unsigned int index = hash(bid.bidId);
    index = probe(index);
    nodes[index] = Node(bid, index);
    itemCount++;
}

// Prints all stored bids
void HashTable::PrintAll() {
    for (const auto& node : nodes) {
        if (node.occupied) {
            cout << node.bid.bidId << " | " << node.bid.amount << " | " << node.bid.fund << endl;
        }
    }
}

// Removes a bid from the hash table
void HashTable::Remove(string bidId) {
    unsigned int index = hash(bidId);
    while (nodes[index].occupied) {
        if (nodes[index].bid.bidId == bidId) {
            nodes[index].occupied = false;
            itemCount--;
            return;
        }
        index = (index + 1) % tableSize;
    }
}

// Searches for a bid by its ID and returns it if found
Bid HashTable::Search(string bidId) {
    unsigned int index = hash(bidId);
    while (nodes[index].occupied) {
        if (nodes[index].bid.bidId == bidId) {
            return nodes[index].bid;
        }
        index = (index + 1) % tableSize;
    }
    return Bid();
}
