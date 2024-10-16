#include <pybind11/pybind11.h>
#include <unordered_map>
#include <chrono>
#include <string>
#include <fstream>
#include <json/json.h>
#include <iostream>

namespace py = pybind11;

class InMemoryDB {
    std::unordered_map<std::string, std::string> data;
    std::unordered_map<std::string, std::chrono::time_point<std::chrono::steady_clock>> ttl;

public:
    void set(const std::string &key, const std::string &value, int expire_in_seconds) {
        data[key] = value;
        if (expire_in_seconds > 0) {
            auto expire_time = std::chrono::steady_clock::now() + std::chrono::seconds(expire_in_seconds);
            ttl[key] = expire_time;
        }
    }

    std::string get(const std::string &key) {
        auto it = ttl.find(key);
        if (it != ttl.end() && std::chrono::steady_clock::now() > it->second) {
            data.erase(key);
            ttl.erase(key);
            return "";
        }
        return data.count(key) ? data[key] : "";
    }

    bool del(const std::string &key) {
        if (data.count(key)) {
            data.erase(key);
            ttl.erase(key);
            return true;
        }
        return false;
    }

    // Save the state of the databse to a JSON file (snapshot)
    void save_snapshot(const std::string& filename) {
        std::ofstream file(filename);
        Json::Value root;

        // Save key-value pairs
        for (const auto& entry : data) {
            root["data"][entry.first] = entry.second;
        }

        // Save TTL (absolute expiration timestamps)
        for (const auto& entry : ttl) {
            auto expire_time = std::chrono::duration_cast<std::chrono::seconds>(
                entry.second.time_since_epoch()).count();
            root["ttl"][entry.first] = expire_time;
        }

        file << root;
        file.close();
        std::cout << "Snapshot saved to " << filename << std::endl;
    }


    // Restore the state of the database from a JSON file (snapshot)
    void load_snapshot(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Could not open snapshot file." << std::endl;
            return;
        }

        Json::Value root;
        file >> root;

        // Clear current data and TTLs
        data.clear();
        ttl.clear();

        // Load key-value pairs
        for (const auto& key : root["data"].getMemberNames()) {
            data[key] = root["data"][key].asString();
        }

        // Load TTLs and check expiration
        for (const auto& key : root["ttl"].getMemberNames()) {
            auto expire_time = std::chrono::time_point<std::chrono::steady_clock>(
                std::chrono::seconds(root["ttl"][key].asInt()));
            if (std::chrono::steady_clock::now() < expire_time) {
                ttl[key] = expire_time;
            } else {
                data.erase(key);  // Remove expired keys
            }
        }

        file.close();
        std::cout << "Snapshot loaded from " << filename << std::endl;
    }
};

PYBIND11_MODULE(database, m) {
    py::class_<InMemoryDB>(m, "InMemoryDB")
        .def(py::init<>())
        .def("set", &InMemoryDB::set)
        .def("get", &InMemoryDB::get)
        .def("delete", &InMemoryDB::del)
        .def("save_snapshot", &InMemoryDB::save_snapshot)
        .def("load_snapshot", &InMemoryDB::load_snapshot);
}
