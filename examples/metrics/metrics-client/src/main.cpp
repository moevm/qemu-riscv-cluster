#include <prometheus/gauge.h>
#include <prometheus/registry.h>
#include <prometheus/gateway.h>

#include <thread>
#include <chrono>
#include <iostream>

class MetricsCollector {
    prometheus::Gateway gateway;
    std::shared_ptr<prometheus::Registry> registry;

    prometheus::Gauge *memory_used_gauge;
    prometheus::Gauge *cpu_usage_gauge;
    prometheus::Gauge *request_count_gauge;
    bool is_running;
    std::thread thread;

    struct {
        uint64_t last_total_user;
        uint64_t last_total_user_low;
        uint64_t last_total_sys;
        uint64_t last_total_idle;
    } cpu;

    double getMemoryUsed();
    double getCPUUsage();
    void mainLoop();

public:
    MetricsCollector(const char *gateway_address, const char *gateway_port, const char *worker_name);
    ~MetricsCollector();
    void pushMetrics();

    void incrementRequestCount()
    {
        request_count_gauge->Increment(1);
    }
};

MetricsCollector::MetricsCollector(const char *gateway_address, const char *gateway_port, const char *worker_name)
    : gateway(gateway_address, gateway_port, worker_name),
      registry(std::make_shared<prometheus::Registry>())
{
    FILE *file = fopen("/proc/stat", "r");
    fscanf(file, "cpu %lu %lu %lu %lu",
        &cpu.last_total_user, &cpu.last_total_user_low,
        &cpu.last_total_sys, &cpu.last_total_idle
    );
    fclose(file);

    auto &cpu_usage_family = prometheus::BuildGauge()
        .Name("cpu_usage")
        .Help("CPU Usage in percents")
        .Register(*registry);
    
    auto &memory_used_family = prometheus::BuildGauge()
        .Name("memory_used")
        .Help("Memory used in gigabytes")
        .Register(*registry);
    
    auto &request_count_family = prometheus::BuildGauge()
        .Name("request_count")
        .Help("Count of requests (example)")
        .Register(*registry);

    memory_used_gauge = &memory_used_family.Add({});
    cpu_usage_gauge = &cpu_usage_family.Add({});
    request_count_gauge = &request_count_family.Add({});

    gateway.RegisterCollectable(registry);

    is_running = true;
    thread = std::thread(&MetricsCollector::mainLoop, this);
}

void MetricsCollector::mainLoop()
{
    while (is_running) {
        std::cout << "MAIN LOOP" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(5));
        
        memory_used_gauge->Set(getMemoryUsed());
        cpu_usage_gauge->Set(getCPUUsage());
        
        gateway.PushAdd();
    }
}

MetricsCollector::~MetricsCollector()
{
    is_running = false;
    thread.join();
}

double MetricsCollector::getMemoryUsed()
{
    uint64_t mem_total = 0, mem_free = 0, buffers = 0, cached = 0;
    FILE *fp = fopen("/proc/meminfo", "r");
    
    static char line[256];
    while (fgets(line, sizeof(line), fp)) {
        if (sscanf(line, "MemTotal: %lu", &mem_total) == 1) continue;
        if (sscanf(line, "MemFree: %lu", &mem_free) == 1) continue;
        if (sscanf(line, "Buffers: %lu", &buffers) == 1) continue;
        if (sscanf(line, "Cached: %lu", &cached) == 1) continue;
    }

    fclose(fp);
    return (double)(mem_total - mem_free - buffers - cached) / (1024.0 * 1024.0);
}

double MetricsCollector::getCPUUsage()
{
    uint64_t total_user, total_user_low, total_sys, total_idle, total;
    double percent;
    
    FILE *file = fopen("/proc/stat", "r");
    fscanf(file, "cpu %lu %lu %lu %lu",
        &total_user, &total_user_low, &total_sys, &total_idle
    );
    fclose(file);

    if (total_user < cpu.last_total_user || total_user_low < cpu.last_total_user_low ||
        total_sys < cpu.last_total_sys || total_idle < cpu.last_total_idle) {
        // overflow detection
        percent = -1.0;
    }
    else {
        total = (total_user - cpu.last_total_user) + (total_user_low - cpu.last_total_user_low) +
            (total_sys - cpu.last_total_sys);
        
        percent = total;
        total += (total_idle - cpu.last_total_idle);
        percent /= total;
        percent *= 100;
    }

    cpu.last_total_user = total_user;
    cpu.last_total_user_low = total_user_low;
    cpu.last_total_sys = total_sys;
    cpu.last_total_idle = total_idle;

    return percent;
}

int main()
{
    // usage example
    MetricsCollector metrics_collector(
        getenv("PROMETHEUS_GATEWAY_ADDRESS"),
        getenv("PROMETHEUS_GATEWAY_PORT"),
        getenv("WORKER_NAME")
    );

    srand(time(NULL));
    while (true) {
        // worker is doing some "work"
        std::this_thread::sleep_for(std::chrono::seconds(rand() % 5 + 1));
        metrics_collector.incrementRequestCount();
    }

    return 0;
}
