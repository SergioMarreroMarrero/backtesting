//
// Created by oigre on 24/02/2025.
//

#ifndef DATABASE_H
#define DATABASE_H

#include <string>
#include <hdf5.h>


class Database {
public:
    explicit Database(const std::string& file_name);
    void close_file();
    double** get_data(const std::string& symbol, const std::string& exchange);
    hid_t h5_file;
};

int compare(const void* pa, const void* pb);
#endif //DATABASE_H
