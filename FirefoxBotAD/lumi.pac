// AdCrush Proxy Auto-Config
//

//
// Define the network paths (direct, proxy and deny)
//

// Default connection
var direct = "DIRECT";

// Alternate Proxy Server
var proxy = "PROXY 192.168.1.116:24001";

// Default localhost for denied connections
var deny = "PROXY 127.0.0.1:65535";

//
// Proxy Logic
//

function FindProxyForURL(url, host) {
    // Default PROXY
    return proxy;
}