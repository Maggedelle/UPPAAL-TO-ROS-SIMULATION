
#include "HTTPRequest.hpp"
#include <iostream>

#ifdef __cplusplus
extern "C"
{      // tells C++ compiler to use C symbol name mangling (C compiler ignores)
#endif // __cplusplus
    double get_position_x();
    void shutdown_drone();
    void move_drone_along_x_axis();
#ifdef __cplusplus
} // end of "C" symbol name mangling
#endif // __cplusplus

double get_position_x()
{
    try
    {
        // you can pass http::InternetProtocol::V6 to Request to make an IPv6 request
        http::Request request{"http://127.0.0.1:5000/get_position_x"};

        // send a get request
        const auto response = request.send("GET");
        auto output = std::stod(std::string{response.body.begin(), response.body.end()});
        return output;
    }
    catch (const std::exception &e)
    {
        std::cerr << "Request failed, error: " << e.what() << '\n';
    }
    return 0;
}


void move_drone_along_x_axis() 
{
    try
    {
        // you can pass http::InternetProtocol::V6 to Request to make an IPv6 request
        http::Request request{"http://127.0.0.1:5000/move_drone_along_x_axis"};

        // send a get request
        const auto response = request.send("GET");
        auto output = std::stod(std::string{response.body.begin(), response.body.end()});
    }
    catch (const std::exception &e)
    {
        std::cerr << "Request failed, error: " << e.what() << '\n';
    }
}


void shutdown_drone()
{
    try
    {
        // you can pass http::InternetProtocol::V6 to Request to make an IPv6 request
        http::Request request{"http://127.0.0.1:5000/shutdown_drone"};

        // send a get request
        const auto response = request.send("GET");
    }
    catch (const std::exception &e)
    {
        std::cerr << "Request failed, error: " << e.what() << '\n';
    }
}
