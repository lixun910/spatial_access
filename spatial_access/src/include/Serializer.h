// Logan Noel (github.com/lmnoel)
//
// ©2017-2019, Center for Spatial Data Science

#pragma once

#include <string>
#include <fstream>
#include <vector>
#include <istream>

class Serializer {
public:
    Serializer(const std::string &filename);
    ~Serializer();

    template <class T> void writeNumericType(T value)
    {
        output.write ( reinterpret_cast<char *>(&value),sizeof(T));
        checkStreamIsGood();
    }
    template <class T> void writeVector(const std::vector<T>& value)
    {
        unsigned long int vec_size = value.size();
        writeNumericType<unsigned long int>(vec_size);
        output.write((char *) &value[0], vec_size * sizeof(T));
        checkStreamIsGood();
    }
    template <class T> void write2DVector(const std::vector<std::vector<T>>& value)
    {
        unsigned long int vec_size = value.size();
        writeNumericType<unsigned long int>(vec_size);
        for (const auto &element : value) {
            writeVector<T>(element);
        }
        checkStreamIsGood();
    }
    void writeBool(bool value);
private:
    std::ofstream output;
    void checkStreamIsGood();
};

class Deserializer {
public:
    Deserializer(const std::string &filename);
    ~Deserializer();

    template <class T> T readNumericType()
    {
        T value;
        input.read( reinterpret_cast<char *>(&value), sizeof(T));
        checkStreamIsGood();
        return value;
    }
    template <class T> void readVector(std::vector<T>& value)
    {
        auto vec_size = readNumericType<unsigned long>();

        value.assign(vec_size, 0);
        input.read(reinterpret_cast<char *>(&value[0]), vec_size*sizeof(T));
        checkStreamIsGood();
    }
    template <class T> void read2DVector(std::vector<std::vector<T>>& value)
    {
        auto vec_size = readNumericType<unsigned long>();
        for (unsigned long int i = 0; i < vec_size; i++)
        {

            std::vector<T> element;
            readVector<T>(element);
            value.push_back(element);
        }
        checkStreamIsGood();
    }

    bool readBool();
private:
    std::ifstream input;
    void checkStreamIsGood();
};
