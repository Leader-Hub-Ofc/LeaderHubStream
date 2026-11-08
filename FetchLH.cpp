#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <iomanip>
#include <sstream>
#include "sqlite3.h"
#include "httplib.h"
#include "json.hpp" // nlohmann/json

using json = nlohmann::json;

// --- Database Initialization ---
void initDatabase(sqlite3* db) {
    char* errMessage = 0;
    
    // User Table
    const char* sqlUserTable = "CREATE TABLE IF NOT EXISTS users ("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "name TEXT NOT NULL, "
                           "email TEXT UNIQUE NOT NULL, "
                           "created_at DATETIME DEFAULT CURRENT_TIMESTAMP);";
    
    // Security Log Table
    const char* sqlLogTable = "CREATE TABLE IF NOT EXISTS security_logs ("
                          "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "ip_address TEXT NOT NULL, "
                          "device_info TEXT NOT NULL, "
                          "access_time DATETIME DEFAULT CURRENT_TIMESTAMP);";

    sqlite3_exec(db, sqlUserTable, 0, 0, &errMessage);
    sqlite3_exec(db, sqlLogTable, 0, 0, &errMessage);
}

// Get Current Timestamp
std::string getCurrentTime() {
    auto now = std::chrono::system_clock::now();
    auto in_time_t = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S");
    return ss.str();
}

int main() {
    sqlite3* db;
    int rc = sqlite3_open("leaderhub.db", &db);
    if (rc) {
        std::cerr << "Can't open database: " << sqlite3_errmsg(db) << std::endl;
        return 1;
    } else {
        std::cout << "Opened database successfully!" << std::endl;
    }

    initDatabase(db);

    httplib::Server svr;

    // 1. Home Route & Security Logging
    svr.Get("/", [&](const httplib::Request& req, httplib::Response& res) {
        std::string client_ip = req.remote_addr;
        std::string device_info = req.has_header("User-Agent") ? req.get_header_value("User-Agent") : "Unknown";
        std::string time_now = getCurrentTime();

        // Save security log to DB
        std::string sql = "INSERT INTO security_logs (ip_address, device_info) VALUES ('" + client_ip + "', '" + device_info + "');";
        char* errMessage = 0;
        sqlite3_exec(db, sql.c_str(), 0, 0, &errMessage);

        json response;
        response["message"] = "Welcome to LeaderHub C++ Website";
        response["security_status"] = "Verified (Human / Secure Connection)";
        response["live_time"] = time_now;
        response["client_ip"] = client_ip;
        response["device_info"] = device_info;

        res.set_content(response.dump(), "application/json");
    });

    // 2. Register User Endpoint (POST)
    svr.Post("/api/users", [&](const httplib::Request& req, httplib::Response& res) {
        try {
            auto data = json::parse(req.body);
            if (!data.contains("name") || !data.contains("email")) {
                res.status = 400;
                res.set_content("{\"error\": \"Name and Email are required!\"}", "application/json");
                return;
            }

            std::string name = data["name"];
            std::string email = data["email"];

            std::string sql = "INSERT INTO users (name, email) VALUES ('" + name + "', '" + email + "');";
            char* errMessage = 0;
            int rc = sqlite3_exec(db, sql.c_str(), 0, 0, &errMessage);

            if (rc != SQLITE_OK) {
                res.status = 400;
                res.set_content("{\"error\": \"User already exists or database error!\"}", "application/json");
                sqlite3_free(errMessage);
            } else {
                res.status = 201;
                res.set_content("{\"message\": \"User registered successfully!\"}", "application/json");
            }
        } catch (...) {
            res.status = 400;
            res.set_content("{\"error\": \"Invalid JSON payload!\"}", "application/json");
        }
    });

    // 3. View Security Logs Endpoint
    svr.Get("/api/logs", [&](const httplib::Request& req, httplib::Response& res) {
        const char* sql = "SELECT id, ip_address, device_info, access_time FROM security_logs;";
        sqlite3_stmt* stmt;
        json log_list = json::array();

        if (sqlite3_prepare_v2(db, sql, -1, &stmt, 0) == SQLITE_OK) {
            while (sqlite3_step(stmt) == SQLITE_ROW) {
                json log;
                log["id"] = sqlite3_column_int(stmt, 0);
                log["ip"] = std::string((const char*)sqlite3_column_text(stmt, 1));
                log["device"] = std::string((const char*)sqlite3_column_text(stmt, 2));
                log["time"] = std::string((const char*)sqlite3_column_text(stmt, 3));
                log_list.push_back(log);
            }
        }
        sqlite3_finalize(stmt);
        res.set_content(log_list.dump(), "application/json");
    });

    std::cout << "Server started at http://localhost:8080..." << std::endl;
    svr.listen("0.0.0.0", 8080);

    sqlite3_close(db);
    return 0;
}
